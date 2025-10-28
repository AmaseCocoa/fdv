from typing import Annotated

from apkit.client.asyncio import ActivityPubClient
from apkit.models import Actor, OrderedCollection
from apkit.server import SubRouter
from async_lru import alru_cache
from fastapi import Query, Request

from endpoints.models import BadgeParams, JSONBadge

from .helpers import parse_account

router = SubRouter()


@alru_cache
@router.get("/statuses")
async def statuses(
    request: Request, query: Annotated[BadgeParams, Query()]
) -> JSONBadge:
    async with ActivityPubClient() as client:
        try:
            username, host = parse_account(query.account)
        except Exception:
            return JSONBadge(
                label="Error",
                message="Internal Server Error",
                color="red",
                isError=True,
                namedLogo=None,
                style="flat"
            )
        result = await client.actor.resolve(username, host)
        link = result.get("application/activity+json")
        if link:
            if isinstance(link, list):
                url = link[0].href
            else:
                url = link.href
            if not url:
                return JSONBadge(
                    label="Error",
                    message="Not Found",
                    color="red",
                    isError=True,
                    namedLogo=None,
                    style="flat",
                )
            async with client.get(
                url,
                headers={
                    "Accept": "application/activity+json",
                    "User-Agent": f"fediv ({str(request.url)})",
                },
            ) as resp:
                model = await resp.parse()
                if isinstance(model, Actor):
                    if isinstance(model.outbox, str):
                        async with client.get(
                            model.outbox,
                            headers={
                                "Accept": "application/activity+json",
                                "User-Agent": f"fediv ({str(request.url)})",
                            },
                        ) as outbox:
                            outbox_model = await outbox.parse()
                            if not isinstance(outbox_model, OrderedCollection):
                                return JSONBadge(
                                    label="Error",
                                    message="Not Found",
                                    color="red",
                                    isError=True,
                                    namedLogo=None,
                                    style="flat",
                                )
                    elif isinstance(model.outbox, OrderedCollection):
                        outbox_model = model.outbox
                    else:
                        return JSONBadge(
                            label="Error",
                            message="Not Found",
                            color="red",
                            isError=True,
                            namedLogo=None,
                            style="flat",
                        )
                    if isinstance(outbox_model.totalItems, int):
                        return JSONBadge(
                            label="Statuses",
                            message=f"{outbox_model.totalItems}",
                            color="FA007C",
                            isError=False,
                            namedLogo="activitypub",
                            style="flat",
                        )
        else:
            return JSONBadge(
                label="Error",
                message="Not Found",
                color="red",
                isError=True,
                namedLogo=None,
                style="flat",
            )
