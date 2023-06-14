from typing import List
from fastapi import Depends, Response, UploadFile
from ..service import Service, get_service
from . import router


@router.post("/{id}/media")
def upload_photos(
    id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
):
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename, id)
        result.append(url)
    update_result = svc.repository.upload_photos(id, result)
    if update_result.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)