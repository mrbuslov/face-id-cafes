from src.face_id.views.video_stream import index, offer

routes = [
    {'path': '/', 'endpoint': index},
    {'path': '/offer', 'endpoint': offer, 'methods': ['post']}
]
