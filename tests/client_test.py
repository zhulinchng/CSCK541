"""Unit test for client."""
import sys
import time
import pickle
import unittest
from unittest import mock
from io import StringIO
import os
from os.path import dirname, join, abspath
import rsa
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from tests import client_testcase
from encryption import EXAMPLE_PUB_KEY, EXAMPLE_PRIV_KEY
from cs_network import client

class TestClient(unittest.TestCase):
    """Unit test for client."""

    @mock.patch('sys.stdout', new_callable=StringIO)
    def client_input_test(self, test_inputs: list, mock_stdout: StringIO) -> str:
        """Test input_data."""
        outputs = []
        test_inputs = [str(x) for x in test_inputs]
        with mock.patch('builtins.input', side_effect=test_inputs):
            config, data = client.input_data({}, {})
            outputs.append(mock_stdout.getvalue())
        return config, data, outputs[0].split("\n")

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

    def test_input_1(self):
        """Encrypted dictionary input test case."""

        config, data, stdout = self.client_input_test(client_testcase.input_1)
        config = self.del_none_from_dict(config)
        client_testcase.input_1_config['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.input_1_config['serialize'] = 1
        self.assertEqual(config, client_testcase.input_1_config)
        self.assertEqual(data, client_testcase.input_1_data)

    def test_input_2(self):
        """
        Plain dictionary input test case.
        Using binary serialization.
        """

        config, data, stdout = self.client_input_test(client_testcase.input_2)
        config = self.del_none_from_dict(config)
        self.assertEqual(config, client_testcase.input_2_config)
        self.assertEqual(data, client_testcase.input_2_data)

    def test_input_3(self):
        """
        Plain dictionary input test case.
        Using JSON serialization.
        """

        config, data, stdout = self.client_input_test(client_testcase.input_3)
        config = self.del_none_from_dict(config)
        self.assertEqual(config, client_testcase.input_3_config)
        self.assertEqual(data, client_testcase.input_3_data)

    def test_input_4(self):
        """
        Plain dictionary input test case.
        Using XML serialization.
        """

        config, data, stdout = self.client_input_test(client_testcase.input_4)
        config = self.del_none_from_dict(config)
        self.assertEqual(config, client_testcase.input_4_config)
        self.assertEqual(data, client_testcase.input_4_data)

    def test_input_5(self):
        """Encrypted text test case."""

        config, data, stdout = self.client_input_test(client_testcase.input_5)
        client_testcase.input_5_config[
            'txtfilepath'] = f'{client_testcase.input_5_config["txtfilepath"]}\
\\{client_testcase.input_5_config["txtfilename"]}'
        del client_testcase.input_5_config['txtfilename']
        client_testcase.input_5_config['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.input_5_config['serialize'] = None
        self.assertEqual(config, client_testcase.input_5_config)
        self.assertEqual(data, client_testcase.INPUT_5_DATA)

    def test_input_6(self):
        """Plain text test case."""

        config, data, stdout = self.client_input_test(client_testcase.input_6)
        client_testcase.input_6_config[
            'txtfilepath'] = f'{client_testcase.input_6_config["txtfilepath"]}\
\\{client_testcase.input_6_config["txtfilename"]}'
        del client_testcase.input_6_config['txtfilename']
        client_testcase.input_6_config['public_key'] = None
        client_testcase.input_6_config['serialize'] = None
        self.assertEqual(config, client_testcase.input_6_config)
        self.assertEqual(data, client_testcase.INPUT_6_DATA)

# _{time.strftime("%Y%m%d_%H%M%S", time.localtime())}.txt
    def test_process(self):
        """Test for process_data."""
        client_testcase.test_case_1['input_config']['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.test_case_1['input_config']['serialize'] = 1
        client_testcase.test_case_5['input_config']['public_key'] = EXAMPLE_PUB_KEY
        client_testcase.test_case_5['input_config']['serialize'] = None

        tests = [client_testcase.test_case_1, client_testcase.test_case_5]
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
                # elif test['input_config']['encrypt'] == 2:
                #     test_config, test_data = client.process_data(test['input_config'],
                #                                                 test['input_data'])
                #     self.assertEqual(test_config, test['output_config'])
                #     if test['input_config']['type'] == 1:
                #         self.assertEqual(pickle.loads(test_data), test['input_data'])
                #     elif test['input_config']['type'] == 2:
                #         # delete file after test
                #         os.remove(f"{test['input_config']['txtfilepath']}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}.txt")
                #         self.assertEqual(test_data, test['input_data'])

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
