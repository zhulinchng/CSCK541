"""Unit test for client."""
import sys
import time
import pickle
import unittest
from unittest import mock
from io import StringIO
import codecs
import json
import os
from os.path import dirname, join, abspath
import xml.etree.ElementTree as ET
import rsa
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from tests import testcase
from encryption import EXAMPLE_PUB_KEY, EXAMPLE_PRIV_KEY
from cs_network import server, process_data


class TestServer(unittest.TestCase):
    """Unit test for client."""

    def server_netconf_input_test(self, test_inputs: list) -> tuple:
        """
        Mock input for server network_config.

        :param test_inputs: list of inputs for network_config.
        :return: tuple of host and port.
        """
        test_inputs = [str(x) for x in test_inputs]
        with mock.patch('builtins.input', side_effect=test_inputs):
            host, port = server.network_config()
        return host, port

    def test_network_config(self):
        "Test server network_config."
        host, port = self.server_netconf_input_test(["localhost", "12345"])
        self.assertEqual(host, "localhost")
        self.assertEqual(port, 12345)

    def server_config_input_test(self, test_inputs: list) -> dict:
        """
        Mock input_data for server config.

        :param test_inputs: list of inputs for server config.
        :return: dictionary of server config."""
        test_inputs = [str(x) for x in test_inputs]
        with mock.patch('builtins.input', side_effect=test_inputs):
            serv_conf = server.server_config()
        return serv_conf

    def test_server_config(self):
        """Test server config."""
        tests = [testcase.server_case_1, testcase.server_case_2]
        for test in tests:
            with self.subTest(case=test['case']):
                serv_conf = self.server_config_input_test(
                    test['input'])
                self.assertEqual(serv_conf, test['output_config'])

    def server_key_input_test(self, test_inputs: list) -> rsa.PrivateKey:
        """
        Mock input_data for getting server private key.

        :param test_inputs: list of inputs for getting server private key.
        :return: tuple of server private key and server public key."""
        test_inputs = [str(x) for x in test_inputs]
        with mock.patch('builtins.input', side_effect=test_inputs):
            priv_key = server.get_private_key()
        return priv_key

    def test_get_private_key(self):
        """Test get_private_key."""
        test = {'input': [''], 'output_key': EXAMPLE_PRIV_KEY}
        priv_key = self.server_key_input_test(
            test['input'])
        self.assertEqual(priv_key, test['output_key'])

    @mock.patch('sys.stdout', new_callable=StringIO)
    def server_process_test(self, test_inputs: tuple, mock_stdout: StringIO) -> tuple:
        """
        Mock input_data for processing data.

        :param test_inputs: tuple of input_config, input_data, server_config.
        :param mock_stdout: status message and terminal output.
        """
        outputs = []
        config = test_inputs[0]
        data = test_inputs[1]
        serv_conf = test_inputs[2]
        status_msg = server.process_recv_data(
            config, data, serv_conf, priv_key=EXAMPLE_PRIV_KEY)
        outputs.append(mock_stdout.getvalue())
        return status_msg, outputs[0].split("\n")

    def test_process_encrypted_data(self):
        "Test for encrypted data."
        testcase.test_case_1['input_config']['case'] = 'Encrypted dictionary: '
        testcase.test_case_1['input_config']['public_key'] = EXAMPLE_PUB_KEY
        testcase.test_case_1['input_config']['serialize'] = 1
        testcase.test_case_5['input_config']['case'] = 'Encrypted text: '
        testcase.test_case_5['input_config']['public_key'] = EXAMPLE_PUB_KEY
        testcase.test_case_5['input_config']['serialize'] = None
        testcase.test_case_5['input_config'][
            'txtfilepath'] = f'{testcase.test_case_5["input_config"]["txtfilepath"]}\
\\{testcase.test_case_5["input_config"]["txtfilename"]}'

        tests = [testcase.test_case_1, testcase.test_case_5]
        serv_confs = [testcase.server_case_1['output_config'],
                      testcase.server_case_2['output_config']]
        tcs = []
        for test in tests:
            time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
            test_config, test_data = process_data(test['input_config'],
                                                  test['input_data'])
            for serv_conf in serv_confs:
                case = test['input_config']['case']
                if serv_conf['output_method'] == 1:
                    case += ': file output'
                else:
                    case += ': console output'
                tcs.append(
                    (case,
                     (test_config, test_data, serv_conf),
                     test))
                case = ''
        for test in tcs:
            with self.subTest(case=test[0]):
                status_msg, outputs = self.server_process_test(test[1])
                self.assertEqual(status_msg, 'DATA_OK')
                if 'file output' in test[0]:
                    # delete client output file
                    try:
                        os.remove(
                            f"{test[2]['input_config']['txtfilepath']}_{time1}.txt")
                    except (FileNotFoundError, KeyError, OSError):
                        pass
                    if 'Data written to ' in outputs[1]:
                        server_output = outputs[1].replace(
                            'Data written to ', '')
                        filepath = codecs.decode(
                            server_output, 'unicode_escape')[1:][:-1]
                        if test[2]['output_config']['serialize'] is None:
                            with open(filepath, 'r', encoding='utf-8') as file:
                                self.assertEqual(
                                    file.read(), test[2]['input_data'])
                        elif test[2]['output_config']['serialize'] == 1:
                            with open(filepath, 'rb') as file:
                                self.assertEqual(
                                    pickle.load(file), repr(test[2]['input_data']))
                elif 'console output' in test[0]:
                    # Test for terminal output
                    self.assertEqual(
                        outputs, test[2]['term_out'])
                try:
                    path = codecs.decode(
                        server_output, 'unicode_escape')[1:][:-1]
                    os.remove(path)
                except (FileNotFoundError, OSError):
                    pass
        return

    def test_process_plain_data(self):
        """Test for plain data."""
        testcase.test_case_6['output_config']['txtfilepath'] = None
        tests = [testcase.test_case_6, testcase.test_case_2,
                 testcase.test_case_3, testcase.test_case_4]
        serv_confs = [testcase.server_case_1['output_config'],
                      testcase.server_case_2['output_config']]
        tcs = []
        for test in tests:
            test_config, test_data = process_data(test['output_config'],
                                                  test['input_data'])
            for serv_conf in serv_confs:
                case = test['case']
                if serv_conf['output_method'] == 1:
                    case += ': file output'
                else:
                    case += ': console output'
                tcs.append(
                    (case,
                     (test_config, test_data, serv_conf),
                     test))
                case = ''
        for test in tcs:
            with self.subTest(case=test[0]):
                status_msg, outputs = self.server_process_test(test[1])
                self.assertEqual(status_msg, 'DATA_OK')
                if 'file output' in test[0]:
                    server_output = outputs[1].replace('Data written to ', '')
                    filepath = codecs.decode(
                        server_output, 'unicode_escape')[1:][:-1]
                    if test[2]['output_config']['serialize'] is None:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            self.assertEqual(
                                file.read(), test[2]['input_data'])
                    elif test[2]['output_config']['serialize'] == 1:
                        with open(filepath, 'rb') as file:
                            self.assertEqual(
                                pickle.load(file), test[2]['input_data'])
                    elif test[2]['output_config']['serialize'] == 2:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            self.assertEqual(
                                json.load(file), test[2]['input_data'])
                    elif test[2]['output_config']['serialize'] == 3:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            # print(ET.tostring(ET.fromstring(test[2]['output_data'])))
                            self.assertEqual(
                                ET.tostring(ET.parse(filepath).getroot()).decode(
                                    'utf-8').replace('\n', '').replace('\t', ''),
                                test[2]['output_data'])
                    try:
                        os.remove(filepath)
                    except (FileNotFoundError, OSError):
                        pass
                elif 'console output' in test[0]:
                    self.assertEqual(outputs,
                                     test[2]['term_out'])


if __name__ == "__main__":
    unittest.main()
