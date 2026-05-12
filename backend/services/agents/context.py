"""
Thread-local context for injecting scene_id and db session into tool functions.

The chat endpoint sets these before invoking the Gemini agent loop.
Tool functions read them via get_scene_id() / get_db_session() without
polluting their signatures (which Gemini uses for schema inference).
"""
import asyncio
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession

_scene_id_var: ContextVar[str] = ContextVar("scene_id")
_db_var: ContextVar[AsyncSession] = ContextVar("db_session")


def set_scene_id(scene_id: str):
    _scene_id_var.set(scene_id)


def get_scene_id() -> str:
    return _scene_id_var.get()


def set_db_session(db: AsyncSession):
    _db_var.set(db)


def get_db_session() -> AsyncSession:
    return _db_var.get()


def run_async(coro):
    """Run an async coroutine from a sync tool function.

    Works whether or not an event loop is already running by reusing
    the current loop's thread-pool when inside an async context.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as pool:
        future = pool.submit(asyncio.run, coro)
        return future.result()
