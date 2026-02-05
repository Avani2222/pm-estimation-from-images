import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import joblib
from model import get_model  # your custom model loader


# -------------------------------
# CONFIG
# -------------------------------
MODEL_PATH = "models/resnet34_aqi.pth"
SCALER_PATH = "/Users/avanigupta/pm-estimation-from-images/models/label_scaler.save"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LABEL_COLS = ['AQI','PM2.5','PM10','O3','CO','SO2','NO2']

# Units for each label
UNITS = {
    'AQI': '',
    'PM2.5': 'µg/m³',
    'PM10': 'µg/m³',
    'O3': 'ppb',
    'CO': 'ppm',
    'SO2': 'ppb',
    'NO2': 'ppb'
}

# -------------------------------
# IMAGE TRANSFORMS (same as training)
# -------------------------------
img_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# -------------------------------
# LOAD MODEL & SCALER
# -------------------------------
model = get_model("resnet34").to(DEVICE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()

scaler = joblib.load(SCALER_PATH)  # saved MinMaxScaler

# -------------------------------
# INFERENCE FUNCTION
# -------------------------------
def predict_image(img_path):
    """
    Predict AQI and pollutant values for a single image.
    Returns a dict with values converted back to original scale and units.
    """
    # Load and preprocess image
    img = Image.open(img_path).convert("RGB")
    img_tensor = img_transforms(img).unsqueeze(0).to(DEVICE)  # add batch dim

    # Model prediction
    with torch.no_grad():
        pred_scaled = model(img_tensor).cpu().numpy()  # 1 x 7

    # Inverse transform to original scale
    pred_unscaled = scaler.inverse_transform(pred_scaled)

    # Format results with units
    pred_dict = {}
    for i, label in enumerate(LABEL_COLS):
        value = float(pred_unscaled[0, i])
        unit = UNITS[label]
        # Round for nicer display
        if label == 'AQI':
            pred_dict[label] = f"{int(round(value))} {unit}"
        else:
            pred_dict[label] = f"{round(value, 2)} {unit}"
    
    return pred_dict

# # -------------------------------
# # EXAMPLE USAGE
# # -------------------------------
# if __name__ == "__main__":
#     test_img = "/Users/avanigupta/pm-estimation-from-images/data/archive/Air Pollution Image Dataset/Combined_Dataset/All_img/BENGR_Good_2023-02-19-08.30-1-1.jpg"
#     predictions = predict_image(test_img)
#     print(predictions)
