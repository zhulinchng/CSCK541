"""Functions for the Client-Server Network Module."""
__version__ = "1.0.1"
from .functions import data_config, network_config, data_input, validate_empty_value
from .functions import continue_input, dict_to_xml_string, server_config
from .client import initialize_client, input_data, process_data
from .client import wait_for_response, send_with_retry, start_client
from .server import initialize_server, receive_config, receive_data, send_response, print_dict
from .server import start_server, get_private_key, print_to_terminal, process_recv_data
