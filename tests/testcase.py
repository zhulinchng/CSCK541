"""Test cases for client."""
import os


def split_dict(data_dict: dict) -> list:
    """
    Convert key values of a dictionary to list elements.

    :param data_dict: The dictionary to split.
    :return: The list of values in the dictionary."""

    d_list = []
    for key, value in data_dict.items():
        d_list.append(key)
        d_list.append(value)
    return d_list


def join_config_data(config_dict: dict, data_dict: dict) -> list:
    """
    Join two dictionaries to a list.

    :param dict_1: The first dictionary.
    :param dict_2: The second dictionary.
    :return: The list of values in the dictionaries."""
    return list(config_dict.values()) + split_dict(data_dict)


# Encrypted dictionary test case
input_1_config = {"type": 1, "encrypt": 1, "public_key": ""}
input_1_data = {'encryptedkey': 'encryptedvalue',
                '123': '456', 'nested_dict': {'nest': 'value'}}
input_1 = join_config_data(input_1_config, input_1_data) + [""]
output_1_config = {"type": 1, "encrypt": 1, "serialize": 1}
test_case_1 = {'case': 'Encrypted Dictionary', 'input_config': input_1_config,
               'input_data': input_1_data,
               'input': input_1, 'output_config': output_1_config,
               'term_out': [
                   '------------Start Dictionary Text Output------------',
                   "'encryptedkey': 'encryptedvalue'", "'123': '456'",
                   "'nested_dict': {'nest': 'value'}",
                   '------------End Dictionary Text Output------------', '']}

# Plain dictionary test case - Binary serialization
input_2_config = {"type": 1, "encrypt": 2, "serialize": 1}
input_2_data = {'testkey': 'testvalue',
                '123': '456', 'nested_dict': {'nest': 'value'}}
input_2 = join_config_data(input_2_config, input_2_data) + [""]
output_2_config = {"type": 1, "encrypt": 2, "serialize": 1}
test_case_2 = {'case': 'Plain Dictionary - Binary Serialization',
               'input_config': input_2_config,
               'input_data': input_2_data,
               'input': input_2,
               'output_config': output_2_config,
               'term_out': ['------------Start Dictionary Text Output------------',
                            "'testkey': 'testvalue'", "'123': '456'",
                            "'nested_dict': {'nest': 'value'}",
                            '------------End Dictionary Text Output------------', '']}

# Plain dictionary test case - JSON serialization
input_3_config = {"type": 1, "encrypt": 2, "serialize": 2}
input_3_data = {'testkey': 'testvalue',
                '123': '456', 'nested_dict': {'nest': 'value'}}
input_3 = join_config_data(input_3_config, input_3_data) + [""]
output_3_config = {"type": 1, "encrypt": 2, "serialize": 2}
test_case_3 = {'case': 'Plain Dictionary - JSON Serialization',
               'input_config': input_3_config,
               'input_data': input_3_data,
               'input': input_3,
               'output_config': output_3_config,
               'term_out': ['------------Start Output------------',
                            "{'testkey': 'testvalue', '123': '456',\
 'nested_dict': {'nest': 'value'}}",
                            '------------End Output------------', '']}

# Plain dictionary test case - XML serialization
input_4_config = {"type": 1, "encrypt": 2, "serialize": 3}
input_4_data = {'testkey': 'testvalue',
                'a123': '456', 'nested_dict': {'nest': {'nest2': 'value'}}}
input_4 = join_config_data(input_4_config, input_4_data) + [""]
output_4_config = {"type": 1, "encrypt": 2, "serialize": 3}
OUTPUT_4_DATA = '<root><testkey>testvalue</testkey><a123>456</a123>\
<nested_dict><nest><nest2>value</nest2></nest></nested_dict></root>'
test_case_4 = {'case': 'Plain Dictionary - XML Serialization',
               'input_config': input_4_config,
               'input_data': input_4_data,
               'input': input_4, 'output_data': OUTPUT_4_DATA,
               'output_config': output_4_config,
               'term_out': ['------------Start Output------------',
                            "'<root><testkey>testvalue</testkey><a123>456</a123>\
<nested_dict><nest><nest2>value</nest2></nest></nested_dict></root>'",
                            '------------End Output------------', '']}

# Encrypted text test case
input_5_config = {"type": 2, "txtfilepath": os.path.dirname(__file__),
                  "txtfilename": 'client_test_output',
                  "encrypt": 1, "public_key": ""}
INPUT_5_DATA = "encryptedtext"
input_5 = join_config_data(input_5_config, {}) + [INPUT_5_DATA] + [""]
output_5_config = {"type": 2,
                   "encrypt": 1, "serialize": None}
test_case_5 = {'case': 'Encrypted Text', 'input_config': input_5_config,
               'input_data': INPUT_5_DATA,
               'input': input_5, 'output_config': output_5_config,
               'term_out': ['------------Start Output------------',
                            "'encryptedtext'",
                            '------------End Output------------', '']}

# Plain text test case - No serialization
input_6_config = {"type": 2, "txtfilepath": os.path.dirname(__file__),
                  "txtfilename": 'client_test_output', "encrypt": 2}
INPUT_6_DATA = "plaintext"
input_6 = join_config_data(input_6_config, {}) + [INPUT_6_DATA] + [""]
output_6_config = {"type": 2, "encrypt": 2,
                   "public_key": None, "serialize": None}
test_case_6 = {'case': 'Plain Text - No Serialization',
               'input_config': input_6_config,
               'input_data': INPUT_6_DATA,
               'input': input_6,
               'output_config': output_6_config,
               'term_out': ['------------Start Output------------',
                            "'plaintext'",
                            '------------End Output------------', '']}

# Continue input test cases
test_case_7 = {'case': 'Continue from input config', 'input_data': ['y', '1'],
               'output_data': 1}

test_case_8 = {'case': 'Continue from input data', 'input_data': ['y', '2'],
               'output_data': 2}

test_case_9 = {'case': 'Exit', 'input_data': ['y', '3'],
               'output_data': 0}

test_case_10 = {'case': 'Exit', 'input_data': 'n',
                'output_data': 0}


# Test cases for the Server Configuration
# Output to file
server_1_config = {"output_method": 1,
                   "filepath": os.path.dirname(__file__),
                   "filename": "server_test_output"}
server_1 = join_config_data(server_1_config, {}) + [""]
server_output_1_config = {"output_method": 1,
                          "filepath": f'{os.path.dirname(__file__)}\\server_test_output'}
server_case_1 = {'case': 'Server output to file',
                 'input_config': server_1_config,
                 'input': server_1,
                 'output_config': server_output_1_config}

# Output to terminal
server_2_config = {"output_method": 2}
server_2 = join_config_data(server_2_config, {})
server_output_2_config = {"output_method": 2, "filepath": None}
server_case_2 = {'case': 'Server output to console',
                 'input_config': server_2_config,
                 'input': server_2,
                 'output_config': server_output_2_config}
