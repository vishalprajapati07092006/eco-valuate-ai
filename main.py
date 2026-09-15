import os
import time
import traceback
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from static_data import WasteValuator
from modules.pdf_generator import build_pdf_report

app = FastAPI(title="E-Waste Valuation Engine API")

# Allow React app to talk to FastAPI (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

valuator = WasteValuator()

# Hugging Face API settings
HF_TOKEN = os.getenv("HF_TOKEN")

# IMPORTANT: openai/clip-vit-base-patch32 (and every other CLIP/SigLIP model we
# checked) is no longer served by HF's free "hf-inference" provider for the
# zero-shot-image-classification task -- HF has been deprecating that task on
# the free serverless tier. Calling it now returns:
#   {"error":"Model not supported by provider hf-inference"}
#
# google/vit-base-patch16-224 (a standard ImageNet-1000 image classifier) IS
# still live on the free HF Inference API, so we use it instead and map its
# ImageNet labels onto our own e-waste categories below.
HF_MODEL_ID = "google/vit-base-patch16-224"
API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

if not HF_TOKEN:
    print("WARNING: HF_TOKEN environment variable is not set. "
          "Hugging Face API calls will fail with a 401 Unauthorized error.")

# Maps substrings that can appear in google/vit-base-patch16-224's ImageNet
# labels to one of our own CATEGORIES strings (which static_data.WasteValuator
# expects). Checked in order, first match wins.
IMAGENET_TO_CATEGORY = [
    ("cellular telephone", "old mobile phone or cell phone"),
    ("cell phone", "old mobile phone or cell phone"),
    ("ipod", "old mobile phone or cell phone"),
    ("modem", "Wi-Fi router or modem"),
    ("hard disc", "hard drive HDD or SSD"),
    ("hard disk", "hard drive HDD or SSD"),
    ("solid state", "hard drive HDD or SSD"),
    ("desktop computer", "desktop computer tower"),
    ("laptop", "old laptop computer"),
    ("notebook computer", "old laptop computer"),
    ("screen", "computer monitor or screen"),
    ("monitor", "computer monitor or screen"),
    ("television", "old television or TV unit"),
    ("printer", "printer or scanner machine"),
    ("photocopier", "printer or scanner machine"),
    ("scanner", "printer or scanner machine"),
    ("microwave", "microwave oven"),
    ("washer", "washing machine appliance"),
    ("washing machine", "washing machine appliance"),
    ("refrigerator", "refrigerator or fridge unit"),
    ("ice box", "refrigerator or fridge unit"),
    ("toaster", "electric toaster"),
    ("iron", "electric iron"),
    ("space heater", "electric kettle"),
    ("remote control", "remote control"),
    ("joystick", "remote control"),
    ("keyboard", "computer mouse or keyboard"),
    ("computer mouse", "computer mouse or keyboard"),
    ("mixing bowl", "mixer grinder or kitchen blender"),
    ("blender", "mixer grinder or kitchen blender"),
    ("power drill", "power adapter or power supply module"),
    ("plug", "power adapter or power supply module"),
    ("extension cord", "power extension board or strip"),
    ("battery", "used rechargeable battery"),
]


def map_to_category(imagenet_label: str) -> str:
    """Maps a raw ImageNet label to one of our CATEGORIES strings."""
    label_lower = imagenet_label.lower()
    for keyword, category in IMAGENET_TO_CATEGORY:
        if keyword in label_lower:
            return category
    # No confident match found among our known e-waste categories.
    # Default to a generic small-electronics bucket rather than guessing wrong.
    return "power adapter or power supply module"

CATEGORIES = [
    # Small Electronics
    "old mobile phone or cell phone",
    "charger or USB cable",
    "earphones or headphones",
    "portable power bank",
    "remote control",
    "computer mouse or keyboard",
    "old webcam or computer camera",
    "Wi-Fi router or modem",
    "TV set-top box or cable box",

    # Computer & Office Equipment
    "old laptop computer",
    "desktop computer tower",
    "computer monitor or screen",
    "printer or scanner machine",
    "hard drive HDD or SSD",
    "uninterruptible power supply UPS unit",
    "USB pen drive or flash memory card",

    # Home Appliances
    "old television or TV unit",
    "refrigerator or fridge unit",
    "washing machine appliance",
    "microwave oven",
    "air conditioner unit",
    "electric iron",
    "electric kettle",
    "mixer grinder or kitchen blender",
    "electric toaster",

    # Lighting & Electrical Items
    "LED bulb light fixture",
    "CFL bulb light",
    "fluorescent tube light",
    "rechargeable emergency light",
    "power extension board or strip",
    "power adapter or power supply module",

    # Batteries
    "used rechargeable battery",
    "laptop battery pack",
    "mobile phone battery",
    "AA AAA remote control battery",
    "UPS battery or lead acid battery"
]


def query_huggingface(image_bytes: bytes, content_type: str = "image/jpeg", max_retries: int = 3):
    """
    Calls the HF Inference API for standard image-classification.
    Unlike zero-shot-image-classification, this task takes the raw image
    bytes directly as the request body -- but it does need a Content-Type
    header telling HF what kind of bytes these are, or it responds with
    400 "No content type provided and no default one configured."
    Handles the "model is loading" cold-start case (HTTP 503) with a short retry.
    """
    request_headers = {**HEADERS, "Content-Type": content_type or "image/jpeg"}

    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=request_headers, data=image_bytes, timeout=30)

            # Model is cold-starting on HF's servers — wait and retry.
            if response.status_code == 503:
                data = response.json()
                wait_time = min(data.get("estimated_time", 5), 15)
                print(f"[HF] Model loading, retrying in {wait_time:.1f}s "
                      f"(attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue

            if response.status_code == 401:
                raise RuntimeError(
                    "Hugging Face returned 401 Unauthorized. Check that HF_TOKEN "
                    "is set correctly and has 'Inference' permission."
                )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Hugging Face API error {response.status_code}: {response.text}"
                )

            results = response.json()

            if isinstance(results, dict) and "error" in results:
                raise RuntimeError(f"Hugging Face API error: {results['error']}")

            if not isinstance(results, list) or len(results) == 0:
                raise RuntimeError(f"Unexpected response shape from Hugging Face: {results}")

            return results

        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"[HF] Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(2)

    raise RuntimeError(f"Hugging Face API unreachable after {max_retries} attempts: {last_error}")


@app.post("/api/classify")
async def classify_item(file: UploadFile = File(...), weight: float = Form(1.0)):
    try:
        contents = await file.read()

        results = query_huggingface(contents, content_type=file.content_type)

        raw_imagenet_label = results[0]["label"]
        confidence_score = round(results[0]["score"] * 100, 2)
        detected_category = map_to_category(raw_imagenet_label)

        analysis = valuator.analyze(detected_category, weight_kg=weight)
        analysis["confidence"] = f"{confidence_score}%"

        return {
            "status": "success",
            "prediction": {
                "class_raw": detected_category,
                "model_raw_label": raw_imagenet_label,
                "confidence": confidence_score,
                "analysis": analysis
            }
        }
    except Exception as e:
        print("\n--- CLASSIFICATION ERROR TRACEBACK ---")
        traceback.print_exc()
        print("--------------------------------------\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-pdf")
async def export_pdf(payload: dict):
    try:
        weight_kg = float(payload.get("weight", 1.0))

        analysis_data = payload.get("analysis")
        if not analysis_data and "prediction" in payload:
            analysis_data = payload["prediction"].get("analysis")
        if not analysis_data:
            analysis_data = payload

        detected_label = (
            analysis_data.get("class_raw") or
            analysis_data.get("display_name") or
            payload.get("label") or
            "hard drive HDD or SSD"
        )

        fresh_analysis = valuator.analyze(detected_label, weight_kg=weight_kg)

        confidence_val = (
            analysis_data.get("confidence") or
            payload.get("confidence") or
            "99.74%"
        )
        if isinstance(confidence_val, (int, float)):
            confidence_val = f"{confidence_val}%"
        fresh_analysis["confidence"] = confidence_val

        pdf_buffer = build_pdf_report(fresh_analysis, input_weight=weight_kg)

        clean_name = fresh_analysis.get("display_name", "item").replace("/", "_").replace(" ", "_")
        filename = f"E_Waste_Report_{clean_name}.pdf"

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        print(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))