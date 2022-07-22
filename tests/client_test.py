"""Unit test for client."""
import sys
import time
import pickle
import unittest
from unittest import mock
import json
import os
from os.path import dirname, join, abspath
import rsa
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from cs_network import client
from encryption import EXAMPLE_PUB_KEY, EXAMPLE_PRIV_KEY
from tests import client_testcase


class TestClient(unittest.TestCase):
    """Unit test for client."""

    def client_input_test(self, test_inputs: list) -> tuple:
        """Mock input_data."""
        test_inputs = [str(x) for x in test_inputs]
        with mock.patch('builtins.input', side_effect=test_inputs):
            config, data = client.input_data({}, {})
        return config, data

    def del_none_from_dict(self, config_dict: dict) -> dict:
        """
        Delete None values from a dictionary.

        :param config_dict: The configuration dictionary.
        :return: The parsed configuration dictionary.
        """
        iterate = list(config_dict.items())
        for key, value in iterate:
            if value is None:
                del config_dict[key]
        return config_dict

    def test_input_encrypted_dict(self):
        """Encrypted dictionary input test case."""

        config, data = self.client_input_test(client_testcase.input_1)
        config = self.del_none_from_dict(config)
        client_testcase.input_1_config['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.input_1_config['serialize'] = 1
        self.assertEqual(config, client_testcase.input_1_config)
        self.assertEqual(data, client_testcase.input_1_data)

    def test_input_plain_dict_serial(self):
        """
        Plain dictionary input test case.
        Testing binary, JSON and XML serialization.
        """
        tests = [client_testcase.test_case_2,
                 client_testcase.test_case_3, client_testcase.test_case_4]
        for test in tests:
            with self.subTest(case=test['case']):
                config, data = self.client_input_test(test['input'])
                config = self.del_none_from_dict(config)
                self.assertEqual(config, test['input_config'])
                self.assertEqual(data, test['input_data'])

    def test_input_encrypted_text(self):
        """Encrypted text test case."""

        config, data = self.client_input_test(client_testcase.input_5)
        client_testcase.input_5_config[
            'txtfilepath'] = f'{client_testcase.input_5_config["txtfilepath"]}\
\\{client_testcase.input_5_config["txtfilename"]}'
        del client_testcase.input_5_config['txtfilename']
        client_testcase.input_5_config['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.input_5_config['serialize'] = None
        self.assertEqual(config, client_testcase.input_5_config)
        self.assertEqual(data, client_testcase.INPUT_5_DATA)

    def test_input_plain_text(self):
        """Plain text test case."""

        config, data = self.client_input_test(client_testcase.input_6)
        client_testcase.input_6_config[
            'txtfilepath'] = f'{client_testcase.input_6_config["txtfilepath"]}\
\\{client_testcase.input_6_config["txtfilename"]}'
        del client_testcase.input_6_config['txtfilename']
        client_testcase.input_6_config['public_key'] = None
        client_testcase.input_6_config['serialize'] = None
        self.assertEqual(config, client_testcase.input_6_config)
        self.assertEqual(data, client_testcase.INPUT_6_DATA)

    def test_process(self):
        """Test for process_data."""
        client_testcase.test_case_1['input_config']['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.test_case_1['input_config']['serialize'] = 1
        client_testcase.test_case_5['input_config']['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.test_case_5['input_config']['serialize'] = None

        tests = [client_testcase.test_case_1, client_testcase.test_case_2,
                 client_testcase.test_case_3, client_testcase.test_case_4,
                 client_testcase.test_case_5, client_testcase.test_case_6]
        for test in tests:
            with self.subTest(case=test['case']):
                # As encryption uses random numbers for padding, we need to
                # decrypt the data to compare it to the original.
                if test['input_config']['encrypt'] == 1:
                    test_config, test_data = client.process_data(test['input_config'],
                                                                 test['input_data'])
                    self.assertEqual(test_config, test['output_config'])
                    if test['input_config']['type'] == 1:
                        self.assertEqual(
                            (rsa.decrypt(
                                pickle.loads(test_data), EXAMPLE_PRIV_KEY)).decode('utf-8'),
                            str(test['input_data']))
                    elif test['input_config']['type'] == 2:
                        # delete file after test
                        try:
                            os.remove(f"\
{test['input_config']['txtfilepath']}_\
{time.strftime('%Y%m%d_%H%M%S', time.localtime())}.txt")
                        except FileNotFoundError:
                            pass
                        self.assertEqual((rsa.decrypt(test_data, EXAMPLE_PRIV_KEY)).decode('utf-8'),
                                         str(test['input_data']))
                elif test['input_config']['encrypt'] == 2:
                    test_config, test_data = client.process_data(test['input_config'],
                                                                 test['input_data'])
                    self.assertEqual(test_config, test['output_config'])
                    if test['input_config']['type'] == 1 and test['input_config']['serialize'] == 1:
                        self.assertEqual(
                            test_data, pickle.dumps(test['input_data']))
                    elif test['input_config']['type'] == 1 and test[
                            'input_config']['serialize'] == 2:
                        self.assertEqual(test_data, json.dumps(
                            test['input_data']).encode('utf-8'))
                    elif test['input_config']['type'] == 1 and test[
                            'input_config']['serialize'] == 3:
                        self.assertEqual(
                            test_data, test['output_data'].encode('utf-8'))
                    elif test['input_config']['type'] == 2:
                        # delete file after test
                        try:
                            os.remove(f"\
{test['input_config']['txtfilepath']}_\
{time.strftime('%Y%m%d_%H%M%S', time.localtime())}.txt")
                        except FileNotFoundError:
                            pass
                        self.assertEqual(
                            test_data, test['input_data'].encode('utf-8'))

    def continue_input_test(self, test_inputs: list) -> tuple:
        """Mock for continue input."""
        with mock.patch('builtins.input', side_effect=test_inputs):
            start_point = client.continue_input()
        return start_point

    def test_continue(self):
        """Test for continue_input."""
        tests = [client_testcase.test_case_7, client_testcase.test_case_8,
                 client_testcase.test_case_9, client_testcase.test_case_10]
        for test in tests:
            with self.subTest(case=test['case']):
                start_point = self.continue_input_test(
                    test['input_data'])
                self.assertEqual(start_point, test['output_data'])


if __name__ == "__main__":
    unittest.main()
