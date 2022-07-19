"""Unit test for client."""
import sys
import unittest
from unittest import mock
from typing import List
from io import StringIO
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cs_network import client, server


class TestClient(unittest.TestCase):
    """Unit test for client."""

    @mock.patch('sys.stdout', new_callable=StringIO)
    def client_input_test(self, test_inputs: List, mock_stdout: StringIO) -> str:
        """Test input_data."""
        with mock.patch('builtins.input', side_effect=test_inputs):
            config, data = client.input_data({},{})
        return config, data

    def test_input(self):
        """Test for input_data."""

        inputs = {"type": "1", "encrypt": "2", "serialize": "1",
                  "key1": "1234567890", "value1": "abc", "end_dict": ""}
        config, data = self.client_input_test(inputs.values())
        print(config, data) 
        # self.assertEqual(config, testcase_config)

    # def test_process(self):
    #     """Test for process_data."""
    #     config = {}
    #     data = {}
    #     send_config, encoded_data = client.process_data(config, data)
    #     print(send_config, encoded_data)
        # self.assertEqual(send_config, testcase_config)

    # def test_continue(self):
    #     """Test for continue input."""
    #     with mock.patch('builtins.input', side_effect=["y", "n"]):
    #         self.assertTrue(client.continue_input())
    #         self.assertFalse(client.continue_input())

if __name__ == "__main__":
    unittest.main()
