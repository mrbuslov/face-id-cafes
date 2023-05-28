from src.face_id.views.video_stream import (
    index,
    offer,
    data_stream,
    clear_peer_connections,
    screenshot
)

routes = [
    {'path': '/', 'endpoint': index},
    {'path': '/offer', 'endpoint': offer, 'methods': ['post']},
    {'path': '/screenshot', 'endpoint': screenshot, 'methods': ['post']}
]

web_socket_routes = [
    {'path': '/video', 'route': data_stream}
]

events = [
    {"event_type": "shutdown", "func": clear_peer_connections}
]
