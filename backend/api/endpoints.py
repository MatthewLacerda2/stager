from fastapi import APIRouter
from .v1 import scenes, chats, renders, objects

router = APIRouter()

router.include_router(scenes.router, prefix="/scenes", tags=["scenes"])
router.include_router(chats.router, prefix="/chats", tags=["chats"])
router.include_router(objects.router, prefix="/objects", tags=["objects"])
router.include_router(renders.router, prefix="/renders", tags=["renders"])
