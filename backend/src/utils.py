import asyncio
from typing import Set, List

from aiortc import RTCPeerConnection
from fastapi import FastAPI, Request

import traceback


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


def update_http_routes(app: FastAPI, routes: List[dict]) -> FastAPI:
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


def update_websocket_routes(app: FastAPI, routes: List[dict]) -> FastAPI:
    """
    Add routes to the FastAPI application.
    Args:
        app: The FastAPI application.
        routes: The routes to add ex: {"path": "/ws"}.
    Returns:
        None
    """
    for route in routes:
        app.add_websocket_route(**route)
    return app


def update_events(app: FastAPI, events: List[dict]) -> FastAPI:
    """
    Add events to the FastAPI application.
    Args:
        app: The FastAPI application.
        events: The events to add ex: {"event": "shutdown", "function": clear_peer_connections}.
    Returns:
        None
    """
    for event in events:
        app.add_event_handler(**event)
    return app


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(traceback.format_exc())
        raise e