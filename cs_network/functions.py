"""Common functions for the cs_network module."""
import socket
import sys
import string
import json
import time
import pickle
import os
from xml.parsers.expat import ExpatError
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, tostring
from typing import Union
from ast import literal_eval
from os.path import dirname, join, abspath, exists, isdir
import rsa
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from encryption import EXAMPLE_PUB_KEY, load_pub_key

def dict_to_xml_string(dict_val: dict, root_tag: str = 'root') -> str:
    """
    Convert a dictionary to an XML string.

    :param dict_val: The dictionary to convert.
    :param root_tag: The root tag of the XML string.
    :return: The XML string.
    """
    def dict_to_xml(dict_val: dict, tag: str = root_tag) -> Element:
        """
        Convert a dictionary to an XML element.

        :param dict_val: The dictionary to convert.
        :param tag: The tag of the element.
        :return: The XML element.
        """
        root = Element(tag)
        for key, value in dict_val.items():
            child = Element(str(key))
            # Recursively call this function to support nested dictionaries
            if isinstance(value, dict):
                child.append(list(dict_to_xml(value))[0])
            else:
                child.text = str(value)
            root.append(child)
        return root
    return tostring(dict_to_xml(dict_val), encoding='utf-8')


def validate_xml_key(xml_str: str) -> bool:
    """
    Validate an XML string.

    :param xml_str: The XML string to validate.
    :return: True if the XML string is valid, False otherwise.
    """
    try:
        parseString(f'<{xml_str}>a</{xml_str}>')
        return True
    except ExpatError:
        return False


def validate_xml_value(xml_str: str) -> bool:
    """
    Validate that the XML string is valid.

    :param xml_str: The XML string to validate.
    :return: True if the XML string is valid, False otherwise.
    """
    try:
        parseString(f'<a>{xml_str}</a>')
        return True
    except ExpatError:
        return False


def network_config(retry: int = 3, default_port: int = 50541) -> tuple:
    """
    Get the user's configuration.

    :retry: The number of times to retry the input.
    :default_port: The default port to connect to.
    :return: The user's configuration.
    """
    # Network config
    print("------------Enter network configuration------------")
    for _ in range(retry):
        try:
            default = socket.gethostname()
            host = input(
                f"Enter the IPv4 host, or press enter to use {default}: ")
            if host == '':
                host = default
                print("Using default hostname:", host)
            socket.gethostbyname(host)
            break
        except socket.gaierror:
            print("Invalid hostname.\nEnter a valid IPv4 hostname.")
            continue

    for _ in range(retry):
        try:
            port = input(
                "Enter the port, or press enter for default port 50541: ")
            if port == '':
                port = default_port
                print("Using default port:", port)
            port = int(port)
            if port < 0 or port > 65535:
                raise ValueError
            return host, port
        except ValueError:
            print("Invalid port.\nEnter a valid port.")
            continue


def validation(config_input: str, input_tup: tuple, err_msg: str = "Invalid input") -> bool:
    """
    Validate the input.

    :param config_input: The input to validate.
    :param input_tup: The valid input range.
    :param err_msg: The error message to print.
    :return: True if the input is valid, False otherwise.
    """
    try:
        int(config_input)
        if int(config_input) not in input_tup:
            raise ValueError
        return True
    except ValueError:
        print(err_msg)
        return False


def data_config(retry: int = 3,
                example_key: rsa.PublicKey = EXAMPLE_PUB_KEY) -> dict:
    """
    Get the user's configuration data.

    :retry: The number of times to retry the input.
    :example_key: The example key to use.
    :return: The user's configuration data.
    """
    # Data config
    print("------------Enter data configuration------------")
    valid_chars = string.ascii_letters + string.digits + '_.-'
    error_message = "Invalid input.\nEnter a valid number in "
    time_txt = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    config = {}

    for _ in range(retry):
        config['type'] = input(
            "Send a dictionary (1), or a text (2): ").strip()
        valid_range = (1, 2)
        if validation(config['type'], valid_range, error_message + str(valid_range)):
            config['type'] = int(config['type'])
            break

    if config['type'] == 2:
        for _ in range(retry):
            try:
                config['txtfilepath'] = input(
                    "Enter folder path save the file, or press Enter to use current directory: "
                ).strip()
                if config['txtfilepath'] == '':
                    config['txtfilepath'] = os.getcwd()
                    print("Using current directory: " + config['txtfilepath'])
                if not isdir(config['txtfilepath']):
                    raise FileNotFoundError
                txtfilename = input(
                    "Enter the filename prefix, or press Enter to use 'client_output': "
                ).strip()
                if not all(char in valid_chars for char in txtfilename):
                    print("Invalid file name.\nEnter a valid file name.")
                    raise ValueError
                if txtfilename == '':
                    txtfilename = 'client_output'
                    print("Using filename prefix: " + txtfilename)
                elif '.' in txtfilename:
                    txtfilename = txtfilename.split('.')[0]
                if len(join(config['txtfilepath'], f'{txtfilename}_{time_txt}.txt')) > 255:
                    print("Filename too long.\nEnter a shorter filename.")
                    raise ValueError
                config['txtfilepath'] = join(
                    config['txtfilepath'], txtfilename)
                break
            except FileNotFoundError:
                print("Invalid folder path.\nEnter a valid folder path.")
                continue
            except ValueError:
                continue
    else:
        config['txtfilepath'] = None

    for _ in range(retry):
        config['encrypt'] = input("Encrypt (1) or not (2): ").strip()
        valid_range = (1, 2)
        if validation(config['encrypt'], valid_range, error_message + str(valid_range)):
            config['encrypt'] = int(config['encrypt'])
            break

    if config['encrypt'] == 1:
        for _ in range(retry):
            try:
                config['public_key'] = input(
                    "Enter the public key .pem file path, or press enter to use example key: "
                ).strip()
                if config['public_key'] == '':
                    config['public_key'] = example_key
                    print("Using example public key")
                    break
                if exists(config['public_key']):
                    if config['public_key'].split('.')[-1] == 'pem':
                        config['public_key'] = load_pub_key(
                            config['public_key'])
                    break
                raise FileNotFoundError
            except FileNotFoundError:
                print("Public key .pem file not found.\nEnter a valid file path.")
                continue
    else:
        config['public_key'] = None

    if config['type'] == 1 and config['encrypt'] == 2:
        for _ in range(retry):
            config['serialize'] = input(
                "Select serialization method (1) Binary (2) JSON (3) XML: ").strip()
            valid_range = (1, 2, 3)
            if validation(config['serialize'], valid_range, error_message + str(valid_range)):
                config['serialize'] = int(config['serialize'])
                break
    elif config['encrypt'] == 1:
        print("Serialization method will default to binary for encrypted dictionary.")
        config['serialize'] = 1
    else:
        config['serialize'] = None

    return config


def server_config(retry: int = 3) -> dict:
    """
    Get the server's configuration data.

    :retry: The number of times to retry the input.
    :output_filelength: The length of the output file name.
    :return: The server's configuration data.
    """
    serv_config = {}
    print("------------Enter server configuration------------")
    valid_chars = string.ascii_letters + string.digits + '_.-'
    error_message = "Invalid input.\nEnter a valid number in "
    time_txt = time.strftime("%Y%m%d_%H%M%S", time.localtime())

    for _ in range(retry):
        serv_config['output_method'] = input(
            "Output to file (1) or console (2): ").strip()
        valid_range = (1, 2)
        if validation(serv_config['output_method'], valid_range, error_message + str(valid_range)):
            serv_config['output_method'] = int(serv_config['output_method'])
            break

    if serv_config['output_method'] == 1:
        for _ in range(retry):
            try:
                serv_config['filepath'] = input(
                    "Enter folder path save the file, or press Enter to use current directory: "
                ).strip()
                if serv_config['filepath'] == '':
                    serv_config['filepath'] = os.getcwd()
                    print("Using current directory: " +
                          serv_config['filepath'])
                if not isdir(serv_config['filepath']):
                    raise FileNotFoundError
                filename = input(
                    "Enter the filename prefix, or press Enter to use 'server_output': "
                ).strip()
                if not all(char in valid_chars for char in filename):
                    print("Invalid file name.\nEnter a valid file name.")
                    raise ValueError
                if filename == '':
                    filename = 'server_output'
                    print("Using filename prefix: " + filename)
                elif '.' in filename:
                    filename = filename.split(".")[0]
                if len(join(serv_config['filepath'], f'{filename}_{time_txt}.txt')) > 255:
                    print("Filename too long.\nEnter a shorter filename.")
                    raise ValueError
                serv_config['filepath'] = join(
                    serv_config['filepath'], filename)
                break
            except FileNotFoundError:
                print("Invalid folder path.\nEnter a valid folder path.")
                continue
            except ValueError:
                continue
    else:
        serv_config['filepath'] = None

    return serv_config


def data_input(config_dict: dict, max_bytes: int = 1024, retry: int = 3) -> Union[str, dict]:
    """
    Get the user's data.

    :config_dict: The user's configuration data.
    :return: The user's data.
    """
    def size_check(data: Union[str, dict], serial_method: int = config_dict['serialize']) -> bool:
        if serial_method == 1:
            size = len(pickle.dumps(data))
        elif serial_method == 2:
            size = len(json.dumps(data).encode('utf-8'))
        elif serial_method == 3:
            size = len(dict_to_xml_string(data))
        else:
            size = len(data.encode('utf-8'))
        compare = max_bytes-size
        if compare < 0:
            return False, compare
        return True, size
    # Data input
    print("------------Enter data------------")
    print("Maximum data size: " + str(max_bytes) + " bytes")
    if config_dict['type'] == 2:
        for _ in range(retry):
            print("Enter the text data:")
            data = input("Enter the text: ").strip()
            if size_check(data)[0]:
                return data
            print(
                f"Data size exceeded {-size_check(data)[1]} bytes.\nEnter less data.")

    key = 'default'
    data = {}
    print("Enter the dictionary:")
    while True:
        scheck, size = size_check(data)
        if not scheck:
            print(f"Data size exceeded.\n Stopping at {key}.")
            break
        key = input("Enter the key, or press Enter to finish: ").strip()
        if key == '':
            break
        if config_dict['serialize'] == 3:
            if not validate_xml_key(key):
                print("Invalid key for XML.")
                continue
        dvalue = input("Enter the value: ").strip()
        try:
            xvalue = literal_eval(dvalue)
            if config_dict['serialize'] == 3:
                if isinstance(xvalue, dict):
                    xml_string = dict_to_xml_string(xvalue)
                    try:
                        parseString(xml_string)
                    except ExpatError:
                        print("Invalid value for XML.")
                        continue
                if validate_xml_value(xvalue):
                    data[key] = xvalue
                    continue
                else:
                    print("Invalid value for XML.")
                    continue
            data[key] = xvalue
        except (ValueError, SyntaxError):
            if config_dict['serialize'] == 3:
                if validate_xml_value(dvalue):
                    data[key] = dvalue
                else:
                    print("Invalid value for XML.")
                    continue
            else:
                data[key] = dvalue
        print(f'Dictionary: {data} \nSize: {size} bytes')
    return data


def validate_empty_value(input_dict: Union[str, dict]) -> bool:
    """
    Validate that a value in the dictionary is not empty.

    :input_dict: The dictionary to validate.
    :return: True if all values in the dictionary is not empty, False otherwise.
    """
    if isinstance(input_dict, str):
        return input_dict != ''
    else:
        for key, value in input_dict.items():
            if value == '':
                print(f"{key} is empty. Enter a value for {key}.\nPlease try again.")
                return False
        return True


def continue_input() -> int:
    """
    Continue input.

    :return: True if the user wants to continue, False otherwise.
    """
    while True:
        answer = input("Do you want to continue? (y/n): ")
        if answer.lower() == 'y':
            where = input("""
Continue from:
(1) Input configuration and data
(2) Input data only
(3) Exit
Select: """).strip()
            if where == '1':
                print("------------Starting from Input Config------------")
                return 1
            elif where == '2':
                print("------------Starting from Input Data------------")
                return 2
            elif where == '3':
                print("------------Exiting------------")
                return 0
            else:
                print("Invalid input.")
                continue
        elif answer.lower() == 'n':
            return 0
        else:
            print("Please enter 'y' or 'n'.")


if __name__ == "__main__":
    net = network_config()
    print(net)
    input_config = data_config()
    print(input_config)
    test_data = data_input(input_config)
    print(test_data)
