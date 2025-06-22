from fastapi import FastAPI,Request
from .database import engine
from . import model
from .routes import admin,admin_login,user_create,dashboard
from .routes import user_login
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)



from fastapi import APIRouter



BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/new_index.html")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "new_index.html"))
@app.get("/new_adminlogin.html")
def admin_login2():
    return FileResponse(os.path.join(STATIC_DIR, "new_adminlogin.html"))
@app.get("/new_library.html")
def admin_login3():
    return FileResponse(os.path.join(STATIC_DIR, "new_library.html"))

@app.get("/new_register.html")
def admin_login4():
    return FileResponse(os.path.join(STATIC_DIR, "new_register.html"))

@app.get("/admin_dashboard.html")
def admin_login5():
    return FileResponse(os.path.join(STATIC_DIR, "admin_dashboard.html"))




app.include_router(admin_login.router)
app.include_router(admin.router)
app.include_router(user_create.router)
app.include_router(user_login.router)
app.include_router(dashboard.router)

