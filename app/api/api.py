from fastapi import APIRouter

from app.api.api_v1.healthcheck import api_healthcheck

router = APIRouter()
router.include_router(api_healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")