from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service

from . import router


@router.delete("/{id}/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    delete_result = svc.repository.delete_comment(jwt_data.user_id, shanyrak_id, comment_id)
    if delete_result.modified_count > 0:
        return Response(status_code=200)
    return Response(status_code=404)