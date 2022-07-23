"""Server functions for the server side of the network."""
import socket
import sys
import json
import time
import pickle
import base64
from ast import literal_eval
import xml.dom.minidom
from typing import Union
from os.path import dirname, join, abspath, exists
import rsa
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
    :param retry: The number of times to retry the connection.
    :return: The dictionary of data.
    """
    # receive the data
    for i in range(1, retry+1):
        try:
            recv_data = connection.recv(1024)
            if address != '':
                print('Connected by', address)
            connection_ok = True
        except socket.error:
            print("Connection Error on receiving config.")
            connection_ok = False
        if not recv_data:
            print("No configuration received.")
        try:
            recv_data = json.loads(recv_data)
            if connection_ok:
                connection.sendall('CONFIG_OK'.encode('utf-8'))
                return recv_data
            else:
                print("Connection Error on sending CONFIG_OK response.")
        except json.decoder.JSONDecodeError:
            print("Could not decode the data.\nPlease check the data.")
            if connection_ok:
                connection.sendall(
                    'CONFIG_ERROR: JSONDecodeError'.encode('utf-8'))
            else:
                print("Connection Error on sending CONFIG DECODE ERROR response.")
        print(f"Receive config error. Retry {i} of {repr(retry)}")
        time.sleep(1)
    sys.exit(1)


def receive_data(connection: socket.socket, retry: int = 3) -> bytes:
    """
    Receive data from a connection.

    :param connection: The connection to receive data from.
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
    :param retry: The number of times to retry the connection.
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
    Get the server private key.

    :param retry: The number of times to retry the connection.
    :param example_key: The example private key.
    :return: The private key.
    """
    keypath = ''
    priv_key = ''
    for _ in range(retry):
        try:
            keypath = input(
                "Enter the private key .pem file path, or press Enter to use example key: "
            ).strip()
            if keypath == '':
                priv_key = example_key
                print("Using example private key.")
                break
            if exists(keypath):
                if keypath.split('.')[-1] == 'pem':
                    priv_key = load_priv_key(keypath)
                break
            raise FileNotFoundError
        except FileNotFoundError:
            print("Public key .pem file not found.\nEnter a valid file path.")
            continue
    if priv_key == '':
        print("Could not load the private key.\nEncrypted data will not be decrypted.")
    return priv_key


def print_dict(input_dict: dict) -> None:
    """
    Print a dictionary iteratively.

    :param d: The dictionary to print.
    :return: None.
    """
    print("------------Start Dictionary Text Output------------")
    if isinstance(input_dict, dict):
        for key, value in input_dict.items():
            print(f"{repr(key)}: {repr(value)}")
    else:
        print(f"{repr(input_dict)}")
    print("------------End Dictionary Text Output------------")


def print_to_terminal(text: str) -> None:
    """
    Print to the terminal.

    :param text: The text to print.
    :return: None.
    """
    print("------------Start Output------------")
    print(repr(text))
    print("------------End Output------------")


def process_recv_data(config_dict: dict,
                      recv_data: bytes,
                      server_configuration: dict,
                      priv_key: rsa.PrivateKey = EXAMPLE_PRIV_KEY) -> str:
    """
    Process the received data.

    :param config_dict: The dictionary of config.
    :param recv_data: The received data.
    :param server_configuration: The server configuration.
    :param priv_key: The private key.
    :return: The processed data.
    """
    # Initialize the variables
    status = 'DATA_OK'

    # Deserialize the data
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
    elif config_dict['type'] == 2 and config_dict['encrypt'] == 2:
        recv_data = recv_data.decode('utf-8')

    # Decrypt the data
    if config_dict['encrypt'] == 1:
        try:
            recv_data = decrypt(recv_data, priv_key).decode('utf-8')
        except (rsa.pkcs1.DecryptionError, AttributeError):
            print("Decryption Error: Could not decrypt the data.")
            status = 'DATA_ERROR: DecryptionError'
            recv_data = base64.b64encode(recv_data).decode('utf-8')

    # Output the data to terminal
    if server_configuration['output_method'] == 2:
        if config_dict['serialize'] == 1 and config_dict['type'] == 1:
            if isinstance(recv_data, str):
                try:
                    recv_data = literal_eval(recv_data)
                except (ValueError, SyntaxError):
                    print("Could not literal_eval the data.")
                    status = 'DATA_ERROR: ValueError'
            print_dict(recv_data)
        else:
            print_to_terminal(recv_data)
    # Output the data to file
    elif server_configuration['output_method'] == 1:
        time_txt = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        filepath = server_configuration['filepath']+'_'+time_txt
        try:
            if config_dict['serialize'] == 1 and config_dict['type'] == 1:
                filepath = filepath+'.p'
                with open(filepath, 'wb') as pkl_file:
                    pickle.dump(recv_data, pkl_file)
                print_to_terminal(f"Data written to {filepath}")
            elif config_dict['serialize'] == 2 and config_dict['type'] == 1:
                filepath = filepath+'.json'
                with open(filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(recv_data, json_file, indent=4)
                print_to_terminal(f"Data written to {filepath}")
            elif config_dict['serialize'] == 3 and config_dict['type'] == 1:
                filepath = filepath+'.xml'
                recv_data = xml.dom.minidom.parseString(recv_data).toprettyxml(
                    indent='\t', encoding='utf-8').decode('utf-8').strip()
                with open(filepath, 'w', encoding='utf-8') as xml_file:
                    xml_file.write(recv_data)
                print_to_terminal(f"Data written to {filepath}")
            elif config_dict['type'] == 2:
                filepath = filepath+'.txt'
                with open(filepath, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(str(recv_data))
                print_to_terminal(f"Data written to {filepath}")
            else:
                print("Invalid serialize type.")
                status = 'DATA_ERROR: Invalid serialize type.'
        except OSError:
            status = 'DATA_ERROR: Could not write to file.'

    return status


def start_server(timeout: Union[int, None] = None) -> None:
    """
    Start the server.

    :param timeout: The timeout for the server.
    :return: None.
    """
    # Get server configuration
    host, port = network_config()
    sock = initialize_server(host, port)
    serv_conf = server_config()
    key = get_private_key()
    print("------------Start Connection------------")
    conn, addr = sock.accept()
    conn.settimeout(timeout)  # Set the timeout for the connection
    try:
        with conn:
            cont = 1
            while cont > 0:
                # Get client configuration
                config = receive_config(conn, addr)
                # Get client data
                data = receive_data(conn)
                # Process data
                status_msg = process_recv_data(
                    config, data, serv_conf, priv_key=key)
                # Send status message
                send_response(conn, status_msg)
                # Check if the client wants to continue
                cont = int(receive_data(conn).decode('utf-8'))
    except socket.timeout:
        print("Connection timed out.")
    except ConnectionError:
        print("Connection Error.")
    sock.close()
    print("Server closed.")


if __name__ == "__main__":
    start_server()
