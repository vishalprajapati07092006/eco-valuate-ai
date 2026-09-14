import streamlit as st
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
import os
import plotly.express as px
from static_data import WasteValuator

st.set_page_config(page_title="AI Waste & E-Waste Classifier", page_icon="♻️", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; color: #2E7D32; font-weight: bold; text-align: center; }
    .sub-subtitle { font-size: 1.1rem; color: #555555; text-align: center; margin-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">♻️ AI Waste & E-Waste Classification System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-subtitle">Classify scrap items, detect E-Waste categories, and analyze extractable raw materials</div>', unsafe_allow_html=True)

@st.cache_resource
def load_trained_model():
    model_path = "models/dynamic_ewaste.pth"
    index_path = "models/class_index.json"
    
    if not os.path.exists(model_path) or not os.path.exists(index_path):
        return None, None

    with open(index_path, "r") as f:
        class_idx = json.load(f)

    num_classes = len(class_idx)
    model = models.efficientnet_b0(pretrained=False)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model, class_idx

model, class_idx = load_trained_model()
valuator = WasteValuator()

if model is None:
    st.error("⚠️ Model not found! Please run `python train_model.py` first to train your neural network.")
else:
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("📷 Upload Item Photo")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])
        weight = st.number_input("Input Weight (kg)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)

        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            st.image(img, caption="Target Waste Item", use_container_width=True)

    with col2:
        st.subheader("📊 Material & Classification Results")
        
        if uploaded_file:
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            
            input_tensor = transform(img).unsqueeze(0)
            
            with torch.no_grad():
                outputs = model(input_tensor)
                probs = torch.nn.functional.softmax(outputs[0], dim=0)
                conf, pred_class_id = torch.max(probs, 0)
                
            detected_label = class_idx[str(pred_class_id.item())]
            res = valuator.analyze(detected_label, weight_kg=weight)

            st.success(f"**Identified Item:** {res['display_name']} ({conf.item()*100:.1f}% AI Confidence)")
            
            if res["is_ewaste"]:
                st.warning(f"⚡ **E-Waste Category:** {res['category']}")
            else:
                st.info(f"🟢 **Category:** {res['category']}")

            mat_data = res["materials"]
            fig = px.pie(
                values=list(mat_data.values()), 
                names=list(mat_data.keys()),
                title="Useful Extractable Materials Breakdown (%)",
                color_discrete_sequence=px.colors.sequential.Greens_r,
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

            if res["is_ewaste"]:
                m1, m2, m3 = st.columns(3)
                m1.metric("Est. Gold Yield", f"{res['gold_g']} g")
                m2.metric("Est. Copper Yield", f"{res['copper_g']} g")
                m3.metric("Scrap Payout", f"${res['est_value_usd']} USD")

            st.write(f"**Hazard Rating:** `{res['hazard']}`")
            st.write(f"**Disposal Protocol:** {res['protocol']}")