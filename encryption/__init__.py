"""Package installation file for the encryption package."""
from os.path import dirname
from .keygen import generate_keys, save_keys, load_priv_key, load_pub_key
from .cipher import encrypt, decrypt

EXAMPLE_PUB_KEY = load_pub_key(
    f'{dirname(__file__)}\\example_keys\\keys_2048_pub.pem')
EXAMPLE_PRIV_KEY = load_priv_key(
    f'{dirname(__file__)}\\example_keys\\keys_2048_priv.pem')
