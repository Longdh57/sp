from fastapi import APIRouter

from app.api.api_v1 import api_healthcheck, api_staff, api_user, api_login

router = APIRouter()
router.include_router(api_login.router, tags=["login"])
router.include_router(api_healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")
router.include_router(api_staff.router, tags=["staff"], prefix="/staffs")
router.include_router(api_user.router, tags=["user"], prefix="/users")
