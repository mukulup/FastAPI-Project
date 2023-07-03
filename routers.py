from fastapi import APIRouter

from app import views as app_view

router = APIRouter(prefix='/api/v1')

router.include_router(app_view.router, prefix='/app')