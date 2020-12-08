from fastapi import APIRouter

from app.schema.base import SchemaBase

router = APIRouter()


@router.get("", response_model=SchemaBase)
async def get():
    return {"message": "Health check success"}
