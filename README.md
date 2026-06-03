# 🌍 AI Disaster Prediction System – Backend

**AI-based Natural Disaster Risk Prediction with Explainable Insights and Decision Support System**  
*Backend API Service*

---

## 📖 Overview

The **AI Disaster Prediction System** is an intelligent backend service designed to predict potential natural disasters using weather parameters and machine learning.

The system utilizes a **Random Forest Classifier** trained on historical weather data to classify environmental conditions into one of four categories:

- 🌊 Flood
- ☀️ Drought
- 🌪️ Storm
- ✅ Normal

In addition to prediction, the system provides:

- **Explainable AI (SHAP)** for feature-level prediction explanations
- **Decision Support Recommendations** based on predicted disaster type
- **Prediction Analytics Dashboard APIs**
- **JWT Authentication & Authorization**
- **Prediction History Tracking**

Built using **Django**, **Django REST Framework**, **Scikit-learn**, **SHAP**, and **PostgreSQL**.

---

## ✨ Features

| Module | Endpoint | Description |
|----------|------------|-------------|
| Authentication | `/api/auth/register/` | User registration |
| Authentication | `/api/auth/login/` | User login with JWT |
| Prediction | `/api/predict/` | Disaster prediction API |
| Analytics | `/api/analytics/history/` | User prediction history |
| Analytics | `/api/analytics/summary/` | Analytics summary |
| Explainable AI | Integrated | SHAP feature explanations |
| Recommendations | Integrated | Disaster response suggestions |

---

## 🛠️ Tech Stack

### Backend
- Python 3.12+
- Django 6.0
- Django REST Framework (DRF)

### Authentication
- Simple JWT

### Machine Learning
- Scikit-learn
- Random Forest Classifier
- SHAP
- Joblib

### Database
- PostgreSQL
- SQLite (Development)

### Utilities
- Python Dotenv
- Django CORS Headers
- NumPy
- Pandas

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/archana9207/ai-disaster-backend.git
cd ai-disaster-backend
```

### 2️⃣ Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### Example Requirements

```txt
Django==6.0
djangorestframework==3.15.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.4.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
scikit-learn==1.5.0
joblib==1.4.0
shap==0.45.0
numpy==1.26.0
pandas==2.2.0
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

DJANGO_SECRET_KEY=your-secret-key
```

> ⚠️ Never commit your `.env` file to GitHub.

### 5️⃣ Apply Migrations

```bash
python manage.py makemigrations users prediction
python manage.py migrate
```

### 6️⃣ Train or Load ML Model

If the model file is missing:

```bash
python config/ml/retrain_model.py
```

Ensure the dataset file:

```text
GlobalWeatherRepository.csv
```

is available in the correct location referenced by the script.

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

Backend API:

```text
http://localhost:8000
```

---

## 🔐 Authentication APIs

### Register

```http
POST /api/auth/register/
```

#### Request

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

---

### Login

```http
POST /api/auth/login/
```

#### Request

```json
{
  "username": "john",
  "password": "secret123"
}
```

#### Response

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  }
}
```

---

### Refresh Token

```http
POST /api/token/refresh/
```

### Authorization Header

All protected APIs require:

```text
Authorization: Bearer <access_token>
```

---

## 🌦️ Disaster Prediction API

### Endpoint

```http
POST /api/predict/
```

### Request

```json
{
  "temperature_celsius": 38.5,
  "humidity": 25,
  "precip_mm": 0,
  "wind_kph": 15,
  "pressure_mb": 1012
}
```

### Response

```json
{
  "disaster_type": "Drought",
  "recommendation": "Implement water conservation measures...",
  "actions": [
    "Enforce water use restrictions",
    "Monitor reservoirs"
  ],
  "shap_explanation": {
    "Temperature": 0.43,
    "Humidity": -0.22,
    "Precipitation": -0.01,
    "Wind Speed": 0.03,
    "Pressure": 0.02
  },
  "message": "Prediction based on current weather parameters."
}
```

---

## 📊 Analytics APIs

### Prediction History

```http
GET /api/analytics/history/?limit=10
```

Returns:

- Recent predictions
- Disaster type
- Timestamp
- Weather values

### Analytics Summary

```http
GET /api/analytics/summary/
```

Returns:

- Total Predictions
- Disaster Breakdown
- Most Common Disaster
- Recent Predictions
- Monthly Trends

#### Example Response

```json
{
  "total_predictions": 120,
  "most_common_disaster": "Flood",
  "disaster_breakdown": {
    "Flood": 52,
    "Storm": 31,
    "Drought": 21,
    "Normal": 16
  }
}
```

---

## 🧪 Testing Using cURL

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"username":"john","password":"secret123"}'
```

### Predict

```bash
curl -X POST http://localhost:8000/api/predict/ \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"temperature_celsius":36,"humidity":20,"precip_mm":0,"wind_kph":10,"pressure_mb":1010}'
```

### Analytics Summary

```bash
curl -X GET http://localhost:8000/api/analytics/summary/ \
-H "Authorization: Bearer <access_token>"
```

---

## 📂 Project Structure

```text
backend/
│
├── apps/
│   ├── authentication/
│   ├── users/
│   ├── prediction/
│   └── analytics/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ml/
│       ├── model/
│       │   └── n_disaster_model.pkl
│       └── retrain_model.py
│
├── .env
├── manage.py
└── requirements.txt
```

---

## 🔮 Future Enhancements

- Real-time weather API integration
- Disaster risk visualization dashboard
- Geographical disaster mapping
- Email & SMS alert system
- Deep Learning based prediction models
- Docker deployment
- CI/CD Pipeline integration

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit pull requests.

---

## 📄 License

This project was developed for academic and research purposes.

All rights reserved.

---

## 🙏 Acknowledgements

- Kaggle Global Weather Repository Dataset
- SHAP Community
- Scikit-learn Community
- Django REST Framework
- Yenepoya (Deemed-to-be University)

---

## 👨‍🎓 Author

**Archana K**  
Bachelor of Computer Applications (BCA)  
Specialization: AI & Data Science  
Year: 2026