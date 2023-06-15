from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.delete("/users/favorites/shanyraks/{id}")
def delete_favourite(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_result = svc.repository.delete_favourite(shanyrak_id, jwt_data.user_id)
    if delete_result.modified_count > 0:
        return Response(status_code=200)
    return Response(status_code=404)