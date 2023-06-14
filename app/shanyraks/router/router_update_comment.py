from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class UpdateCommentRequest(AppModel):
    shanyrak_id: str
    comment_id: str
    content: str


@router.patch("/{id}/comments/{comment_id}")
def update_comment(
    input: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    update_result = svc.repository.update_comment(input.shanyrak_id, input.comment_id, input.content)
    if update_result.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)