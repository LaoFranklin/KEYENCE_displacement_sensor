import socket
import config
import datetime
from time import sleep

def getTime():
    return datetime.datetime.now().strftime(f'%Y-%m-%d %H:%M:%S.%f')

def tcp():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = config.keyence_ip
    server_port = config.keyence_port
    tcp_socket.connect((server_ip, server_port))

    while True:
        if send_msg(tcp_socket) == 0:
            break
        recv_msg(tcp_socket)
        sleep(0.005)

    tcp_socket.close()

def send_msg(tcp_socket):
    # send_data = input()
    send_data = "M0"
    if send_data == "exit":
        return 0

    send_data += "\r\n"
    tcp_socket.send(send_data.encode("utf-8"))

    return send_data

def recv_msg(tcp_socket):
    recv_data = tcp_socket.recv(1024)
    msg = recv_data.decode("utf-8").replace("\r\n", "")
    if msg.find(",") != -1:
        # print(msg)
        msg_status = msg.split(",")[1]
    else:
        return
    try:
        # print(f'[{msg}]{config.command[msg_status]}')
        data = msg_status[0:]

        write_msg = ""+getTime()+"\t"+data
        print(write_msg)

        write_file(write_msg)
    except KeyError as res:
        print(f'[{msg}]')

def write_file(data):
    file_path = "d:\\KEYENCE_20210225\\Data\\T3_Displacement_0c2.txt"
    with open(file_path, 'a') as f:
        f.write(data+"\n")

def main():
    tcp()

if __name__ == '__main__':
    main()