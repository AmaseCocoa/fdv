from apkit.server import SubRouter

from . import followers, following, statuses

router = SubRouter(prefix="/api/activitypub")
router.include_router(statuses.router)
router.include_router(following.router)
router.include_router(followers.router)
