from fastapi import APIRouter

from app.api.api_v1 import api_healthcheck, staff

router = APIRouter()
router.include_router(api_healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")
router.include_router(staff.router, tags=["staff"], prefix="/staffs")
