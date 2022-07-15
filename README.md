# Client-Server Network

> This repository is created as part of the Practical Assessment for University of Liverpool's CSCK541 Software Development in Practice Module (June 2022 A)

`cs_network` is a Python module that implements a client-server network protocol.

`encryption` is a Python module that implements a simple encryption protocol using RSA.

## Table of Contents

- [Client-Server Network](#client-server-network)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Usage](#usage)
    - [Functions for CSCK541 module](#functions-for-csck541-module)
    - [Miscellaneous Functions](#miscellaneous-functions)
      - [Encryption](#encryption)
      - [XML Serialization](#xml-serialization)
  - [Tests](#tests)
    - [Unit Tests](#unit-tests)
    - [Performance tests](#performance-tests)
      - [Results](#results)
  - [Repository Tree](#repository-tree)
  - [Contributing](#contributing)
  - [License](#license)

## Install

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Floyd Warshall Algorithm using the following command:

```shell
pip install git+https://github.com/zhulinchng/CSCSK541.git
```

Re-run the above command to check for and install updates.

## Usage

### Functions for CSCK541 module

placeholder explanation

```shell
python
```

```python
>>> from cs_network import start_server
>>> start_server
```

### Miscellaneous Functions

#### Encryption

#### XML Serialization

## Tests

### Unit Tests

placeholder

```python
>>> import unittest
>>> from tests import TestFloydWarshall
>>> unittest.main()
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

Results are printed to the console: [Sample of the result](placeholder)

### Performance tests

placeholder
Functions:

- `placeholder` -> explanation

#### Results

Results are printed to the console.

[Explanation and a sample of the result](placeholder)

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
│       Context Diagram.drawio
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
```

## Contributing

Pull requests are welcome. For major changes, open an issue to discuss beforehand.

## License

[MIT License](LICENSE)
