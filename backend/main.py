from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router

app = FastAPI(title="PKT Backend")

# CORS middleware (must be added after app creation)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "PKT Backend Running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "PKT backend"
    }