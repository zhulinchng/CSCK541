"""Unit test for client."""
import sys
import time
import pickle
import unittest
from unittest import mock
from io import StringIO
import json
import os
from os.path import dirname, join, abspath
import rsa
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from tests import testcase
from encryption import EXAMPLE_PUB_KEY, EXAMPLE_PRIV_KEY
from cs_network import server


class TestServer(unittest.TestCase):
    """Unit test for client."""

    def server_netconf_input_test(self, test_inputs: list) -> tuple:
        """Mock input for network_config."""
        test_inputs = [str(x) for x in test_inputs]
        with mock.patch('builtins.input', side_effect=test_inputs):
            host, port = server.network_config()
        return host, port

    def test_network_config(self):
        "Test network_config."
        host, port = self.server_netconf_input_test(["localhost", "12345"])
        self.assertEqual(host, "localhost")
        self.assertEqual(port, 12345)

    # @mock.patch('sys.stdout', new_callable=StringIO)
    # def server_config_input_test(self, test_inputs: list, mock_stdout: StringIO) -> tuple:
    #     """Mock input_data."""
    #     outputs = []
    #     test_inputs = [str(x) for x in test_inputs]
    #     with mock.patch('builtins.input', side_effect=test_inputs):
    #         config, data = server.server_config()
    #         outputs.append(mock_stdout.getvalue())
    #     return config, data, outputs[0].split("\n")

    # @mock.patch('sys.stdout', new_callable=StringIO)
    # def server_key_input_test(self, test_inputs: list, mock_stdout: StringIO) -> tuple:
    #     """Mock input_data."""
    #     outputs = []
    #     test_inputs = [str(x) for x in test_inputs]
    #     with mock.patch('builtins.input', side_effect=test_inputs):
    #         config, data = server.get_private_key()
    #         outputs.append(mock_stdout.getvalue())
    #     return config, data, outputs[0].split("\n")

    # def test_process_recv_data(self):
    #     "Test process_recv_data."
    #     return



if __name__ == "__main__":
    unittest.main()
