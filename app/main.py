from fastapi import FastAPI,Request
from .database import engine
from . import model
from .routes import admin,admin_login,user_create,dashboard
from .routes import user_login
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)



from fastapi import APIRouter








app.include_router(admin_login.router)
app.include_router(admin.router)
app.include_router(user_create.router)
app.include_router(user_login.router)
app.include_router(dashboard.router)

