import socket
import os

# ソケットの作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

server_address = '/lcm_socket_file'
address = '/lcm_client_socket_file'

# addressで指定したパスが紐付けられていたら解除
try:
    os.unlink(address)
except:
    pass

sock.bind(address)

while True:
    message = input('[client input]: ')

    # 'exit'と入力があったら終了
    if message == "exit":
        break

    # serverにnessageを送信
    sent = sock.sendto(message.encode(), server_address)
    print("Sending {!r}".format(message))

    # 受信
    print("Waiting for receive")
    data, server = sock.recvfrom(4096)

    print("Received {!r}".format(data))

print("Closing socket")
sock.close()

