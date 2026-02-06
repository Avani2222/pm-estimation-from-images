# 🌍 PM Estimation from Images

A **FastAPI-based deep learning application** that predicts **air quality metrics** (AQI, PM2.5, PM10, etc.) from uploaded sky/atmosphere images — with **secure user authentication and account management**.

This system uses a trained computer vision model to estimate pollution levels from visual environmental cues in images.

---

## 🚀 Features

- 🖼️ **Image-Based Air Quality Prediction**  
  Upload an image and receive estimated pollution metrics.

- 🔐 **User Authentication System**
  - User registration  
  - Login with password  
  - JWT-based authentication  
  - Protected API routes  

- ⚡ **FastAPI Backend**
  - High-performance async API  
  - Automatic Swagger & ReDoc documentation  

- 🧠 **Deep Learning Model Integration**
  - PyTorch model loading  
  - Image preprocessing  
  - Multi-metric regression output  

---

## 🧠 How It Works

1. A user creates an account or logs in  
2. The user uploads an image through the `/predict` endpoint  
3. The backend processes the image  
4. The trained model predicts air quality metrics  
5. The results are returned as a JSON response  

---

## 📂 Project Structure

pm-estimation-from-images/
│
├── models/ # Saved model weights
├── notebooks/ # Training / research notebooks
├── src/
│ ├── api.py # Main FastAPI app
│ ├── auth.py # Authentication routes & logic
│ ├── database.py # Database connection & models
│ ├── inference.py # Model loading and prediction
│ └── utils/ # Helper functions
│
├── static/ # Frontend files (HTML/CSS/JS)
├── requirements.txt # Dependencies
├── runtime.txt # Python runtime version (for deployment)
└── README.md


---

## 🛠️ Installation (Local Setup)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Avani2222/pm-estimation-from-images.git
cd pm-estimation-from-images
```

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Set Environment Variables

