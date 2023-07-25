# Read data from the client and return all complete messages as a single string
def receive_data(socket):
    # Variable to store received data
    data = b''
    message_full = ''

    while True:
        # Receive data in chunks
        chunk = socket.recv(1024)
        if not chunk:
            # If no more data is received, the client disconnected
            raise ConnectionResetError

        data += chunk
        while b'\n' in data:
            # If we have a complete message (ending with '\n'), append it to the full message
            message, _, data = data.partition(b'\n')
            message_full += message.decode()

        # Check if we have received all messages, i.e., no more '\n' in the remaining data
        if b'\n' not in data:
            break

    return message_full.strip()
