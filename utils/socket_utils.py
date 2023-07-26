incomplete_message = b''


def receive_data(socket):
    global incomplete_message

    # Variable to store received data
    data = b''
    complete_messages = []

    while True:
        # Receive data in chunks
        chunk = socket.recv(1024)
        if not chunk:
            # If no more data is received, the client disconnected
            raise ConnectionResetError

        data += chunk
        while b'\n' in data:
            # If we have a complete message (ending with '\n'), append it to the complete_messages list
            message, _, data = data.partition(b'\n')
            complete_message = incomplete_message + message
            complete_messages.append(complete_message.decode())
            incomplete_message = b''

        # Store any incomplete message for later completion
        incomplete_message = data

        # Check if we have received all complete messages, i.e., no more '\n' in the remaining data
        if b'\n' not in data:
            break

    return complete_messages
