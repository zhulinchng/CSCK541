"""Server functions for the server side of the network."""
import socket
import sys
import json
import time
import os
import pickle
import rsa
from xml.etree.ElementTree import fromstring, ElementTree
from os.path import dirname, join, abspath, exists
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cs_network import network_config, server_config
from encryption import decrypt, EXAMPLE_PRIV_KEY, load_priv_key


def initialize_server(host: str, port: int, backlog: int = 1) -> socket.socket:
    """
    Initialize the server.

    :param host: The host to bind to.
    :param port: The port to bind to.
    :param backlog: The backlog of the socket.
    :return: The server socket.
    """
    # open a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        sock.listen(backlog)
        print(f"Listening on {host}:{port}")
        return sock
    except OSError:
        print("Could not bind to host and port.\nPlease check the host and port.")
        sys.exit(1)


def receive_config(connection: socket.socket, address: str = '', retry: int = 3) -> dict:
    """
    Receive config from a connection.

    :param connection: The connection to receive data from.
    :param address: The address of the connection.
    :param timeout: The timeout of the connection.
    :param retry: The number of times to retry the connection.
    :return: The dictionary of data.
    """
    # receive the data
    for i in range(retry):
        if address != '':
            print('Connected by', address)
        try:
            recv_data = connection.recv(1024)
        except socket.error:
            print("Connection Error on receiving config.")
        if not recv_data:
            print("No configuration received.")
        try:
            recv_data = json.loads(recv_data)
            connection.sendall('CONFIG_OK'.encode('utf-8'))
            return recv_data
        except json.decoder.JSONDecodeError:
            print("Could not decode the data.\nPlease check the data.")
            connection.sendall('CONFIG_ERROR: JSONDecodeError'.encode('utf-8'))
        print(f"Receive config error. Retry {i+1} of {retry}")
        time.sleep(1)
    sys.exit(1)


def receive_data(connection: socket.socket, retry: int = 3) -> bytes:
    """
    Receive data from a connection.

    :param connection: The connection to receive data from.
    :param address: The address of the connection.
    :param timeout: The timeout of the connection.
    :param retry: The number of times to retry the connection.
    :return: The data.
    """
    # receive the data
    for i in range(retry):
        try:
            recv_data = connection.recv(2048)
            return recv_data
        except socket.error:
            print("Connection Error on receiving data.")
        print(f"Receive data error. Retry {i+1} of {retry}")
        time.sleep(1)
    sys.exit(1)


def send_response(connection: socket.socket, response: str, retry: int = 3) -> None:
    """
    Send a response to a connection.

    :param connection: The connection to send the response to.
    :param response: The response to send.
    :param timeout: The timeout of the connection.
    :return: None.
    """
    for i in range(retry):
        try:
            connection.sendall(response.encode('utf-8'))
            return None
        except socket.error:
            print(f"Could not send the response. Retry {i+1} of {retry}")
            time.sleep(1)
    sys.exit(1)


def get_private_key(retry: int = 3,
                    example_key: rsa.PrivateKey = EXAMPLE_PRIV_KEY
                    ) -> rsa.PrivateKey:
    """
    Get the private key.

    :return: The private key.
    """
    keypath = ''
    for _ in range(retry):
        try:
            keypath = input(
                "Enter the private key .pem file path, or press enter to use example key: "
            ).strip()
            if keypath == '':
                priv_key = example_key
                print("Using example private key")
                break
            if exists(keypath):
                if keypath.split('.')[-1] == 'pem':
                    priv_key = load_priv_key(keypath)
                break
            raise FileNotFoundError
        except FileNotFoundError:
            print("Public key .pem file not found.\nEnter a valid file path.")
            continue
    return priv_key


def print_to_terminal(text: str) -> None:
    """
    Print to the terminal.

    :param text: The text to print.
    :return: None.
    """
    print("------------Start Output------------")
    print(text)
    print("------------End Output------------")


def process_recv_data(config_dict: dict,
                      recv_data: bytes,
                      server_configuration: dict,
                      priv_key: rsa.PrivateKey = EXAMPLE_PRIV_KEY) -> str:
    """
    Process the received data.

    :param config_dict: The dictionary of config.
    :param recv_data: The received data.
    :return: The processed data.
    """
    # decrypt the data

    status = 'DATA_OK'

    if config_dict['type'] == 1:
        if config_dict['serialize'] == 1:
            recv_data = pickle.loads(recv_data)
        elif config_dict['serialize'] == 2:
            recv_data = json.loads(recv_data.decode('utf-8'))
        elif config_dict['serialize'] == 3:
            recv_data = recv_data.decode('utf-8')
        else:
            print("Invalid serialize type.")
            status = 'DATA_ERROR: Invalid serialize type.'
    elif config_dict['type'] == 2:
        recv_data = recv_data.decode('utf-8')

    if config_dict['encrypt'] == 1:
        try:
            print(recv_data)
            recv_data = decrypt(recv_data, priv_key).decode('utf-8')
        except rsa.pkcs1.DecryptionError:
            print("Decryption Error: Could not decrypt the data.")
            status = 'DATA_ERROR: DecryptionError'

    if server_configuration['output_method'] == 2:
        print_to_terminal(recv_data)
    elif server_configuration['output_method'] == 1:
        try:
            if config_dict['serialize'] == 1:
                filepath = server_configuration['filepath']+'.p'
                with open(filepath, 'wb') as pkl_file:
                    pickle.dump(recv_data, pkl_file)
                print_to_terminal(f"Data written to {filepath}")
            elif config_dict['serialize'] == 2:
                filepath = server_configuration['filepath']+'.json'
                with open(filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(recv_data, json_file)
                print_to_terminal(f"Data written to {filepath}")
            elif config_dict['serialize'] == 3:
                filepath = server_configuration['filepath']+'.xml'
                ElementTree(fromstring(recv_data)).write("temp.xml")
                os.replace("temp.xml", filepath)
                print_to_terminal(f"Data written to {filepath}")
            else:
                print("Invalid serialize type.")
                status = 'DATA_ERROR: Invalid serialize type.'
        except OSError:
            status = 'DATA_ERROR: Could not write to file.'

    return status


def start_server() -> None:
    """
    Start the server.

    :return: None.
    """
    key = get_private_key()
    host, port = network_config()
    sock = initialize_server(host, port)
    serv_conf = server_config()
    conn, addr = sock.accept()
    with conn:
        cont = 1
        while cont > 0:
            config = receive_config(conn, addr)
            data = receive_data(conn)
            status_msg = process_recv_data(
                config, data, serv_conf, priv_key=key)
            send_response(conn, status_msg)
            cont = int(receive_data(conn).decode('utf-8'))
    sock.close()
    print("Server closed.")


if __name__ == "__main__":
    start_server()
