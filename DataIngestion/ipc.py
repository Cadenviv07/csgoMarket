import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.setsockopt(zmq.IMMEDIATE, 1)
socket.connect("tcp://127.0.0.1:5555")

def send_shock(asset: str, baseline: float, status: str = "SHOCK_DETECTED") -> None:
    payload =({
        "asset": asset,
        "baseline": baseline,
        "status": status
    })
    socket.send_string(json.dumps(payload))
