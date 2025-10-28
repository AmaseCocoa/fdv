from fastapi import APIRouter

from . import followers, following, posts

router = APIRouter(prefix="/api/atproto")
router.include_router(posts.router)
router.include_router(following.router)
router.include_router(followers.router)
