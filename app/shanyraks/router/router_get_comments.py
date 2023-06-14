from typing import Any, List
from fastapi import Depends, Response
from pydantic import Field
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class Comment(AppModel):
    id: Any = Field(alias="_id")
    content: str
    created_at: str
    author_id: Any


class GetCommentsResponse(AppModel):
    comments : List[Comment]


@router.get("/{id}/comments", response_model=GetCommentsResponse)
def get_comments(
    shanyrak_id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    comments = svc.repository.get_comments(shanyrak_id)
    if comments is None:
        return Response(status_code=404)
    return GetCommentsResponse(**comments)