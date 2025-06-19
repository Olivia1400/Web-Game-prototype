import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def decrypt():
    # Load the private key from the file
    with open('private_key.pem', 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    
    encrypted_file_path = 'openAIKeyEncrypted.txt'
    if not os.path.exists(encrypted_file_path):
        print(f"Encrypted file '{encrypted_file_path}' does not exist.")
        return
    
    # Read the ciphertext back from the file
    with open(encrypted_file_path, 'rb') as encrypted_file:
        ciphertext_from_file = encrypted_file.read()
    
    try:
        # Decrypt the ciphertext read from the file
        decrypted_data = private_key.decrypt(
            ciphertext_from_file,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return (decrypted_data.decode('utf-8'))
    except Exception as e:
        print(f"Decryption failed: {e}")

