fn (tx: Sender<ShockMessage>){
    let context = zmq::Context::new();
    let socket = context.socket(PULL);
    socket.bind("tcp://127.0.0.1:5555");
    loop:
        let raw = socket.recv_byte().unwrap_or(continue);
        let msg = serde_json::from_slice::<ShockMessage>(&raw);
        
        match msg:
            Ok(m) => tx.send(m),
            err(e) => println!("Failed to parse JSON: {}", e)
}