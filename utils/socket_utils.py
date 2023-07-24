# Read data from client and return when newline is received
def receive_data(socket):
    # Variable to store received data
    data = b''
    while True:
        # Receive data in chunks
        chunk = socket.recv(1024)
        data += chunk
        if b'\n' in data:
            # If we have a complete message (ending with '\n'), return it
            message, _, data = data.partition(b'\n')
            return message.decode('utf-8').strip()
