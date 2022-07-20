"""Test cases for client."""


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

# Input data test cases


# Encrypted dictionary test case
input_1_config = {"type": 1, "encrypt": 1, "public_key": ""}
input_1_data = {'encryptedkey': 'encryptedvalue',
                '123': '456', 'nested_dict': {'nest': 'value'}}
input_1 = join_config_data(input_1_config, input_1_data) + [""]

# Plain dictionary test case - Binary serialization
input_2_config = {"type": 1, "encrypt": 2, "serialize": 1}
input_2_data = {'testkey': 'testvalue',
                '123': '456', 'nested_dict': {'nest': 'value'}}
input_2 = join_config_data(input_2_config, input_2_data) + [""]

# Plain dictionary test case - JSON serialization
input_3_config = {"type": 1, "encrypt": 2, "serialize": 2}
input_3_data = {'testkey': 'testvalue',
                '123': '456', 'nested_dict': {'nest': 'value'}}
input_3 = join_config_data(input_3_config, input_3_data) + [""]

# Plain dictionary test case - XML serialization
input_4_config = {"type": 1, "encrypt": 2, "serialize": 3}
input_4_data = {'testkey': 'testvalue',
                'a123': '456', 'nested_dict': {'nest': {'nest2': 'value'}}}
input_4 = join_config_data(input_4_config, input_4_data) + [""]

# Encrypted text test case
input_5_config = {"type": 2, "txtfilepath": ".\\tests",
                  "txtfilename": 'client_output',
                  "encrypt": 1, "public_key": ""}
INPUT_5_DATA = "encryptedtext"
input_5 = join_config_data(input_5_config, {}) + [INPUT_5_DATA] + [""]

# Plain text test case - No serialization
input_6_config = {"type": 2, "txtfilepath": ".\\tests",
                  "txtfilename": 'client_output', "encrypt": 2}
INPUT_6_DATA = "plaintext"
input_6 = join_config_data(input_6_config, {}) + [INPUT_6_DATA] + [""]
