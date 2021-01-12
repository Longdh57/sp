import logging
import sys
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

sys.path = ['', '..'] + sys.path[1:]
from app.db.base_class import engine
from app.core.config import settings
from app.api.api import router
from app.models.base_model import Base
from app.utils.exception_handler import SaleServiceException, sale_service_exception_handler, http_exception_handler, \
    validation_exception_handler, fastapi_error_handler

logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs"
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router, prefix=settings.API_PREFIX)
    application.add_exception_handler(SaleServiceException, sale_service_exception_handler)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    application.add_exception_handler(Exception, fastapi_error_handler)

    return application


app = get_application()
app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
