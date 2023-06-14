from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service

from . import router


@router.delete("/{id}/media")
def delete_photo(
    shanyrak_id: str,
    photo_name: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_result = svc.repository.delete_photo(shanyrak_id, jwt_data.user_id, photo_name)
    if delete_result.modified_count > 0:
        return Response(status_code=200)
    return Response(status_code=404)