"""Functions to encrypt and decrypt messages with a public and private key."""
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


if __name__ == "__main__":
    TEST = "Hello World!"
    pub_key, priv_key = rsa.newkeys(1024)
    encrypted = encrypt(TEST, pub_key)
    decrypted = decrypt(encrypted, priv_key)
    print(f"Message: {TEST}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    assert TEST == decrypted, "Decrypted message does not match"
