import hashlib
import secrets
import string
import os
import pyperclip
from getpass import getpass as input_password

from utils import cmdRed, cmdGreen

def _encrypt_data(data, key):
    data = key + data + key

    data_characters = list(data)
    key_characters = list(key)

    # Convert key characers to their ASCII values and get sum
    key_sum = 0
    for index, character in enumerate(key_characters):
        key_characters[index] = ord(character)

        key_sum += key_characters[index]
    key_sum = key_sum % 127

    encrypted_data = ''
    key_characters_index = 0
    for character in data_characters:
        encrypted_data += chr((ord(character) + key_sum + key_characters[key_characters_index]) % 127)

        key_characters_index += 1
        if key_characters_index == len(key_characters):
            key_characters_index = 0

    return encrypted_data

def add_file(ENCRYPTED_FILES_PATH, file_path):
    password = input_password(prompt='Enter your password: ')
    if (password != input_password(prompt='Confirm your password: ')):
        print('Wrong input!')
        cmdRed()

    # generate a random salt
    characters = string.ascii_letters + string.digits
    salt = ''.join(secrets.choice(characters) for _ in range(64))

    encrypted_data = None
    encryption_key = None

    with open(file_path, 'r') as file:
        file_content = file.read()

        encryption_key = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

        encrypted_data = _encrypt_data(file_content, encryption_key)

    try:
        file_name = os.path.splitext(file_path)[0]

        with open(ENCRYPTED_FILES_PATH + file_name + '.ura', 'x') as file:
            file.write(encryption_key + ' ' + salt + "\n" + encrypted_data)

        print(f"\nFile '{file_path}' has been added to the prison realm.")
        os.remove(file_path)
        cmdGreen()
    except FileExistsError:
        print(f"\nFile '{file_name}' already exists in the prison realm.")
    return


def _decrypt_data(data, key):
    data_characters = list(data)
    key_characters = list(key)

    # Convert key characers to their ASCII values and get sum
    key_sum = 0
    for index, character in enumerate(key_characters):
        key_characters[index] = ord(character)

        key_sum += key_characters[index]
    key_sum = key_sum % 127

    decrypted_data = ''
    key_characters_index = 0
    for character in data_characters:
        decrypted_data += chr((ord(character) - key_sum - key_characters[key_characters_index] + 254) % 127)

        key_characters_index += 1
        if key_characters_index == len(key_characters):
            key_characters_index = 0

    return decrypted_data

def open_file(ENCRYPTED_FILES_PATH, file_name) -> int:
    password = input_password(prompt='Enter password: ')

    file_path = ENCRYPTED_FILES_PATH + file_name + '.ura'

    decrypted_data = None
    with open(file_path, 'r') as file:
        file_content = file.read()
        
        newline_index = file_content.find('\n')

        encryption_key, salt = file_content[:newline_index].split()

        encrypted_data = file_content[newline_index + 1:]

        decryption_key = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

        if (encryption_key != decryption_key):
            print('Wrong password!')
            cmdRed()
            return 1

        decrypted_data = _decrypt_data(encrypted_data, decryption_key)[len(decryption_key):-len(decryption_key)]
        
        pyperclip.copy(decrypted_data)

    # reencryption part
    # generate a new random salt
    characters = string.ascii_letters + string.digits
    new_salt = ''.join(secrets.choice(characters) for _ in range(64))

    new_encryption_key = hashlib.sha256((new_salt + password).encode('utf-8')).hexdigest()

    encrypted_data = _encrypt_data(decrypted_data, new_encryption_key)

    with open(file_path, 'w') as file:
        file.write(new_encryption_key + ' ' + new_salt + "\n" + encrypted_data)

    print('\nFile content copied to clipboard.')
    cmdGreen()
    return 0