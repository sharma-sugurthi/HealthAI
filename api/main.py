"""
HealthAI FastAPI Application.
Main API entry point with all routers and middleware.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.routers import auth, chat, health, treatment
from config import config
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="HealthAI API",
    description="Intelligent Healthcare Assistant API powered by AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router, prefix=f"{config.API_PREFIX}/auth", tags=["Authentication"])
app.include_router(chat.router, prefix=f"{config.API_PREFIX}/chat", tags=["Chat"])
app.include_router(health.router, prefix=f"{config.API_PREFIX}/health", tags=["Health Metrics"])
app.include_router(
    treatment.router, prefix=f"{config.API_PREFIX}/treatment", tags=["Treatment Plans"]
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to HealthAI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    try:
        # Check database connection
        from backend.utils.database import get_db_manager

        db_manager = get_db_manager()
        session = db_manager.get_session()
        session.execute("SELECT 1")
        session.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"

    # Check AI API (optional - can be slow)
    ai_status = "healthy" if config.OPENROUTER_API_KEY else "not_configured"

    overall_status = "healthy" if db_status == "healthy" else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "ai_service": ai_status,
        "version": "1.0.0",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.is_development(),
        log_level=config.LOG_LEVEL.lower(),
    )
