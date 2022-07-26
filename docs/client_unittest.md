# Client Unit Test Output

```python
>>> import unittest
>>> from tests import TestClient
>>> unittest.main()
------------Starting from Input Config------------
------------Starting from Input Data------------
------------Exiting------------
.------------Enter data configuration------------
Using example public key
Serialization method will default to binary for encrypted dictionary.
------------Enter data------------
Maximum data size: 245 bytes
Enter the dictionary:

---Tip: The value can be another dictionary---

If entered using the correct python syntax, the value will be evaluated as a nested dictionary, otherwise it will be string.

Dictionary: {'encryptedkey': 'encryptedvalue'}
Size: 47 bytes
Dictionary: {'encryptedkey': 'encryptedvalue', '123': '456'}
Size: 60 bytes
Dictionary: {'encryptedkey': 'encryptedvalue', '123': '456', 'nested_dict': {'nest': 'value'}}
Size: 92 bytes
.------------Enter data configuration------------
Using example public key
------------Enter data------------
Maximum data size: 245 bytes
Enter the text data:
.------------Enter data configuration------------
------------Enter data------------
Maximum data size: 245 bytes
Enter the dictionary:

---Tip: The value can be another dictionary---

If entered using the correct python syntax, the value will be evaluated as a nested dictionary, otherwise it will be string.

Dictionary: {'testkey': 'testvalue'}
Size: 37 bytes
Dictionary: {'testkey': 'testvalue', '123': '456'}
Size: 50 bytes
Dictionary: {'testkey': 'testvalue', '123': '456', 'nested_dict': {'nest': 'value'}}
Size: 82 bytes
------------Enter data configuration------------
------------Enter data------------
Maximum data size: 245 bytes
Enter the dictionary:

---Tip: The value can be another dictionary---

If entered using the correct python syntax, the value will be evaluated as a nested dictionary, otherwise it will be string.

Dictionary: {'testkey': 'testvalue'}
Size: 24 bytes
Dictionary: {'testkey': 'testvalue', '123': '456'}
Size: 38 bytes
Dictionary: {'testkey': 'testvalue', '123': '456', 'nested_dict': {'nest': 'value'}}
Size: 72 bytes
------------Enter data configuration------------
------------Enter data------------
Maximum data size: 245 bytes
Enter the dictionary:

---Tip: The value can be another dictionary---

If entered using the correct python syntax, the value will be evaluated as a nested dictionary, otherwise it will be string.

Dictionary: {'testkey': 'testvalue'}
Size: 41 bytes
Dictionary: {'testkey': 'testvalue', 'a123': '456'}
Size: 57 bytes
Dictionary: {'testkey': 'testvalue', 'a123': '456', 'nested_dict': {'nest': {'nest2': 'value'}}}
Size: 117 bytes
.------------Enter data configuration------------
------------Enter data------------
Maximum data size: 245 bytes
Enter the text data:
.------------Enter network configuration------------
.Data written successfully to .csck541_test\venv\lib\site-packages\tests\client_test_output_20220725_222837.txt
Data written successfully to .csck541_test\venv\lib\site-packages\tests\client_test_output_20220725_222837.txt
.
----------------------------------------------------------------------
Ran 7 tests in 0.026s

OK
```
