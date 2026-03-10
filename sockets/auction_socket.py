from flask_socketio import join_room
from socketio_instance import socketio

@socketio.on("join_auction")

def join_auction(data):

    auction_id = data["auction_id"]

    join_room(f"auction_{auction_id}")