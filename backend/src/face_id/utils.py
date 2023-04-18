import asyncio
from typing import Set, List

from aiortc import RTCPeerConnection
from fastapi import FastAPI


async def clear_peer_connections(pcs: Set[RTCPeerConnection]) -> None:
    """
    Close all peer connections and clear the set.
    Args:
        pcs: The set of peer connections to close.
    Returns:
        None
    """
    coroutines = [pc.close() for pc in pcs]
    await asyncio.gather(*coroutines)
    pcs.clear()


def update_routes(app: FastAPI, routes: List[dict]) -> FastAPI:
    """
    Add routes to the FastAPI application.
    Args:
        app: The FastAPI application.
        routes: The routes to add ex: {"path": "/", "methods": ["GET"]}.
    Returns:
        None
    """
    for route in routes:
        app.add_api_route(**route)
    return app
