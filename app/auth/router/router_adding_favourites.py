from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.post("/users/favorites/shanyraks/{id}")
def add_to_favourites(
    shanyrak_id : str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    response = svc.repository.add_to_favourites(jwt_data.user_id, shanyrak_id)
    if response is None:
        return Response(status_code=404)
    return Response(status_code=200)