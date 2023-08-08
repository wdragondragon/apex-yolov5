def send(send_socket, byte_array, buffer_size=4096):
    send_socket.sendall(str(len(byte_array)).encode('utf-8'))
    ready = send_socket.recv(buffer_size)
    if ready == b'ready':
        send_socket.sendall(byte_array)


def recv(recv_socket, buffer_size=4096):
    data_length = recv_socket.recv(32)
    if not data_length:
        return None
    recv_socket.send(b'ready')
    data_length = int(data_length.decode('utf-8'))
    recv_data_count = 0
    recv_data = bytearray()
    while recv_data_count < data_length:
        if data_length - recv_data_count < buffer_size:
            data_temp = recv_socket.recv(data_length - recv_data_count)
        else:
            data_temp = recv_socket.recv(buffer_size)
        recv_data.extend(data_temp)
        recv_data_count += len(data_temp)
    return recv_data
