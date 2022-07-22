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
import rsa
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from tests.testcase import test_case_1, test_case_5
from tests import testcase
from encryption import EXAMPLE_PUB_KEY, EXAMPLE_PRIV_KEY
from cs_network import server, process_data


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

    def server_config_input_test(self, test_inputs: list) -> tuple:
        """Mock input_data."""
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

    def server_key_input_test(self, test_inputs: list) -> tuple:
        """Mock input_data."""
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
        """Mock input_data."""
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
        test_case_1['input_config']['case'] = 'Encrypted dictionary: '
        test_case_1['input_config']['public_key'] = EXAMPLE_PUB_KEY
        test_case_1['input_config']['serialize'] = 1
        test_case_5['input_config']['case'] = 'Encrypted text: '
        test_case_5['input_config']['public_key'] = EXAMPLE_PUB_KEY
        test_case_5['input_config']['serialize'] = None
        test_case_5['input_config'][
            'txtfilepath'] = f'{test_case_5["input_config"]["txtfilepath"]}\
\\{test_case_5["input_config"]["txtfilename"]}'

        tests = [test_case_1, test_case_5]
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
                    case += 'file output'
                else:
                    case += 'console output'
                tcs.append(
                    (case, (test_config, test_data, serv_conf),
                     test))
                case = ''
        for test in tcs:
            with self.subTest(case=test[0]):
                time2 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
                status_msg, outputs = self.server_process_test(test[1])
                if 'file output' in test[0]:
                    # delete client output file
                    try:
                        os.remove(
                            f"{test[2]['input_config']['txtfilepath']}_{time1}.txt")
                    except (FileNotFoundError, KeyError, OSError):
                        pass
                    if 'Data written to ' in outputs[1]:
                        server_output = outputs[1].replace('Data written to ', '')
                        if test[2]['output_config']['serialize'] is None:
                            filepath = codecs.decode(server_output, 'unicode_escape')[1:][:-1]
                            with open(filepath, 'r', encoding='utf-8') as f:
                                self.assertEqual(
                                    f.read(), test[2]['input_data'])
                        elif test[2]['output_config']['serialize'] == 1:
                            filepath = codecs.decode(
                                server_output, 'unicode_escape')[1:][:-1]
                            with open(filepath, 'rb') as f:
                                self.assertEqual(
                                    pickle.load(f), repr(test[2]['input_data']))
                elif 'console output' in test[0]:
                    # Test for terminal output
                    self.assertEqual(
                        outputs, test[2]['term_out'])
                self.assertEqual(status_msg, 'DATA_OK')
                try:
                    path = codecs.decode(
                        server_output, 'unicode_escape')[1:][:-1]
                    os.remove(path)
                except (FileNotFoundError, OSError):
                    pass
        return

    # def test_process_decrypted_data(self):



if __name__ == "__main__":
    unittest.main()
