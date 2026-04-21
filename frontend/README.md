# HealthAI React Frontend

Modern React + Vite frontend for the HealthAI backend API.

## Features
- Professional chat workspace
- Embedded symptom analyzer and treatment draft tools
- Health metrics dashboard
- Authentication and profile views

## Setup
1. Install dependencies:
   - `npm install`
2. Configure environment:
   - Create `.env` with `VITE_API_BASE_URL=http://localhost:8000/api/v1`
3. Run locally:
   - `npm run dev`

## Notes
- The backend API is expected at `http://localhost:8000`.
- Authentication uses JWT tokens returned by the backend.
- This is the primary frontend for HealthAI.