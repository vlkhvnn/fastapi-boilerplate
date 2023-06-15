from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.shanyraks.service import Service as shanService
from app.shanyraks.service import get_service as shan_get_service
from . import router
from app.utils import AppModel
from typing import List, Any
from pydantic import Field


class Shanyrak(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    media: List[str]
    location: dict[str, str]


class GetFavouritesResponse(AppModel):
    shanyraks : List[Shanyrak]


@router.get("/users/favorites/shanyraks/{id}", response_model=GetFavouritesResponse)
def get_favourites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    svc2: shanService = Depends(shan_get_service)
) -> dict[str, str]:
    response = svc.repository.get_favourites(jwt_data.user_id)
    arr = []
    for shanyrak_id in response:
        shanyrak = svc2.repository.get_media(shanyrak_id)
        shanyrak["location"] = svc2.here_service.get_coordinates(shanyrak["address"])
        arr.append(shanyrak)
    if arr is None:
        return Response(status_code=404)
    return GetFavouritesResponse(shanyraks=arr)