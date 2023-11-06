import socket
import os
import asyncio
import threading
from pathlib import Path

class ChatClient:
    def __init__(self,address,portNum,connection):
        self.address = address
        self.portNum = portNum
        self.mySocket = connection
        self.myRoom = None

    def getClientName(self):
        return str(self.address) + " " + str(self.portNum)
    
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
        key = str(chatClient.address) + " " + str(chatClient.portNum)

        if key not in self.chatClientMap:
            self.chatClientMap[key] = chatClient
        else:
            print("client " + key + " already exists in the room " + self.roomName)

    def deleteClient(self, chatClient):
        key = str(chatClient.address) + " " + str(chatClient.portNum)

        if key not in self.chatClientMap:
            print("This room does not contain the client " + key + ".")
        else:
            print("delete the client " + key + " from the room " + self.roomName)
            self.chatClientMap.pop(key)

class ChatRoomManager:
    def __init__(self) -> None:
        self.chatRoomMap = {}

    def createChatRoom(self,roomName):
        if roomName not in self.chatRoomMap:
            self.chatRoomMap[roomName] = ChatRoom(roomName)
        else:
            print("roomName " + roomName + "already exists.")

    def moveClient(self,cc,destRoomName):
        #ccが元居たルームからccを削除
        if cc.myRoom is not None:
            cc.myRoom.deleteClient(cc)

        #行先のルームにccを追加
        self.chatRoomMap[destRoomName].addClient(cc)
        cc.joinRoom(self.chatRoomMap[destRoomName])

crm = ChatRoomManager()
clientsMap = {}

async def handleClient(reader,writer):
    while True:
        try:
            client_address = writer.get_extra_info('peername')
            print(client_address)

            print("waiting for message.")
            data = await reader.read(100)
            if not data:
                break

            request = data.decode('utf-8')
            print(request)
            result = request.split(":")

            if writer.get_extra_info('peername') not in clientsMap:
                clientsMap[client_address] = ChatClient(client_address[0],client_address[1],writer)

            command = result[0]

            # ルームの移動
            if command == "join":
                roomName = result[1]
                if roomName not in crm.chatRoomMap:
                    print("chatRoom "+ roomName + " does not exist.")
                else:
                    crm.moveClient(clientsMap[client_address],roomName)

            # ルームの作成
            elif command == "create":
                roomName = result[1]

                if roomName not in crm.chatRoomMap:
                    crm.createChatRoom(roomName)
                    crm.moveClient(clientsMap[client_address],roomName)
                else:
                    print("the room " + roomName + " already exists.")

            #メッセージの送信
            elif command == "send":
                messageSize = result[1]
                message = result[2]

                #同じルームroomNameに入っているすべてのクライアントにメッセージを送信
                for currentClient in clientsMap[client_address].myRoom.chatClientMap.values():
                    if currentClient != clientsMap[client_address]:
                        sendData = "message from " + clientsMap[client_address].getClientName() + ": " + message + "\n"
                        sendData += "message size : " + messageSize
                        sendData = sendData.encode('utf-8')
                        currentClient.mySocket.write(sendData)
                        await currentClient.mySocket.drain()

            # 上記以外のコマンドが入力されても何も起きない
            else:
                print("invalid command.")

            for key, room in crm.chatRoomMap.items():
                print("this room : " + key)
                print("contains...")
                for ckey in room.chatClientMap:
                    print(ckey)
                print("")

            for key, client in clientsMap.items():
                print("client: " + client.getClientName())
                print("-room : " + (client.myRoom.roomName if client.myRoom is not None else "None"))
                print("")


        except Exception as e:
            print('Error: ' + str(e))
            break

    clientsMap.pop(client_address)
    writer.close()
    

async def main():
    # サーバーソケットを作成
    server = await asyncio.start_server(handleClient, '0.0.0.0', 9001)
    addr = server.sockets[0].getsockname()

    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
