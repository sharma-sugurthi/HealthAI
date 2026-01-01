# 🏥 HealthAI - Intelligent Healthcare Assistant

<div align="center">

![HealthAI Logo](https://img.shields.io/badge/HealthAI-v0.1.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

**An AI-powered healthcare assistant that provides intelligent health information, symptom analysis, treatment planning, and health tracking.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#%EF%B8%8F-medical-disclaimer)

---

## 🎯 Overview

HealthAI is an intelligent healthcare assistant that leverages advanced AI technology to provide users with:

- **AI-Powered Health Consultations** - Get instant answers to health-related questions
- **Symptom Analysis** - Describe your symptoms and receive possible condition insights
- **Treatment Planning** - Generate personalized wellness and treatment plans
- **Health Tracking** - Monitor vital health metrics over time with interactive visualizations

> **⚠️ Important:** HealthAI is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment.

---

## ✨ Features

### 🔐 User Authentication
- Secure registration and login system
- Password hashing with bcrypt
- Session-based authentication
- User profile management

### 💬 AI-Powered Patient Chat
- Real-time Q&A with xAI's Grok 4.1 Fast model
- Context-aware health information
- Persistent chat history
- Medical disclaimers included

### 🔍 Symptom Checker
- Detailed symptom analysis
- Possible condition suggestions with likelihood
- Recommendations for when to seek immediate care
- Suggested next steps

### 📋 Treatment Plan Generator
- Personalized treatment and wellness plans
- Age and gender-specific recommendations
- Lifestyle modifications and dietary advice
- Exercise suggestions
- Save and manage multiple treatment plans

### 📊 Health Analytics Dashboard
- Track multiple health metrics:
  - Heart Rate (bpm)
  - Blood Pressure (Systolic/Diastolic)
  - Blood Glucose (mg/dL)
  - Weight (kg)
  - Body Temperature (°F)
  - Oxygen Saturation (%)
- Interactive Plotly charts showing trends
- Statistical analysis (average, min, max)
- Data table view with timestamps
- Optional notes for each measurement

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11+** - Core programming language
- **Streamlit** - Web application framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (development)
- **bcrypt** - Password hashing
- **python-dotenv** - Environment variable management

### AI & APIs
- **OpenRouter** - AI API gateway
- **xAI Grok 4.1 Fast** - AI model (free, 2M context window)
- **OpenAI Python SDK** - API client library

### Data & Visualization
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts and graphs

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/sharma-sugurthi/HealthAI.git
cd HealthAI
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenRouter API key
# Get your free key at: https://openrouter.ai/keys
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required: OpenRouter API Key
OPENROUTER_API_KEY=your_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///healthai.db

# AI Model Settings
AI_MODEL=x-ai/grok-4.1-fast
AI_MAX_RETRIES=3
AI_RETRY_DELAY=2
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7

# Security Settings
SECRET_KEY=your-secret-key-here
BCRYPT_LOG_ROUNDS=12

# Session Settings
SESSION_TIMEOUT_MINUTES=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=healthai.log

# Environment
ENVIRONMENT=development
```

### Getting an OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/keys)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

The xAI Grok 4.1 Fast model is completely free with no usage limits!

---

## 🚀 Usage

### First Time Setup

1. **Register an Account**
   - Click on the "Register" tab
   - Fill in your details (username, password, full name, age, gender)
   - Click "Register"

2. **Login**
   - Enter your username and password
   - Click "Login"

### Using the Features

#### Patient Chat
- Navigate to "💬 Patient Chat"
- Type your health-related question
- Receive AI-powered responses
- Chat history is automatically saved

#### Symptom Checker
- Navigate to "🔍 Symptom Checker"
- Describe your symptoms in detail
- Click "Analyze Symptoms"
- Review possible conditions and recommendations

#### Treatment Plans
- Navigate to "📋 Treatment Plans"
- Enter a condition or health concern
- Click "Generate Treatment Plan"
- Save the plan for future reference
- View all saved plans in the "View Saved Plans" tab

#### Health Analytics
- Navigate to "📊 Health Analytics"
- **Add Health Data** tab:
  - Select metric type
  - Enter value
  - Add optional notes
  - Click "Record Metric"
- **View Analytics** tab:
  - Select metric to visualize
  - View interactive charts
  - See statistics and trends
  - Review measurement history

---

## 📁 Project Structure

```
HealthAI/
├── app.py                 # Main Streamlit application
├── ai_client.py          # AI API client (OpenRouter/Grok)
├── db.py                 # Database models and operations
├── config.py             # Configuration management
├── validation.py         # Input validation utilities
├── .env                  # Environment variables (not in git)
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
├── pyproject.toml       # Project dependencies
├── requirements.txt     # Pip requirements (generated)
├── healthai.db          # SQLite database (created on first run)
├── README.md            # This file
└── .streamlit/
    └── config.toml      # Streamlit configuration
```

---

## 👨‍💻 Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with debug mode
streamlit run app.py --logger.level=debug
```

### Code Quality Tools

```bash
# Format code with Black
black .

# Lint with Flake8
flake8 .

# Sort imports
isort .

# Type checking
mypy .
```

### Database Management

```bash
# Reset database (WARNING: Deletes all data)
rm healthai.db

# The database will be recreated on next app run
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_validation.py
```

---

## 🌐 Deployment

### Docker Deployment (Coming Soon)

```bash
# Build Docker image
docker build -t healthai .

# Run container
docker run -p 8501:8501 healthai
```

### Cloud Deployment

The application can be deployed to:
- **Streamlit Cloud** (Recommended for Streamlit apps)
- **Heroku**
- **AWS EC2**
- **Google Cloud Run**
- **Azure App Service**

Deployment guides coming soon!

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚕️ Medical Disclaimer

**IMPORTANT: READ CAREFULLY**

HealthAI is an AI-powered informational tool and is **NOT** a substitute for professional medical advice, diagnosis, or treatment. 

- Always seek the advice of your physician or qualified healthcare provider with any questions you may have regarding a medical condition
- Never disregard professional medical advice or delay seeking it because of information provided by HealthAI
- If you think you may have a medical emergency, call your doctor or emergency services immediately
- HealthAI does not recommend or endorse any specific tests, physicians, products, procedures, opinions, or other information

The information provided by HealthAI is for educational and informational purposes only.

---

## 📞 Support

For questions, issues, or suggestions:

- **GitHub Issues**: [Report a bug](https://github.com/sharma-sugurthi/HealthAI/issues)
- **Email**: [Contact maintainer](mailto:your-email@example.com)

---

## 🙏 Acknowledgments

- **OpenRouter** for providing free access to AI models
- **xAI** for the Grok 4.1 Fast model
- **Streamlit** for the amazing web framework
- All contributors and users of HealthAI

---

<div align="center">

Made with ❤️ by [Sharma Sugurthi](https://github.com/sharma-sugurthi)

⭐ Star this repo if you find it helpful!

</div>
