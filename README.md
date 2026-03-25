#  AI-Powered Crop Recommendation System

A data-driven web application designed to assist farmers in making informed decisions about crop selection.  
This project is a prototype developed for the **Smart India Hackathon 2025** under the problem statement *"AI-Based Crop Recommendation for Farmers"* in the Agriculture, FoodTech & Rural Development category.

Our solution aims to bridge the gap between traditional farming practices and modern data science, empowering farmers to increase yield, maximize profitability, and practice sustainable agriculture.

---

##  Table of Contents
- [Problem Statement](#-problem-statement)
- [Live Demo & Screenshots](#-live-demo--screenshots)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Setup and Installation](#-setup-and-installation)
- [Usage](#-usage)
- [Future Scope](#-future-scope)
- [Contributors](#-contributors)
---

##  Problem Statement
In India, a farmer's choice of crop is often dictated by tradition and intuition rather than scientific data.  
This can lead to suboptimal yields, financial losses, and inefficient use of resources, especially with the increasing challenges of climate change and soil degradation.  

This project directly addresses the issue by providing a simple tool that delivers **scientific, personalized crop recommendations** based on specific farm data.

---

##  Live Demo & Screenshots
A live demo of the application can be accessed here:  
 [Link to your deployed application]  

**Screenshot**  
The application's user-friendly interface for data input and recommendation output.

---

##  Features
- **Intuitive User Interface**: Clean, simple web form for farmers to input soil and environmental data.  
- **Instantaneous Recommendations**: ML model provides real-time crop suggestions.  
- **Data-Driven AI Model**: Uses RandomForestClassifier trained on agricultural dataset.  
- **Scalable Architecture**: Flask backend, easy integration with services.  

---

##  Technology Stack

**Backend**  
- Python 3.9  
- Flask  

**Machine Learning**  
- Scikit-learn  
- Pandas  
- NumPy  

**Frontend**  
- HTML5  
- CSS3  

**Model Persistence**  
- Pickle  

---

##  System Architecture

```text
[User] -> [Browser (HTML Form)] -> [POST Request] 
       -> [Flask App] -> [ML Model] -> [Prediction] 
       -> [Flask App] -> [Rendered HTML] -> [User]
````

---

##  Setup and Installation

### Prerequisites

* Python 3.8+
* pip and venv

### Steps

```bash
# Clone repository
git clone https://github.com/your-username/crop-recommender.git
cd crop-recommender

# Create virtual environment
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### (Optional) Train the model

```bash
python train_model.py
```

Generates a new `model.pkl` based on `crop_recommendation.csv`.

### Run the Flask application

```bash
flask run
# or
python app.py
```

Access app in browser → [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

##  Usage

1. Run the app and open the browser interface.
2. Enter farm data (Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall).
3. Click **Get Recommendation**.
4. The most suitable crop will be displayed instantly.

---

##  Future Scope

* API integration with live weather data.
* GPS-based region-specific recommendations.
* Government soil database integration.
* Fertilizer & pest prediction modules.
* Multilingual interface for accessibility.
* Native Android/iOS app for offline use.

---


