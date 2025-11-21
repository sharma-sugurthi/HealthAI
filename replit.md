# HealthAI - Intelligent Healthcare Assistant

## Overview
HealthAI is a comprehensive web application built with Streamlit that serves as an intelligent healthcare assistant. The app leverages Google's Gemini Pro AI model to provide accurate, reliable, and context-aware medical assistance to users.

**Purpose:** Provide users with AI-powered health information, symptom analysis, treatment planning, and health tracking capabilities.

**Current State:** Fully functional MVP with all core features implemented.

## Recent Changes
- **2025-11-21:** Initial implementation of complete HealthAI application
  - User authentication system with bcrypt password hashing
  - AI-powered patient chat using Google Gemini Pro
  - Symptom checker with detailed analysis
  - Treatment plan generator and storage
  - Health analytics dashboard with Plotly visualizations
  - SQLite database with SQLAlchemy ORM for data persistence

## Core Features

### 1. User Authentication
- Secure registration and login system
- Password hashing using bcrypt
- Session management to keep users logged in
- User profile data: username, password, full name, age, gender

### 2. AI-Powered Patient Chat
- Real-time Q&A with Google Gemini Pro
- Context-aware responses for health-related queries
- Chat history persistence
- Empathetic and informative AI responses
- Medical disclaimers included in all responses

### 3. Symptom Checker
- Input symptoms and get AI analysis
- Possible conditions listed with likelihood
- Recommendations for when to seek immediate care
- Suggested next steps for users
- Results saved to chat history

### 4. Treatment Plan Generator
- Generate personalized treatment plans based on conditions
- Takes into account patient age and gender
- Includes lifestyle modifications, dietary recommendations, exercise suggestions
- Save and view treatment plans
- Treatment plan history with timestamps

### 5. Health Analytics Dashboard
- Track multiple health metrics:
  - Heart Rate (bpm)
  - Blood Pressure - Systolic/Diastolic (mmHg)
  - Blood Glucose (mg/dL)
  - Weight (kg)
  - Temperature (°F)
  - Oxygen Saturation (%)
- Interactive Plotly charts showing trends over time
- Statistics: latest, average, minimum, maximum values
- Data table view of all measurements
- Notes field for additional context

### 6. Database Persistence
- SQLite database with SQLAlchemy ORM
- Tables: users, chat_history, treatment_plans, health_metrics
- Automatic schema creation on first run
- Relationships properly defined between tables

### 7. User Interface
- Clean, intuitive Streamlit interface
- Sidebar navigation for easy feature access
- Responsive layout
- Medical disclaimer prominently displayed
- Professional healthcare-themed design

## Project Architecture

### File Structure
```
healthai/
├── app.py              # Main Streamlit application
├── db.py              # Database models and operations
├── gemini_api.py      # Gemini API integration
├── healthai.db        # SQLite database (created on first run)
├── replit.md          # This documentation file
└── .streamlit/
    └── config.toml    # Streamlit configuration
```

### Technology Stack
- **Frontend:** Streamlit (Python web framework)
- **AI Model:** Google Gemini Pro (via google-generativeai)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** bcrypt for password hashing
- **Visualization:** Plotly for interactive charts
- **Data Processing:** Pandas for data manipulation

### Database Schema

**Users Table:**
- id (Primary Key)
- username (Unique)
- password_hash
- full_name
- age
- gender
- created_at

**ChatHistory Table:**
- id (Primary Key)
- user_id (Foreign Key)
- message
- response
- timestamp

**TreatmentPlans Table:**
- id (Primary Key)
- user_id (Foreign Key)
- title
- condition
- plan_details
- created_at

**HealthMetrics Table:**
- id (Primary Key)
- user_id (Foreign Key)
- metric_type
- value
- unit
- notes
- recorded_at

## Environment Variables

### Required Secrets
- `GEMINI_API_KEY`: Google Gemini API key for AI functionality
  - Get your free key at: https://aistudio.google.com/app/apikey

### Optional Variables
- `SESSION_SECRET`: Used for session management (automatically configured)

## API Integration

### Gemini API Features
- **Model:** gemini-pro (text generation)
- **Safety Settings:** Configured to allow medical content while maintaining safety
- **Retry Logic:** 3 attempts with exponential backoff
- **Error Handling:** Graceful fallbacks with user-friendly error messages
- **Rate Limiting:** Built-in handling for API rate limits

### API Functions
1. `chat_with_patient()` - General health Q&A
2. `analyze_symptoms()` - Symptom analysis and condition suggestions
3. `generate_treatment_plan()` - Personalized treatment recommendations
4. `get_health_advice()` - General health information

## Security Considerations

### Implemented Security Measures
- Password hashing with bcrypt (salt rounds automatically managed)
- No hardcoded API keys (environment variables only)
- Session-based authentication
- SQL injection protection via SQLAlchemy ORM
- Input validation on all forms

### Medical Disclaimers
- Prominent disclaimer on all pages
- AI responses include reminders about professional medical advice
- Clear messaging that AI is not a substitute for doctors
- Encouragement to seek professional help for serious concerns

## User Workflow

1. **Registration/Login**
   - New users create account with personal information
   - Existing users log in with username/password
   - Session persists until logout

2. **Patient Chat**
   - Ask health-related questions
   - Receive AI-powered responses
   - Chat history automatically saved

3. **Symptom Checker**
   - Describe symptoms in detail
   - Receive analysis with possible conditions
   - Get recommendations for next steps

4. **Treatment Plans**
   - Generate plans for specific conditions
   - Save plans for future reference
   - View all saved plans with timestamps

5. **Health Analytics**
   - Record various health metrics
   - View trends over time with charts
   - Track progress with statistics

## Deployment

### Running Locally
```bash
streamlit run app.py --server.port 5000
```

### Replit Deployment
- Application automatically runs on port 5000
- Webview configured for browser access
- Environment variables managed in Replit Secrets

## Future Enhancements (Next Phase)

Planned features for future iterations:
1. PDF export for treatment plans and health reports
2. Advanced data visualization with trend comparisons
3. Medication reminder system with notifications
4. Health goal setting and progress tracking
5. Data export in multiple formats (CSV, JSON, PDF)
6. Integration with wearable devices
7. Multi-language support
8. Family account sharing options

## Testing Guidelines

### Manual Testing Checklist
- [ ] User registration with valid data
- [ ] User login with correct credentials
- [ ] Login failure with incorrect credentials
- [ ] Patient chat conversation flow
- [ ] Symptom checker analysis
- [ ] Treatment plan generation and saving
- [ ] Health metric recording
- [ ] Chart visualization rendering
- [ ] Session persistence across page changes
- [ ] Logout functionality

### Known Limitations
- AI responses depend on Gemini API availability
- Safety filters may occasionally block legitimate medical queries
- Chart performance may vary with large datasets (>1000 points)
- Single-user session (no concurrent multi-device support)

## Troubleshooting

### Common Issues

**"GEMINI_API_KEY not found"**
- Add your Gemini API key in Replit Secrets tab
- Key name must be exactly: GEMINI_API_KEY

**"Failed to initialize AI assistant"**
- Check API key is valid
- Verify internet connection
- Check Gemini API quota/limits

**Database errors**
- Delete healthai.db file to reset database
- Check file permissions in project directory

**Charts not displaying**
- Ensure plotly is installed
- Check browser console for JavaScript errors
- Try refreshing the page

## Support and Resources

- Google Gemini API Documentation: https://ai.google.dev/docs
- Streamlit Documentation: https://docs.streamlit.io
- SQLAlchemy Documentation: https://docs.sqlalchemy.org
- Plotly Documentation: https://plotly.com/python/

## License and Disclaimer

This application is for educational and informational purposes only. Always consult qualified healthcare professionals for medical advice, diagnosis, and treatment.
