from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.database import create_tables, close_db_connection
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.posts.router import router as posts_router
from app.preferences.router import router as preferences_router
from app.exceptions import (
    ConflictError,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
    InternalServerError
)


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

# Exception handlers
@app.exception_handler(ConflictError)
async def conflict_exception_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "success": False}
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "success": False}
    )

@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "success": False}
    )

@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "success": False}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc),
            "success": False
        }
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
app.include_router(preferences_router, prefix="/preferences", tags=["Preferences"])


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

@app.get("/recommendations")
async def recommendations_page(request: Request):
    return templates.TemplateResponse("recommendations.html", {"request": request})

@app.get("/profile")
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/edit-profile")
async def edit_profile_page(request: Request):
    return templates.TemplateResponse("edit-profile.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


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