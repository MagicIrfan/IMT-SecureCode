
def recv_complete_message(sock):
    # Receive data until a complete message is received
    data = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
        try:
            message = data.decode()
            return message
        except UnicodeDecodeError:
            # Incomplete message, continue receiving
            continue
    return None
