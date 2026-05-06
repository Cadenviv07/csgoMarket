import zmq

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.setsockopt(zmq.IMMEDIATE, 1)

def send_shock(asset: str, baseline: float, status: str = "SHOCK_DETECTED") -> None:
    socket.connect("tcp://127.0.0.1:5555")
    socket.send_string('{"asset": asset, "status":"SHOCK_DETECTED", "baseline": baseline}')
    
