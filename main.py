# main.py
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Cricket AI Coach – Multi-Model Edition",
    description="""
    5 Powerful Pose Engines in One API:
    • MediaPipe • YOLOv8 • Roboflow (Custom) • MMPose • PoseNet
    All return the exact same clean JSON format you love.
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include all pose detection routes
app.include_router(router)

@app.get("/")
async def home():
    return {
        "message": "Cricket AI Coach is LIVE!",
        "endpoints": [
            "/pose/yolo"
        ],
        "docs": "http://localhost:8000/docs"
    }

# This allows: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",           # ← main.py + app
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )