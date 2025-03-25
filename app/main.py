from fastapi import FastAPI
from .database import engine
from . import model
from .routes import admin,admin_login,user_create
from .routes import user_login


from fastapi import APIRouter



model.Base.metadata.create_all(bind =engine)
app = FastAPI()

app.include_router(admin_login.router)
app.include_router(admin.router)
app.include_router(user_create.router)
app.include_router(user_login.router)


