#test for server.py
# one is required to change the values in the variables within a function to test
# if correct input is provided, the tests will run once the program is run
import unittest
import server

class servertests(unittest.TestCase):

    def test_initialize_server(self): 
        actual = server.initialize_server("localhost", 80,1)
        expected = "Listening on localhost:80"
        self.assertEqual(actual, expected)

    def test_receive_config(self):
        actual = server.receive_config(socket.socket,"localhost",3)
        expected = "Connected by localhost"
        self.assertEqual(actual, expected)

    def test_receive_data(self):
        actual = server.receive_data(socket.socket, 3)
        notExpected = "Connection Error on receiving data."
        self.assertNotEqual(actual, notExpected)

    def test_send_response(self):
        actual = server.send_response(socket.socket, "hello", 3)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_private_key(self):
        actual = server.get_private_key(3,"12345678fdfsd")
        expected = "12345678fdfsd"
        self.assertEqual(actual, expected)

    def test_print_dict(self):
        actual = server.print_dict("{one}:{1}")
        expected = "------------Start Dictionary Text Output------------\n{one}:{1}\n------------End Dictionary Text Output------------"
        self.assertEqual(actual, expected)

    def test_print_to_terminal(self):
        actual = server.print_to_terminal("testing testing")
        expected = "------------Start Output------------\ntesting testing\n------------End Output------------"
        self.assertEqual(actual, expected)

    def test_process_recv_data(self):
        actual = server.process_recv_data({one}:{1},
                        recv_data: bytes,
                        server_configuration: dict,
                        priv_key: rsa.PrivateKey = EXAMPLE_PRIV_KEY)
        expected = "'DATA_OK"
        self.assertEqual(actual, expected)

    def test_start_server(self):
        actual = server.start_server()
        expected = ""
        self.assertEqual(actual, expected)
