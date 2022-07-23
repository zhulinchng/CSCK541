"""Functions to generate keys for asymmetric encryption."""
import rsa


def generate_keys(keysize: int) -> tuple:
    """
    Generate a key for encryption.

    :param keysize: The size of the key.
    :return: A tuple containing the public and private keys.
    """
    return rsa.newkeys(keysize)


def save_keys(public_key: rsa.PublicKey, private_key: rsa.PrivateKey, filename: str) -> None:
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


def load_pub_key(filename: str) -> tuple:
    """
    Load public key from a file.

    :param filename: The filename to load the key from.
    :return: The public key.
    """
    with open(f'{filename}', 'rb') as file:
        public = rsa.PublicKey.load_pkcs1(file.read(), format='PEM')
    return public


def load_priv_key(filename: str) -> tuple:
    """
    Load public key from a file.

    :param filename: The filename to load the key from.
    :return: The public key.
    """
    with open(f'{filename}', 'rb') as file:
        private = rsa.PrivateKey.load_pkcs1(file.read(), format='PEM')
    return private


if __name__ == '__main__':
    from os.path import dirname
    keysizes = [2048]
    FOLDER = f'{dirname(__file__)}\\example_keys'
    for size in keysizes:
        pub_key, priv_key = generate_keys(size)
        save_keys(pub_key, priv_key, f'{FOLDER}\\keys_{size}')
        load_pub_key = load_pub_key(f'{FOLDER}\\testkeys_{size}_pub.pem')
        load_priv_key = load_priv_key(f'{FOLDER}\\testkeys_{size}_priv.pem')
        assert pub_key == load_pub_key, "Public keys do not match"
        assert priv_key == load_priv_key, "Private keys do not match"
        print("Keys generated and loaded successfully")
