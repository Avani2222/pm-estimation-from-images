# 🌫️ AirSight – Image-Based Air Quality Prediction

A machine learning web application that estimates **air quality and pollution levels from open-sky images** using computer vision.  
Users upload a **sky image** and receive **real-time air quality metrics** through an interactive web interface.

---

## 🚀 Live App  
🔗 **[Air Quality Prediction](https://air-quality-api-251707603195.asia-south1.run.app)**

---

## 🧠 What This Project Does

This system analyzes **open-sky images** and predicts:

- **AQI (Air Quality Index)**
- **PM2.5** – Fine particulate matter  
- **PM10** – Coarse particulate matter  
- **O₃ (Ozone)**  
- **CO (Carbon Monoxide)**  
- **SO₂ (Sulfur Dioxide)**  
- **NO₂ (Nitrogen Dioxide)**  

---

## 📊 Example Output

AQI: 63  
PM2.5: 32.49 µg/m³  
PM10: 68.19 µg/m³  
O3: 17.3 ppb  
CO: 177.68 ppm  
SO2: 4.0 ppb  
NO2: 14.22 ppb  

---

## 🖼️ How It Works

1. User uploads an **open-sky image**  
2. Image is processed using **computer vision techniques**  
3. Trained **ML models estimate pollutant concentrations**  
4. Backend API returns predictions  
5. Results are displayed on a **user-friendly dashboard**

---

## 🏗️ Tech Stack

### ⚙️ Backend
- FastAPI  
- SQLAlchemy  
- PostgreSQL  

### 🤖 Machine Learning
- PyTorch  
- Scikit-learn  
- NumPy  

### 🔐 Authentication
- Email OTP verification  
- Password hashing (bcrypt)  

### ☁️ Deployment
- Google Cloud Run  
- Docker

---

## 🔐 Features

✔ Image-based air quality prediction  
✔ REST API built with FastAPI  
✔ Machine Learning model integration  
✔ Secure user authentication with email OTP verification  
✔ Cloud deployment with a scalable backend  

---

## 🧪 Running Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

###2️⃣ Create virtual environment 
```bash
python -m venv venv source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows
```

###3️⃣ Install dependencies 
```bash
pip install -r requirements.txt
```

###4️⃣ Set environment variables 
```bash
Create a .env file:
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_app_password
```

###5️⃣ Run the server 
```bash
uvicorn src.api:app --reload
```

App will run at 👉 http://localhost:8000 write in .md format

---

## 📦 API Endpoints

| Method | Endpoint                | Description                                      |
|--------|-------------------------|--------------------------------------------------|
| POST   | `/predict`              | Upload image and get air quality predictions     |
| POST   | `/register/send-otp`    | Send OTP to email                                |
| POST   | `/register/verify-otp`  | Verify OTP and create account                    |
| POST   | `/login`                | User login                                       |

---

## 📊 Future Improvements

- 🌍 Add real-time weather data integration  
- 📱 Mobile-friendly UI  
- 🛰️ Satellite image support  
- 📈 Model performance dashboard  

---

## 👩‍💻 Author

**Avani Gupta**  
Machine Learning & Computer Vision Enthusiast  

🔗 LinkedIn: [Linkden](https://www.linkedin.com/in/avani-gupta-b59a59215/) 
🔗 GitHub: [Github](https://github.com/Avani2222) 

