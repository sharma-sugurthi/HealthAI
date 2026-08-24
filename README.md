# HealthAI - Intelligent Healthcare Assistant

An enterprise-grade, API-first healthcare platform that provides AI-driven medical context analysis, symptom evaluation, and personalized treatment plan generation. 

Built with scalability, security, and medical data integrity in mind, HealthAI leverages FastAPI for high-performance backend routing, PostgreSQL for robust data persistence, and React (Vite) for a responsive frontend client.

## System Architecture

HealthAI is designed as a decoupled, multi-tier system:

- **Core API Layer**: FastAPI-driven REST endpoints with strict validation, rate limiting (`slowapi`), and structured JSON responses.
- **Domain Service Layer**: Abstracted business logic (e.g., `EnhancedChatService`, `MedicalContextService`) orchestrating AI interactions and database transactions.
- **Data Persistence**: SQLAlchemy ORM backed by PostgreSQL (in production) or SQLite (in development/testing), managed through an abstract repository pattern.
- **AI Integration**: Pluggable AI client with robust error handling, structured prompt building, and fallback strategies, securely interacting with external models.

## Technical Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0, Uvicorn
- **Frontend**: React, Vite
- **Database**: PostgreSQL / SQLite
- **Infrastructure**: Docker, Docker Compose
- **Quality Assurance**: Pytest, Black, Flake8, isort, Mypy

## Core Capabilities

- **Context-Aware Medical AI**: The integration provides deep contextual awareness, utilizing the patient's comprehensive medical history, existing medications, and allergies to inform all AI interactions.
- **Symptom Triage**: Deterministic evaluation of symptoms against known critical indicators, prioritizing emergency detection.
- **Dynamic Treatment Plans**: Generation of nuanced treatment guidance that inherently respects the patient's prior medical conditions and physiological metrics.

## Getting Started

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed environment setup, Docker orchestration, and local development workflows.

See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, test suite execution, and pull request guidelines.

## Security & Compliance

> **Disclaimer**: This software is intended for informational and triage purposes only. It is not a substitute for professional medical diagnosis or emergency care.

- **Data Privacy**: Medical records are isolated via user ID scoping at the repository level.
- **Authentication**: JWT-based stateless authentication utilizing `python-jose` and `bcrypt` hashing.
- **Rate Limiting**: IP-based rate limiting on sensitive endpoints to prevent abuse.
