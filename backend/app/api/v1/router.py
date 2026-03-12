from fastapi import APIRouter
from app.api.router_loader import load_routers

api_router = APIRouter()

routers = load_routers("app.api.routers")

api_router.include_router(routers)