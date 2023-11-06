import os

from utils import validate_input, cmdRed
from commands import add_file, open_file

ENCRYPTED_FILES_PATH = 'ura/'

while True:
    # check if the encrypted files path folder exists
    if (not os.path.exists(ENCRYPTED_FILES_PATH)):
        os.makedirs(ENCRYPTED_FILES_PATH)

    # get all encrypted files from the encrypted files path folder
    encrypted_files = []
    for file in os.listdir(ENCRYPTED_FILES_PATH):
        file_name, extension = os.path.splitext(file)

        if (extension == '.ura'):
            encrypted_files.append(file_name)

    message = (
        "Welcome to Gokumonkyo password manager!\n\n" +
        "encrypted files:\n"
    )

    # check if encrypted files path folder has encrypted files
    if (len(encrypted_files) > 0):
        for index, file_name in enumerate(encrypted_files):
            message += str(index + 1) + ". " + file_name
    else:
        message += "none"

    message += (
        "\n\n" +
        "available commands:\n" +
        "- add <file_name>.txt\n" +
        "- open <file_name>\n\n"
    )

    user_input = input(message)
    print()

    if (not validate_input(ENCRYPTED_FILES_PATH, user_input)):
        cmdRed()
    else:
        command, file = user_input.split()

        if (command == 'add'):
            add_file(ENCRYPTED_FILES_PATH, file)
        else:
            if (open_file(ENCRYPTED_FILES_PATH, file) == 0):
                break