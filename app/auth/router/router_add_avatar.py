from fastapi import Depends, Response, UploadFile
from ..service import Service, get_service
from . import router
from app.shanyraks.service import Service as shanService
from app.shanyraks.service import get_service as shan_get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


@router.post("/{id}/media")
def add_avatar(
    file: UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    svc2: shanService = Depends(shan_get_service)
):
    url = svc2.s3_service.upload_file(file.file, file.filename, id)
    update_result = svc.repository.upload_avatar(jwt_data.user_id, url)
    if update_result.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)