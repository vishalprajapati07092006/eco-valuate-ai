import re

# Comprehensive Database for Household E-Waste
CATEGORY_DATABASE = {
    "mobile": {
        "is_ewaste": True, "ewaste_category": "Small IT & Telecommunications",
        "display_name": "Smartphone / Mobile Phone", "hazard_level": "High (Lithium-Ion Fire Risk)",
        "materials": {"Glass/Display": 35.0, "Cobalt/Lithium": 25.0, "Plastics": 20.0, "Copper": 15.0, "Gold/Silver": 5.0},
        "gold_g_per_kg": 0.18, "silver_g_per_kg": 1.75, "copper_g_per_kg": 150.0,
        "cobalt_g_per_kg": 30.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 50.0,
        "protocol": "Isolate lithium battery manually before mechanical shredding."
    },
    "cables_and_adapters": {
        "is_ewaste": True, "ewaste_category": "Small Electrical Accessories",
        "display_name": "Chargers, USB Cables, Adapters & Power Supplies", "hazard_level": "Low",
        "materials": {"Copper Wiring": 45.0, "PVC Insulation": 50.0, "Brass Contacts": 5.0},
        "gold_g_per_kg": 0.0, "silver_g_per_kg": 0.0, "copper_g_per_kg": 450.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Granulate insulation; extract high-purity copper via air-density separation."
    },
    "small_audio": {
        "is_ewaste": True, "ewaste_category": "Consumer Electronics",
        "display_name": "Earphones / Headphones", "hazard_level": "Low",
        "materials": {"Plastics": 60.0, "Copper Wire": 30.0, "Neodymium Magnets": 10.0},
        "gold_g_per_kg": 0.0, "silver_g_per_kg": 0.005, "copper_g_per_kg": 300.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Shred outer casing to liberate fine copper wiring and micro-drivers."
    },
    "power_bank": {
        "is_ewaste": True, "ewaste_category": "Energy Storage",
        "display_name": "Power Bank / Portable Battery", "hazard_level": "Extreme (Thermal Runaway Hazard)",
        "materials": {"Lithium Cells": 50.0, "Aluminum/Plastic Case": 35.0, "Control Circuit": 15.0},
        "gold_g_per_kg": 0.01, "silver_g_per_kg": 0.05, "copper_g_per_kg": 100.0,
        "cobalt_g_per_kg": 120.0, "steel_g_per_kg": 100.0, "aluminum_g_per_kg": 150.0,
        "protocol": "Fully discharge units in salt-bath solution prior to hydrometallurgical recycling."
    },
    "peripheral_low": {
        "is_ewaste": True, "ewaste_category": "Small IT Equipment",
        "display_name": "Remote Controls, Computer Mouse & Webcams", "hazard_level": "Low",
        "materials": {"ABS Plastics": 80.0, "Low-Grade PCB": 10.0, "Copper Wiring": 10.0},
        "gold_g_per_kg": 0.005, "silver_g_per_kg": 0.02, "copper_g_per_kg": 80.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Shred plastic shell; route internal single-layer PCB to secondary refiners."
    },
    "keyboard": {
        "is_ewaste": True, "ewaste_category": "Small IT Equipment",
        "display_name": "Computer Keyboard", "hazard_level": "Low",
        "materials": {"ABS Plastics": 85.0, "Copper Cable": 10.0, "Mylar Sheet": 5.0},
        "gold_g_per_kg": 0.001, "silver_g_per_kg": 0.01, "copper_g_per_kg": 100.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Granulate plastic housing for municipal recycling; extract copper wiring."
    },
    "networking_box": {
        "is_ewaste": True, "ewaste_category": "Telecommunications",
        "display_name": "Wi-Fi Router / Modem / Set-Top Box", "hazard_level": "Low",
        "materials": {"Plastic Casing": 50.0, "Mid-Grade PCB": 35.0, "Copper Wiring/Transformers": 15.0},
        "gold_g_per_kg": 0.05, "silver_g_per_kg": 0.25, "copper_g_per_kg": 150.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 50.0, "aluminum_g_per_kg": 30.0,
        "protocol": "Remove plastic housing and dismantle internal mid-grade logic board."
    },
    "laptop": {
        "is_ewaste": True, "ewaste_category": "IT Equipment",
        "display_name": "Old Laptop", "hazard_level": "Medium (Battery Hazard)",
        "materials": {"Motherboard/RAM": 30.0, "Aluminum Chassis": 25.0, "Display Screen": 25.0, "Li-Ion Battery": 20.0},
        "gold_g_per_kg": 0.15, "silver_g_per_kg": 0.80, "copper_g_per_kg": 200.0,
        "cobalt_g_per_kg": 20.0, "steel_g_per_kg": 50.0, "aluminum_g_per_kg": 250.0,
        "protocol": "Remove battery first. Separate high-grade mainboard from LED display unit."
    },
    "desktop_pc": {
        "is_ewaste": True, "ewaste_category": "IT Equipment",
        "display_name": "Desktop Computer Tower", "hazard_level": "Medium",
        "materials": {"Steel Case": 60.0, "Motherboard/Cards": 20.0, "Power Supply": 10.0, "Aluminum Heatsinks": 10.0},
        "gold_g_per_kg": 0.10, "silver_g_per_kg": 0.50, "copper_g_per_kg": 250.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 600.0, "aluminum_g_per_kg": 100.0,
        "protocol": "Dismantle steel case; harvest high-grade motherboards, RAM, and copper heatsinks."
    },
    "monitor_tv": {
        "is_ewaste": True, "ewaste_category": "Displays & Screens",
        "display_name": "Monitors & Televisions", "hazard_level": "High (Mercury/Lead)",
        "materials": {"Glass Panel": 45.0, "Plastics": 35.0, "Copper Coils": 12.0, "Driver Board": 8.0},
        "gold_g_per_kg": 0.03, "silver_g_per_kg": 0.15, "copper_g_per_kg": 120.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 100.0, "aluminum_g_per_kg": 50.0,
        "protocol": "Extract mercury backlights or CRT yokes under negative pressure filtration."
    },
    "printer_scanner": {
        "is_ewaste": True, "ewaste_category": "Office Equipment",
        "display_name": "Printer / Scanner", "hazard_level": "Medium (Toner Dust Hazard)",
        "materials": {"Plastics": 60.0, "Steel Frame": 25.0, "Stepper Motors": 10.0, "Logic Board": 5.0},
        "gold_g_per_kg": 0.01, "silver_g_per_kg": 0.05, "copper_g_per_kg": 100.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 250.0, "aluminum_g_per_kg": 20.0,
        "protocol": "Isolate toner/ink cartridges before mechanical shredding."
    },
    "storage_drive": {
        "is_ewaste": True, "ewaste_category": "Data Storage",
        "display_name": "Hard Drive (HDD) / Solid State Drive (SSD)", "hazard_level": "Low (Data Security Risk)",
        "materials": {"Aluminum Casing": 55.0, "Steel Chassis": 30.0, "Rare Earth Magnets": 5.0, "PCB": 10.0},
        "gold_g_per_kg": 0.08, "silver_g_per_kg": 0.30, "copper_g_per_kg": 120.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 300.0, "aluminum_g_per_kg": 550.0,
        "protocol": "Degauss/shred disk platters for data security; recover aluminum and neodymium."
    },
    "flash_memory": {
        "is_ewaste": True, "ewaste_category": "Data Storage",
        "display_name": "Pen Drive / Memory Cards", "hazard_level": "Low",
        "materials": {"Silicon Chips": 40.0, "Plastics/Resin": 40.0, "Gold/Copper Contacts": 20.0},
        "gold_g_per_kg": 0.35, "silver_g_per_kg": 1.20, "copper_g_per_kg": 200.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Chemical leaching of monolithic micro-chips to recover fine gold bond wires."
    },
    "ups_unit": {
        "is_ewaste": True, "ewaste_category": "Energy Storage & Power Systems",
        "display_name": "UPS Unit (Uninterruptible Power Supply)", "hazard_level": "High (Lead-Acid Hazard)",
        "materials": {"Lead-Acid Battery": 60.0, "Steel Housing": 25.0, "Transformer Copper": 15.0},
        "gold_g_per_kg": 0.005, "silver_g_per_kg": 0.02, "copper_g_per_kg": 150.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 250.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Extract lead-acid battery for dedicated chemical treatment."
    },
    "large_appliance": {
        "is_ewaste": True, "ewaste_category": "Large Household Appliances",
        "display_name": "Refrigerator / Washing Machine / Air Conditioner", "hazard_level": "Medium (Refrigerant Gases)",
        "materials": {"Steel Chassis": 60.0, "Plastics": 20.0, "Copper Compressor Motors": 10.0, "Aluminum": 10.0},
        "gold_g_per_kg": 0.001, "silver_g_per_kg": 0.01, "copper_g_per_kg": 100.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 600.0, "aluminum_g_per_kg": 100.0,
        "protocol": "Evacuate refrigerant gases (CFCs/HFCs); extract heavy electric motors."
    },
    "small_kitchen_appliance": {
        "is_ewaste": True, "ewaste_category": "Small Household Appliances",
        "display_name": "Microwave / Kettle / Mixer / Toaster / Iron", "hazard_level": "Medium (High-Voltage Capacitor in Microwaves)",
        "materials": {"Steel Casing": 55.0, "Copper Windings": 20.0, "Plastics": 20.0, "Heating Elements": 5.0},
        "gold_g_per_kg": 0.002, "silver_g_per_kg": 0.02, "copper_g_per_kg": 180.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 550.0, "aluminum_g_per_kg": 30.0,
        "protocol": "Discharge microwave high-voltage capacitors; extract internal copper transformers."
    },
    "lighting_mercury": {
        "is_ewaste": True, "ewaste_category": "Lighting Equipment",
        "display_name": "CFL Bulbs / Fluorescent Tubes", "hazard_level": "Extreme (Toxic Mercury Vapor)",
        "materials": {"Glass Tube": 80.0, "Aluminum Contacts": 10.0, "Phosphor Powder": 10.0},
        "gold_g_per_kg": 0.0, "silver_g_per_kg": 0.0, "copper_g_per_kg": 10.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 100.0,
        "protocol": "CRITICAL: Process in sealed negative-pressure drum crushing units to capture mercury vapor."
    },
    "lighting_led": {
        "is_ewaste": True, "ewaste_category": "Lighting Equipment",
        "display_name": "LED Bulbs / Emergency Lights", "hazard_level": "Low",
        "materials": {"Aluminum Heatsink": 45.0, "Plastic Diffuser": 35.0, "Driver Board": 20.0},
        "gold_g_per_kg": 0.005, "silver_g_per_kg": 0.05, "copper_g_per_kg": 40.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 50.0, "aluminum_g_per_kg": 450.0,
        "protocol": "Separate aluminum cooling body from small internal LED driver circuit."
    },
    "extension_board": {
        "is_ewaste": True, "ewaste_category": "Electrical Supplies",
        "display_name": "Extension Boards & Power Strips", "hazard_level": "Low",
        "materials": {"Hard Plastics": 70.0, "Brass/Copper Busbars": 30.0},
        "gold_g_per_kg": 0.0, "silver_g_per_kg": 0.0, "copper_g_per_kg": 250.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 0.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Dismantle housing to extract heavy internal brass/copper contacts."
    },
    "rechargeable_batteries": {
        "is_ewaste": True, "ewaste_category": "Energy Storage",
        "display_name": "Used Rechargeable / Laptop / Phone Batteries", "hazard_level": "Extreme (Thermal & Chemical Risk)",
        "materials": {"Lithium/Cobalt/Nickel": 40.0, "Steel Casing": 30.0, "Graphite": 20.0, "Electrolyte": 10.0},
        "gold_g_per_kg": 0.0, "silver_g_per_kg": 0.0, "copper_g_per_kg": 60.0,
        "cobalt_g_per_kg": 150.0, "steel_g_per_kg": 300.0, "aluminum_g_per_kg": 50.0,
        "protocol": "Store in dry sand bins. Send to hydrometallurgical recycling facilities."
    },
    "dry_cell_batteries": {
        "is_ewaste": True, "ewaste_category": "Energy Storage",
        "display_name": "Remote Control (Alkaline) Batteries", "hazard_level": "Low to Medium (Acid Leakage)",
        "materials": {"Zinc": 30.0, "Manganese Dioxide": 30.0, "Steel Shell": 25.0, "Carbon": 15.0},
        "gold_g_per_kg": 0.0, "silver_g_per_kg": 0.0, "copper_g_per_kg": 0.0,
        "cobalt_g_per_kg": 0.0, "steel_g_per_kg": 250.0, "aluminum_g_per_kg": 0.0,
        "protocol": "Process via pyrometallurgical recovery to extract elemental zinc and manganese."
    }
}


class WasteValuator:
    def __init__(self):
        # Base metal prices (USD per gram)
        self.prices = {
            "gold": 75.0,
            "silver": 0.95,
            "copper": 0.0095,      # ~$9.50/kg
            "cobalt": 0.028,       # ~$28.00/kg
            "aluminum": 0.0024,    # ~$2.40/kg
            "steel": 0.0004        # ~$0.40/kg
        }

        # Exact multi-word matching rules ordered by priority
        self.keyword_rules = [
            # Small Electronics
            (r"\bmobile-phone battery\b|\blaptop battery\b|\brechargeable battery\b", "rechargeable_batteries"),
            (r"\bremote-control battery\b|\balkaline battery\b", "dry_cell_batteries"),
            (r"\bups battery\b|\blead acid battery\b", "ups_unit"),
            (r"\bpower bank\b", "power_bank"),
            (r"\bcharger\b|\busb cable\b|\badapter\b|\bpower supply\b|\bwiring\b", "cables_and_adapters"),
            (r"\bearphone\b|\bheadphone\b", "small_audio"),
            (r"\bwebcam\b|\bremote control\b|\bmouse\b", "peripheral_low"),
            (r"\bkeyboard\b", "keyboard"),
            (r"\bwi-fi router\b|\bmodem\b|\bset-top box\b|\brouter\b", "networking_box"),
            (r"\bmobile\b|\bsmartphone\b|\bcell phone\b", "mobile"),

            # Computer & Office
            (r"\blaptop\b|\bold laptop\b|\bnotebook\b|\bmacbook\b", "laptop"),
            (r"\bdesktop computer\b|\bdesktop\b|\bcomputer tower\b|\bpc\b", "desktop_pc"),
            (r"\bmonitor\b|\bdisplay\b", "monitor_tv"),
            (r"\bprinter\b|\bscanner\b", "printer_scanner"),
            (r"\bhard drive\b|\bssd\b|\bhdd\b", "storage_drive"),
            (r"\bups unit\b|\bups\b", "ups_unit"),
            (r"\bpen drive\b|\bmemory card\b|\bflash drive\b", "flash_memory"),

            # Home Appliances
            (r"\btelevision\b|\bold tv\b|\btv\b", "monitor_tv"),
            (r"\brefrigerator\b|\bwashing machine\b|\bair conditioner\b|\bac unit\b", "large_appliance"),
            (r"\bmicrowave\b|\belectric iron\b|\belectric kettle\b|\bmixer\b|\bgrinder\b|\btoaster\b", "small_kitchen_appliance"),

            # Lighting & Electrical
            (r"\bcfl bulb\b|\bfluorescent tube\b", "lighting_mercury"),
            (r"\bled bulb\b|\bemergency light\b", "lighting_led"),
            (r"\bextension board\b|\bpower strip\b", "extension_board"),

            # Generic fallbacks
            (r"\bbattery\b|\bbatteries\b", "rechargeable_batteries")
        ]

    def analyze(self, raw_label: str, weight_kg: float = 1.0):
        if not weight_kg or weight_kg <= 0:
            weight_kg = 1.0

        clean_text = raw_label.lower().strip()
        matched_key = None

        # 1. First, check direct key or display_name match
        for key, info in CATEGORY_DATABASE.items():
            if clean_text == key or clean_text == info["display_name"].lower():
                matched_key = key
                break

        # 2. If no exact key/display match, run through regex rules
        if not matched_key:
            for pattern, db_key in self.keyword_rules:
                if re.search(pattern, clean_text):
                    matched_key = db_key
                    break

        # 3. Last fallback (changed default from kitchen appliance to laptop if computer terms exist, otherwise laptop as safe default)
        if not matched_key or matched_key not in CATEGORY_DATABASE:
            matched_key = "laptop"

        info = CATEGORY_DATABASE[matched_key]

        gold_g = info["gold_g_per_kg"] * weight_kg
        silver_g = info["silver_g_per_kg"] * weight_kg
        copper_g = info["copper_g_per_kg"] * weight_kg
        cobalt_g = info.get("cobalt_g_per_kg", 0.0) * weight_kg
        steel_g = info.get("steel_g_per_kg", 0.0) * weight_kg
        aluminum_g = info.get("aluminum_g_per_kg", 0.0) * weight_kg

        val_usd = (
            (gold_g * self.prices["gold"]) +
            (silver_g * self.prices["silver"]) +
            (copper_g * self.prices["copper"]) +
            (cobalt_g * self.prices["cobalt"]) +
            (steel_g * self.prices["steel"]) +
            (aluminum_g * self.prices["aluminum"])
        )

        metals_dict = {
            "gold": round(gold_g, 3),
            "silver": round(silver_g, 3),
            "copper": round(copper_g, 1),
            "cobalt": round(cobalt_g, 1),
            "steel": round(steel_g, 1),
            "aluminum": round(aluminum_g, 1)
        }

        return {
            "is_ewaste": True,
            "category": info["ewaste_category"],
            "display_name": info["display_name"],
            "hazard": info["hazard_level"],
            "materials": info["materials"],
            "est_value_usd": round(val_usd, 2),
            "scrap_market_value": round(val_usd, 2),
            
            # Explicit top-level fields for direct frontend UI bindings
            "gold_g": round(gold_g, 3),
            "copper_g": round(copper_g, 1),
            "silver_g": round(silver_g, 3),
            "aluminum_g": round(aluminum_g, 1),
            "steel_g": round(steel_g, 1),
            "cobalt_g": round(cobalt_g, 1),

            # Dual aliases for nested structure support
            "metals_g": metals_dict,
            "metals_recovered_g": metals_dict,
            
            "protocol": info["protocol"]
        }