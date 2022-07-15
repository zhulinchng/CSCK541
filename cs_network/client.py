"""Client object for the client side of the network."""
import socket
import json
import sys
import pickle
import time
from typing import Union
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from encryption import encrypt
from cs_network import data_config, network_config, data_input, validate_empty_value, continue_input, dict_to_xml_string

def initialize_client(host: str, port: int) -> socket.socket:
    """
    Initialize the client.

    :param host: The host to connect to.
    :param port: The port to connect to.
    :return: The client socket.
    """
    # open a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        return sock
    except ConnectionRefusedError:
        print("Connection refused.\nPlease check the host and port.")
        sys.exit(1)


def input_data(start_from=1,
               retry: int = 3,
               max_bytes: int = 1024,
               output_filelength: int = 97) -> tuple:
    """
    Input the data.

    :param retry: The number of times to retry the input.
    :param max_bytes: The maximum number of bytes for data.
    :param output_filelength: The maximum length of the output file name.
    :return: The tuple of dictionaries.
    """
    if start_from <= 1:
        for _ in range(retry):
            configuration_dict = data_config(
                retry=retry,
                output_filelength=output_filelength)
            if validate_empty_value(configuration_dict):
                break

    if start_from <= 2:
        for _ in range(retry):
            data_dictionary = data_input(
                config_dict=configuration_dict,
                max_bytes=max_bytes,
                retry=retry)
            if validate_empty_value(data_dictionary):
                break

    return configuration_dict, data_dictionary


def process_data(config_dict: dict, data: Union[str, dict]) -> tuple:
    """
    Process the data.

    :config_dict: The user's configuration data.
    :data: The user's data.
    :return: The processed data.
    """

    output_dict = config_dict.copy()

    if output_dict['encrypt'] == 1:
        output_dict['data'] = encrypt(str(data), output_dict.pop('public_key'))

    if output_dict['type'] == 2:
        with open(output_dict['txtfilepath'], 'w', encoding='utf-8') as file:
            file.write(str(output_dict['data']))
            print(
                f"Data written successfully to {output_dict.pop('txtfilepath')}")

    if output_dict['serialize'] == 1 or output_dict['encrypt'] == 1:
        output_dict['data'] = pickle.dumps(data)
    elif output_dict['serialize'] == 2 and output_dict['encrypt'] == 2:
        output_dict['data'] = json.dumps(data).encode('utf-8')
    elif output_dict['serialize'] == 3 and output_dict['encrypt'] == 2:
        output_dict['data'] = dict_to_xml_string(data)

    data_only = output_dict.pop('data')
    return output_dict, data_only


def wait_for_response(sock: socket.socket, timeout: int = 100, socksize: int = 1024) -> str:
    """
    Wait for the response.

    :param sock: The client socket.
    :return: The response.
    """
    sock.settimeout(timeout)
    try:
        response = sock.recv(socksize)
    except socket.timeout:
        print("Connection timed out.\nPlease try again.\nCheck the host and port.")
        sys.exit(1)
    return response


def send_with_retry(sock: socket.socket,
                    bytes_to_send: bytes,
                    retry: int = 3,
                    sleep: int = 1) -> None:
    """
    Send the data with retry.

    :param bytes_to_send: The data to send.
    :param sock: The client socket.
    :param retry: The number of times to retry the send.
    :return: None.
    """
    for i in range(retry):
        try:
            sock.sendall(bytes_to_send)
            break
        except ConnectionResetError:
            # retry after a second
            print(
                f"Connection Error, retrying in 1 second.\nRetry {i+1} of {retry}")
            time.sleep(sleep)


def start_client() -> None:
    """
    Main function.

    :return: None.
    """
    # get network configuration data
    host, port = network_config()
    # connect to the server
    sock = initialize_client(host, port)
    start = 1
    while start > 0:
        # get the config and input data
        config, data_dict = input_data(start_from=start)
        # process the data
        send_config, encoded_data = process_data(config, data_dict)
        # send config
        send_with_retry(sock, json.dumps(send_config).encode('utf-8'))
        res = wait_for_response(sock, timeout=100)
        if res.decode('utf-8') == "CONFIG OK":
            # send data
            send_with_retry(sock, encoded_data)
            res = wait_for_response(sock, timeout=100)
            if res.decode('utf-8') == "DATA OK":
                print("Data processed successfully.")
            else:
                print(f"Data processing failed: {res.decode('utf-8')}")
        else:
            print(f"Configuration failed: {res.decode('utf-8')}")
        start = continue_input()
    sock.close()


if __name__ == "__main__":

    start_client()
