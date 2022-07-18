#test for server.py
import pytest
import server

def test_initialize_server(): 
    initialization = server.initialize_server("localhost", 80,1)
    print(initialization)

def test_receive_config():
    configs = server.receive_config(socket.socket,"localhost",3)
    print (configs)

def test_receive_data():
    receive_data = server.receive_data(socket.socket, 3)
    print (receive_data)

def test_send_response():
    send_response = server.send_response(socket.socket, "hello", 3)
    print (send_response)

def test_get_private_key():
    get_private_key = server.get_private_key(3,"12345678fdfsd")
    print(get_private_key)

def test_print_dict():
    print_dict = server.print_dict({one}:{1}))
    print(print_dict)

def test_print_to_terminal():
    print_to_terminal = server.print_to_terminal("testing testing")
    print(print_to_terminal)

def test_process_recv_data():
    process_recv_data = server.process_recv_data({one}:{1},
                      recv_data: bytes,
                      server_configuration: dict,
                      priv_key: rsa.PrivateKey = EXAMPLE_PRIV_KEY)
    print (process_recv_data)

def test_start_server():
    server_started = server.start_server()
    print server_started
