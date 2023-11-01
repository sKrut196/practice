import socket
import sys
import os

# protocol_header()という関数は、サーバに送信されるファイルのヘッダ情報をフォーマットするために使用されます。このヘッダは、ファイル名の長さ（バイト）、JSONデータの長さ（バイト）、データの長さ（バイト）の3つの値で構成されます。これらの値は、to_bytes()メソッドを用いてバイナリに変換され、1つの64ビットバイナリに結合されます。
def protocol_header(filename_length, json_length, data_length):
    return filename_length.to_bytes(1, "big") + json_length.to_bytes(3,"big") + data_length.to_bytes(4,"big")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバが待ち受けているポートにソケットを接続します
server_address = input("Type in the server's address to connect to: ")
server_port = 9001

print('connecting to {}'.format(server_address, server_port))

try:
    # 接続後、サーバとクライアントが相互に読み書きができるようになります 
    sock.connect((server_address, server_port))
except socket.error as err:
    print(err)
    sys.exit(1)

while True:
    try:
        # messageを送信
        message = input("Input request with splitting calculator \":\" : ")
        message_bits = message.encode('utf-8')

        sock.send(message_bits)

    except Exception as e:
        print('ERROR: ' + str(e))
        break


print('closing socket')
sock.close()