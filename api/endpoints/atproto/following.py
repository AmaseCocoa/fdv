from typing import Annotated

from atproto.exceptions import AtProtocolError
from fastapi import APIRouter, Query, Request

from endpoints.models import BadgeParams, JSONBadge

from .profile import get_profile

router = APIRouter()


@router.get("/following")
async def following(
    request: Request, query: Annotated[BadgeParams, Query()]
) -> JSONBadge:
    try:
        profile = await get_profile(query.account)
    except AtProtocolError:
        return JSONBadge(
            label="Error",
            message="Internal Server Error",
            color="red",
            isError=True,
            namedLogo=None,
            style="flat",
        )
    return JSONBadge(
        label="Follows",
        message=f"{profile.follows_count}",
        color="1185FE",
        isError=False,
        namedLogo="bluesky",
        style="flat",
    )
