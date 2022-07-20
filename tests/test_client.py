# test for client.py
# one is required to change the values in the variables within a function to test
# if correct input is provided, the tests will run once the program is run
import unittest
import client

class servertests(unittest.TestCase):
    def test_initialize_client(self):
        actual = client.initialize_client("localhost", 80)
        expected = "localhost:80"
        self.assertEqual(actual, expected)

    def test_input_data(self):
        #change the input data to match your configuration
        actual = client.input_data(configuration_dict: dict,
                data_dictionary: dict,
                start_from=1,
                retry: int = 3,
                max_bytes: int = 245,
                example_p_key: rsa.PublicKey = EXAMPLE_PUB_KEY,
                )
        expected = ""
        self.assertEqual(actual, expected)

    def test_process_data(self):
        actual = client.process_data(config_dict: dict, data: Union[str, dict])
        expected = ""
        self.assertEqual(actual, expected)

    def test_wait_for_response(self):
        actual = client.wait_for_response(sock: socket.socket, timeout: int = 100, socksize: int = 1024)
        expected = ""
        self.assertEqual(actual, expected)
        
    def test_send_with_retry(self):
        actual = client.send_with_retry(sock: socket.socket,
                        bytes_to_send: bytes,
                        retry: int = 3,
                        sleep: int = 1)
        expected = ""
        self.assertEqual(actual, expected)

    def test_start_client():
        actual = client.start_server()
        expected = ""
        self.assertEqual(actual, expected)
