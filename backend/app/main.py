from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import Base,engine
from .exceptions.app_exception import AppException
from .exceptions.exception_handler import app_exception_handler,validation_exception_handler
from .models import category,user,supplier,product,inventory,order,customer,logistics
from .routes import category,product,user,supplier,inventory,order,customer,logistics,dashboard,report

Base.metadata.create_all(bind=engine)
app=FastAPI(title="Inventory Management API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.add_exception_handler(AppException,app_exception_handler)
app.add_exception_handler(RequestValidationError,validation_exception_handler)
for r in [user.router,category.router,product.router,supplier.router,inventory.router,order.router,customer.router,logistics.router,dashboard.router,report.router]: app.include_router(r,prefix="/api")
@app.get("/")
def root(): return {"success":True,"message":"Inventory API running"}
@app.get("/health")
def health(): return {"success":True,"message":"API healthy"}
