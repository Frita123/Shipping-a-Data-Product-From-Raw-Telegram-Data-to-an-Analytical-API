import os
import pandas as pd
from ultralytics import YOLO
from tqdm import tqdm

# ---------------------------
# CONFIG
# ---------------------------
IMAGE_DIR = "data/raw/images"
OUTPUT_CSV = "data/yolo_results.csv"

# ---------------------------
# Load YOLOv8 Nano Model
# ---------------------------
model = YOLO("yolov8n.pt")

results_list = []

# ---------------------------
# Walk through all subfolders and images
# ---------------------------
for root, dirs, files in os.walk(IMAGE_DIR):
    for filename in tqdm(files):
        if not filename.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        image_path = os.path.join(root, filename)

        # Extract message_id from filename (example: 12345.jpg)
        message_id = os.path.splitext(filename)[0]

        detections = model(image_path)[0]

        found_person = False
        found_product = False

        for box in detections.boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            confidence = float(box.conf[0])

            # Consider these as "product-like"
            if cls_name in ["bottle", "cup", "cell phone", "book"]:
                found_product = True

            if cls_name == "person":
                found_person = True

            results_list.append({
                "message_id": message_id,
                "image_file": filename,
                "detected_class": cls_name,
                "confidence_score": round(confidence, 4)
            })

        # ---------------------------
        # Assign Image Category
        # ---------------------------
        if found_person and found_product:
            category = "promotional"
        elif found_product and not found_person:
            category = "product_display"
        elif found_person and not found_product:
            category = "lifestyle"
        else:
            category = "other"

        results_list.append({
            "message_id": message_id,
            "image_file": filename,
            "detected_class": "SUMMARY",
            "confidence_score": None,
            "image_category": category
        })

# ---------------------------
# Save CSV
# ---------------------------
df = pd.DataFrame(results_list)
df.to_csv(OUTPUT_CSV, index=False)

print("YOLO detection finished!")
print(f"Results saved to {OUTPUT_CSV}")
