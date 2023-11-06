import asyncio

async def sendMessage(reader,writer):
    while True:
        try:
            # messageを送信
            command = await asyncio.to_thread(input, "Input command : ")

            if command == "join" or command == "create":
                roomName = await asyncio.to_thread(input, "Input roomName : ")
                sendData = command + ":" + roomName
            elif command == "send":
                message = await asyncio.to_thread(input, "Input message : ")
                sendData = command + ":" + str(len(message)) + ":" + message

            sendData_bits = sendData.encode('utf-8')

            writer.write(sendData_bits)
            await writer.drain()

        except Exception as e:
            print('ERROR: ' + str(e))
            break

async def recvMessage(reader,writer):
    while True:
        try:
            recvData = await reader.read(4096)
            if not recvData:
                break
            print(recvData.decode('utf-8'))
        except Exception as e:
            print('ERROR: ' + str(e))
            break


async def main():
    global server_address, server_port
    server_address = "localhost"
    server_port = 9001
    print('connecting to {}:{}'.format(server_address, server_port))

    reader, writer = await asyncio.open_connection(server_address,server_port)
    send_task = asyncio.create_task(sendMessage(reader,writer))
    recv_task = asyncio.create_task(recvMessage(reader,writer))

    await asyncio.gather(send_task, recv_task)
    writer.close()


if __name__ == "__main__":
    asyncio.run(main())