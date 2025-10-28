from apkit.server import SubRouter

from . import activitypub, atproto

router = SubRouter()
router.include_router(activitypub.router)
router.include_router(atproto.router)