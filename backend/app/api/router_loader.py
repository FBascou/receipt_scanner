import pkgutil
import importlib
from fastapi import APIRouter

def load_routers(package_name: str) -> APIRouter:
    api_router = APIRouter()

    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")

        if hasattr(module, "router"):
            api_router.include_router(module.router)

    return api_router