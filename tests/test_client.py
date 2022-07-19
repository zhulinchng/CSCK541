# test for client.py
# one is required to change the values in the variables within a function to test
# if correct input is provided, the tests will run once the program is run
import pytest
import client

def test_initialize_client():
    initialization = client.initialize_client("localhost", 80)
    print(initialization)

def test_input_data():
    #change the input data to match your configuration
    input data = client.input_data(configuration_dict: dict,
               data_dictionary: dict,
               start_from=1,
               retry: int = 3,
               max_bytes: int = 245,
               example_p_key: rsa.PublicKey = EXAMPLE_PUB_KEY,
               )
    print(input data)

def test_process_data():
    process data = client.process_data(config_dict: dict, data: Union[str, dict])
    print (process_data)

def test_wait_for_response():
    wait_for_response = client.wait_for_response(sock: socket.socket, timeout: int = 100, socksize: int = 1024)
    print(wait_for_response)

def test_send_with_retry():
    send_with_retry = client.send_with_retry(sock: socket.socket,
                    bytes_to_send: bytes,
                    retry: int = 3,
                    sleep: int = 1)
    print (send_with_retry)

def test_start_client():
    server_started = client.start_server()
    print server_started
