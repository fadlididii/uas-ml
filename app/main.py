from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.database import create_tables, close_db_connection
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.posts.router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_tables()
    yield
    # Shutdown
    await close_db_connection()


app = FastAPI(
    title="FastAPI Backend",
    description="Professional FastAPI backend with modular architecture",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"])


# HTML Template Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/about")
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/welcome")
async def welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.get("/preferences")
async def preferences_page(request: Request):
    return templates.TemplateResponse("preferences.html", {"request": request})


# API Routes
@app.get("/api")
async def api_root():
    return {"message": "Welcome to FastAPI Backend API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)