
def recv_complete_message(socket):
    # Receive data until a complete message is received
    data = b""
    while True:
        chunk = socket.recv(1024)
        if not chunk:
            break
        data += chunk
        message = data.decode()
        return message
    return None