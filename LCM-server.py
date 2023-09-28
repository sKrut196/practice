import socket
import os
from faker import Faker

fake = Faker()

# socketの作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

server_address = '/lcm_socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

sock.bind(server_address)
print("Starting up on {}".format(server_address))

while True:
    # データを受信するまで待機
    print("Waiting to receive message")
    data, address = sock.recvfrom(4096)
    print("Received {} bytes from {}".format(len(data), address))
    print(data)

    # データを受信したあと送信し返す
    if data:
        # 返信メッセージとしてフェイクアドレスを送信
        return_message = fake.address().encode()
        sent = sock.sendto(return_message, address)
        print("Sent {} bytes data back to {}".format(sent, address))