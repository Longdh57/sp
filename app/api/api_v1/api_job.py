from io import BytesIO

from fastapi import APIRouter, File, UploadFile

from app.utils.minio_handler import MinioHandler

router = APIRouter()


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    data_file = MinioHandler().get_instance().put_object(
        file_data=BytesIO(await file.read()),
        file_name=file.filename,
        content_type=file.content_type
    )
    return {"data_file": data_file}
