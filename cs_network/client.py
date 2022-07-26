"""Client functions for the client side of the network."""
import socket
import json
import sys
import pickle
import time
import base64
from typing import Union
from os.path import dirname, join, abspath
import rsa
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cs_network import validate_empty_value, continue_input, dict_to_xml_string
from cs_network import data_config, network_config, data_input
from encryption import encrypt, EXAMPLE_PUB_KEY


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


def input_data(configuration_dict: dict,
               data_dictionary: dict,
               start_from: int = 1,
               retry: int = 3,
               max_bytes: int = 245,
               example_p_key: rsa.PublicKey = EXAMPLE_PUB_KEY,
               ) -> tuple:
    """
    Input the data.

    :param configuration_dict: The user's configuration data.
    :param data_dictionary: The user's data.
    :param start_from: The starting point of the data.
    :param retry: The number of times to retry the input.
    :param max_bytes: The maximum number of bytes for data.
    :param example_p_key: The example public key.
    :return: The tuple of dictionaries.
    """
    if start_from <= 1:
        for _ in range(retry):
            configuration_dict = data_config(
                retry=retry, example_key=example_p_key)
            if validate_empty_value(configuration_dict):
                break

    if start_from <= 2:
        data_dictionary = data_input(
            config_dict=configuration_dict,
            max_bytes=max_bytes)

    return configuration_dict, data_dictionary


def process_data(config_dict: dict, data: Union[str, dict]) -> tuple:
    """
    Process the data.

    :config_dict: The user's configuration data.
    :data: The user's data.
    :return: The processed data.
    """

    output_dict = config_dict.copy()
    time_txt = time.strftime("%Y%m%d_%H%M%S", time.localtime())

    if output_dict['encrypt'] == 1:
        output_dict['data'] = encrypt(str(data), output_dict.pop('public_key'))

    if output_dict['type'] == 2 and output_dict['encrypt'] == 1:
        textdata = base64.b64encode(output_dict['data']).decode('utf-8')
    elif output_dict['type'] == 2 and output_dict['encrypt'] == 2:
        textdata = data

    if output_dict['type'] == 2:
        if output_dict['txtfilepath'] is None:
            print("Invalid file path specified. File will not be saved.")
        else:
            with open(f"{output_dict['txtfilepath']}_{time_txt}.txt", 'w',
                      encoding='utf-8') as file:
                file.write(str(textdata))
                print(
                    f"Data written successfully to {output_dict.pop('txtfilepath')}_{time_txt}.txt")
        if output_dict['encrypt'] == 2:
            output_dict['data'] = textdata.encode('utf-8')

    if output_dict['serialize'] == 1 and output_dict['type'] == 1:
        if output_dict['encrypt'] == 1:
            output_dict['data'] = pickle.dumps(output_dict['data'])
        else:
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
    :param timeout: The timeout.
    :param socksize: The socket size.
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
    :param sleep: The number of seconds to sleep between retries.
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


def start_client(timeout: Union[int, None] = None) -> None:
    """
    Main function.

    :param timeout: The timeout for the client.
    :return: None.
    """
    # get network configuration data
    host, port = network_config()
    # connect to the server
    sock = initialize_client(host, port)
    sock.settimeout(timeout)  # set timeout
    start = 1
    config = {}
    data_dict = {}
    while start > 0:
        print("---------Connection Initialized---------")
        if start == 1:
            config, data_dict = input_data(
                config, data_dict, start_from=start, example_p_key=EXAMPLE_PUB_KEY)
        elif start == 2:
            data_dict = {}
            _, data_dict = input_data(
                config, data_dict, start_from=start, example_p_key=EXAMPLE_PUB_KEY)
        print("---------Processing Data---------")
        send_config, encoded_data = process_data(config, data_dict)
        print("Processing complete.")
        print("---------Sending Config---------")
        send_with_retry(sock, json.dumps(send_config).encode('utf-8'))
        res = wait_for_response(sock, timeout=100)
        if res.decode('utf-8') != "CONFIG_OK":
            print(f"Configuration failed: {res.decode('utf-8')}")
            sys.exit(1)
        print(res.decode('utf-8'))
        print("---------Sending Data---------")
        send_with_retry(sock, encoded_data)
        res = wait_for_response(sock, timeout=100)
        if res.decode('utf-8') == "DATA_OK":
            print("Data processed successfully.")
        else:
            print(f"Data processing failed: {res.decode('utf-8')}")
        print("--------- Continue? ---------")
        start = continue_input()
        send_with_retry(sock, str(start).encode('utf-8'))
    sock.close()
    print("Connection closed.")


if __name__ == "__main__":
    start_client()
