from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes import auth_routes, scan_routes, risk_routes

app = FastAPI(
    title="AI-Powered Personal Digital Safety Assistant",
    description="Backend API for scam and phishing detection across multiple platforms",
    version="1.0.0"
)

# CORS middleware to allow frontend connections
# Get frontend URLs from environment variables
frontend_local = os.getenv("FRONTEND_URL_LOCAL", "http://localhost:3000")
frontend_android = os.getenv("FRONTEND_URL_ANDROID", "http://localhost:3001")
frontend_extension = os.getenv("FRONTEND_URL_EXTENSION", "chrome-extension://*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_local, frontend_android, frontend_extension],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(scan_routes.router)
app.include_router(risk_routes.router)

@app.get("/")
async def root():
    return {"message": "AI-Powered Personal Digital Safety Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Initialize database
@app.on_event("startup")
async def startup_event():
    from utils.database import init_db
    success = init_db()
    if success:
        print("Database initialized successfully")
    else:
        print("Failed to initialize database")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)