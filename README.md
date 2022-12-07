# Client-Server Network

> This repository is created as part of the Group Project Practical Assessment for University of Liverpool's CSCK541 Software Development in Practice Module (June 2022 A)

`cs_network` is a Python module that implements a client-server network protocol.

`tests` is a Python module that contains unit tests for the `cs_network` module.

`encryption` is a Python module that implements a simple encryption protocol using `rsa`.

## Table of Contents

- [Client-Server Network](#client-server-network)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Usage](#usage)
    - [Run the Server](#run-the-server)
      - [start_server Function](#start_server-function)
      - [Server Features](#server-features)
      - [Example Server Usage](#example-server-usage)
    - [Run the Client](#run-the-client)
      - [start_client Function](#start_client-function)
      - [Client Features](#client-features)
      - [Example Client Usage](#example-client-usage)
    - [Key Features](#key-features)
      - [Encryption](#encryption)
        - [Encrypt](#encrypt)
        - [Decrypt](#decrypt)
        - [Keygen](#keygen)
        - [Load Keys](#load-keys)
      - [Input Validation](#input-validation)
        - [Network Configuration](#network-configuration)
        - [User Configuration Input](#user-configuration-input)
        - [File Path Input](#file-path-input)
        - [Input Data Size](#input-data-size)
        - [XML data input](#xml-data-input)
      - [Nested Dictionaries](#nested-dictionaries)
      - [Serialization](#serialization)
  - [Tests](#tests)
    - [Unit Tests](#unit-tests)
      - [Usage: TestServer](#usage-testserver)
        - [Server unit tests performed](#server-unit-tests-performed)
      - [Usage: TestClient](#usage-testclient)
        - [Client unit tests performed](#client-unit-tests-performed)
  - [Repository Tree](#repository-tree)
  - [Contributing](#contributing)
    - [Contributors](#contributors)
  - [License](#license)

## Install

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the CSCK541 Client-Server Network using the following command:

```shell
pip install git+https://github.com/zhulinchng/CSCSK541.git
```

Re-run the above command to check for and install updates.

## Usage

### Run the Server

`start_server()` function from the `cs_network` module is used to start the server.

```shell
python
```

```python
>>> from cs_network import start_server
>>> start_server()
```

#### start_server Function

```python
def start_server(
                 timeout: Union[int,None] = None # Timeout for the server (seconds), default is None
                 ) -> None:                      # Return None
```

#### Server Features

- Supports decryption of messages using RSA.
- Output options:
  - File output
  - Terminal output

#### Example Server Usage

```ps1
>>> from cs_network import start_server
>>> start_server()
------------Enter network configuration------------
Enter the IPv4 host, or press enter to use EXAMPLE_PC:
Using default hostname: EXAMPLE_PC
Enter the port, or press enter for default port 50541:
Using default port: 50541
Listening on EXAMPLE_PC:50541
------------Enter server configuration------------
Output to file (1) or console (2): 2
Enter the private key .pem file path, or press Enter to use example key:
Using example private key.
------------Start Connection------------
Connected by ('192.168.1.138', 61032)
------------Start Output------------
'<root><testxmlkey>testxmlvalue</testxmlkey></root>'
------------End Output------------
Server closed.
```

### Run the Client

`start_client()` function from the `cs_network` module is used to start the client.

```shell
python
```

```python
>>> from cs_network import start_client
>>> start_client()
```

#### start_client Function

```python
def start_client(
                 timeout: Union[int,None] = None # Timeout for the client (seconds), default is None
                 ) -> None:                      # Return None
```

#### Client Features

- Supports encryption of messages using RSA.
- Supports dictionary and text input.
- Encrypted data are serialized to Binary.
- Plain dictionaries have the following serialization options:-
  - Binary
  - JSON
  - XML
- Supports nested dictionaries for dictionary input.
- Text input are saved to a file specified by the user.

#### Example Client Usage

```ps1
>>> from cs_network import start_client
>>> start_client()
------------Enter network configuration------------
Enter the IPv4 host, or press enter to use EXAMPLE_PC: 
Using default hostname: EXAMPLE_PC
Enter the port, or press enter for default port 50541: 
Using default port: 50541
---------Connection Initialized---------
------------Enter data configuration------------
Send a dictionary (1), or a text (2): 1
Encrypt (1) or not (2): 2
Select serialization method (1) Binary (2) JSON (3) XML: 3
Enter the key, or press Enter to finish:
---------Processing Data---------
Processing complete.
---------Sending Config---------
CONFIG_OK
---------Sending Data---------
Data processed successfully.--------- Continue? ---------
Do you want to continue? (y/n): n
Connection closed.
```

### Key Features

#### Encryption

The encryption module contains the following features:

##### Encrypt

The `encrypt` function is located within the `encryption` module.
It uses the encryption function within the `rsa` package.

```python
import rsa

def encrypt(message: str, public_key: rsa.PublicKey) -> bytes:
    """
    Encrypt a message with a public key.

    The RSA module only operates on bytes, and not on strings.
    So string is required to be encoded to bytes.

    :param message: The message to encrypt.
    :param public_key: The public key to encrypt with.
    :return: The encrypted message.
    """
    return rsa.encrypt(message.encode('utf8'), public_key)
```

##### Decrypt

The `decrypt` function is located within the `encryption` module.
It uses the decryption function within the `rsa` package.

```python
import rsa

def decrypt(data_bytes: bytes, private_key: rsa.PrivateKey) -> str:
    """
    Decrypt a message with a private key.

    The RSA module only operates on bytes, and not on strings.
    So string is required to be decoded.

    :param data_bytes: The message in bytes to decrypt.
    :param private_key: The private key to decrypt with.
    :return: The decrypted message.
    """
    return rsa.decrypt(data_bytes, private_key)
```

##### Keygen

The `encryption` module also contains the following functions relating to generating and saving encryption keys:-

- `generate_keys` is used to generate a pair of public and private key.

```python
import rsa

def generate_keys(keysize: int) -> tuple:
    """
    Generate a key for encryption.

    :param keysize: The size of the key.
    :return: A tuple containing the public and private keys.
    """
    return rsa.newkeys(keysize)
```

- `save_keys` is used to save a pair of public and private key to 2 separate files.

```python
import rsa

def save_keys(public_key: rsa.PublicKey,
              private_key: rsa.PrivateKey,
              filename: str) -> None:
    """
    Save the keys to a file.

    :param public_key: The public key from rsa.PublicKey.
    :param private_key: The private key from rsa.PrivateKey.
    :param filename: The filename to save the keys to.
    :return: None.
    """
    with open(f'{filename}_pub.pem', 'wb+') as file:
        file.write(rsa.PublicKey.save_pkcs1(public_key, format='PEM'))
    with open(f'{filename}_priv.pem', 'wb+') as file:
        file.write(rsa.PrivateKey.save_pkcs1(private_key, format='PEM'))
```

##### Load Keys

The `encryption` module also contains the following functions relating to loading encryption keys:-

- `load_pub_key` for loading a public key.

```python
import rsa

def load_pub_key(filename: str) -> tuple:
    """
    Load public key from a file.

    :param filename: The filename to load the key from.
    :return: The public key.
    """
    with open(f'{filename}', 'rb') as file:
        public = rsa.PublicKey.load_pkcs1(file.read(), format='PEM')
    return public
```

- `load_priv_key` for loading a private key.

```python
import rsa

def load_priv_key(filename: str) -> tuple:
    """
    Load public key from a file.

    :param filename: The filename to load the key from.
    :return: The public key.
    """
    with open(f'{filename}', 'rb') as file:
        private = rsa.PrivateKey.load_pkcs1(file.read(), format='PEM')
    return private
```

#### Input Validation

Validation are performed for each user input in the network configuration menu.
The following validation functions are used:-

##### Network Configuration

- `socket.gethostbyname(host)` for validating IPv4 hostname.
- `port < 0 or port > 65535` for validating port number.

##### User Configuration Input

Validation are performed for each user input in the configuration menu.
The following validation functions are used:-

- `validation` from cs_network\functions.py for validating integer inputs.
- `validate_empty_value` from cs_network\functions.py is to check for empty keys in a dictionary input.

##### File Path Input

- Public key files for encryption are validated by checking if the file exists using `os.path.exists`.
- Folder paths are validated by checking if the folder exists using `os.path.isdir`.
- File path length are limited to `255` characters.
- Valid characters are checked for the file path for characters within `string.ascii_letters`, `string.digits`, and `_.-`

##### Input Data Size

Size of the input data are checked using the `size_check` function within the `data_input` function from the cs_network/functions.py file.

Size checks are necessary as the size should not be larger than the size of the encryption key. (e.g., if the encryption key is 1024 bits, the size of the input data should not be larger than 1024 bits.)

##### XML data input

XML only supports a limited set of characters.
As such, the XML data input is checked for valid characters by parsing each input line and checking if the characters are valid using `xml.dom.minidom.parseString`.

#### Nested Dictionaries

Support for nested dictionaries are added, as it is often required to send a dictionary with a dictionary. (i.e., child nodes for XML serialization and JSON serialization.)

If the syntax of the dictionary is not correct, the program will treat the input as string.

#### Serialization

**Binary** serialization is used for encrypted data (i.e., text and dictionary) and plain dictionary.
It is serialized using the built-in `pickle` module.

**JSON** serialization is used for plain dictionary inputs only using the built-in `json` module.

**XML** serialization is used for plain dictionary inputs only using the built-in `xml.etree.ElementTree` module.

## Tests

### Unit Tests

#### Usage: TestServer

```python
>>> import unittest
>>> from tests import TestServer
>>> unittest.main()
```

Unit test results for server are printed to the console: [Sample of the result](docs/server_unittest.md)

##### Server unit tests performed

- Test 1: Network configuration input tests are mocked and tested.
- Test 2: Server configuration input tests are mocked and tested.
- Test 3: Private key input tests are mocked and tested.
- Processing of data are tested for each type of output (file, terminal):-
  - Test 4: Encrypted input are tested to ensure data is decrypted correctly.
  - Test 5: Plain input are tested to ensure data is deserialized correctly.

#### Usage: TestClient

```python
>>> import unittest
>>> from tests import TestClient
>>> unittest.main()
```

Unit test results for client are printed to the console: [Sample of the result](docs/client_unittest.md)

##### Client unit tests performed

- Test 1: Network configuration input tests are mocked and tested.
- Test 2: Configuration input and data for encrypted dictionary tests are mocked and tested.
- Test 3: Configuration input and data for plain dictionary tests are mocked and tested for each serialization type.
- Test 4: Configuration and data input for encrypted text tests are mocked and tested.
- Test 5: Configuration and data input for plain text tests are mocked and tested.
- Test 6: Processing data tests are performed for each type of inputs.
- Test 7: Mock and tested for `continue()` function in the client.

## Repository Tree

```bash
CSCK541
│   .gitignore
│   LICENSE
│   README.md
│   requirements.txt
│   setup.py
│   
├───cs_network
│       client.py
│       functions.py
│       server.py
│       __init__.py
│       
├───docs
│       client_unittest.md
│       Context Diagram.drawio
│       Context Diagram.drawio.png
│       Context Diagram.drawio.svg
│       server_unittest.md
│
├───encryption
│   │   cipher.py
│   │   keygen.py
│   │   __init__.py
│   │
│   └───example_keys
│           keys_2048_priv.pem
│           keys_2048_pub.pem
│
└───tests
        client_test.py
        server_test.py
        testcase.py
        __init__.py
```

## Contributing

Pull requests are welcome. For major changes, open an issue to discuss beforehand.

### Contributors

This project is created as a collaboration between the following students for the ***CSCK541 Group Project***:

- [Alketbi, Mohamed](https://github.com/malktbi)
- [Phiri, Lunzitsani Gerald](https://github.com/lunziphiri)
- [Obaje, Vanessa](https://github.com/lachocella)

## License

[MIT License](LICENSE)
