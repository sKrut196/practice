import socket
import os
from pathlib import Path

class ChatClient:
    def __init__(self,address,portNum):
        self.address = address
        self.portNum = portNum

    def joinRoom(self, chatRoom):
        self.myRoom = chatRoom

    def exitRoom(self):
        if self.myRoom is not None:
            self.myRoom = None
        else:
            print("no chatRoom.")

        
class ChatRoom:
    def __init__(self,roomName) -> None:
        self.roomName = roomName
        self.users = []
        self.chatClientMap = {}
        self.roomSize = 5

    def addClient(self, chatClient):
        key = str(chatClient.address) + str(chatClient.portNum)

        if key not in self.chatClientMap:
            self.chatClientMap[key] = chatClient
        else:
            print("client " + key + " already exists in the room " + self.roomName)

class ChatRoomManager:
    def __init__(self) -> None:
        self.chatRoomMap = {}

    def createChatRoom(self,roomName):
        if roomName not in self.chatRoomMap:
            self.chatRoomMap[roomName] = ChatRoom(roomName)
        else:
            print("roomName " + roomName + "already exists.")


    

# まず、必要なモジュールをインポートし、ソケットオブジェクトを作成して、アドレスファミリ（AF_INET）とソケットタイプ（SOCK_STREAM）を指定します。サーバのアドレスは、任意のIPアドレスからの接続を受け入れるアドレスである0.0.0.0に設定し、サーバのポートは9001に設定されています。
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '0.0.0.0'
server_port = 9001

# 次に、現在の作業ディレクトリに「temp」という名前のフォルダが存在するかどうかをチェックします。存在しない場合は、os.makedirs() 関数を使用してフォルダを作成します。このフォルダは、クライアントから受信したファイルを格納するために使用されます。
dpath = 'temp'
if not os.path.exists(dpath):
    os.makedirs(dpath)

print('Starting up on {} port {}'.format(server_address, server_port))

# 次に、サーバは bind()関数を使用して、ソケットをサーバのアドレスとポートに紐付けします。その後、listen()関数を呼び出すことで、サーバは着信接続の待ち受けを開始します。サーバは一度に最大1つの接続を受け入れることができます。
sock.bind((server_address, server_port))

sock.listen(1)

crm = ChatRoomManager()

connection, client_address = sock.accept()
print('connection from', client_address)

while True:
    try:
        print("waiting for message.")
        request = connection.recv(4096).decode('utf-8')
        print(request)
        result = request.split(":")

        if len(result) == 2:
            roomName = result[0]
            command = result[1]

            cc = ChatClient(client_address[0],client_address[1])

            if command == "join":
                crm.chatRoomMap[roomName].addClient(cc)
                cc.joinRoom(crm.chatRoomMap[roomName])
            elif command == "create":
                crm.createChatRoom(roomName)
                crm.chatRoomMap[roomName].addClient(cc)
                cc.joinRoom(crm.chatRoomMap[roomName])

        for key, room in crm.chatRoomMap.items():
            print("this room : " + key)
            print("contains...")
            for ckey, cc in room.chatClientMap.items():
                print(ckey)


    except Exception as e:
        print('Error: ' + str(e))
        break

print("Closing current connection")
connection.close()