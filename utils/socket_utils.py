def receive_data(socket):
    # Variable to store received data
    data = b''
    while True:
        # Receive data in chunks
        chunk = socket.recv(1024)
        if not chunk:
            # If the chunk is empty, the client has closed the connection
            return ''

        data += chunk
        if b'\n' in data:
            # If we have a complete message (ending with '\n'), return it
            message, _, data = data.partition(b'\n')
            return message.decode('utf-8').strip()
