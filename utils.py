import os
import time

def validate_input(ENCRYPTED_FILES_PATH, user_input):
    splitted_input = user_input.split()

    if (len(splitted_input) < 2):
        print('Invalid command!')
        return False
    
    command = splitted_input[0]
    file_path = splitted_input[1]
    
    if(command != 'add'
       and command != 'open'
       and command != 'del'):
        print('Invalid command!')
        return False
    elif ((command == 'add' and not os.path.exists(file_path))):
        print(f'File {file_path} does not exist!')
        return False
    elif ((command == 'add' and os.path.exists(ENCRYPTED_FILES_PATH + file_path))):
        print(f'File {file_path} already exists in the prison realm!')
        return False
    elif ((command == 'open' or command == 'del') and not os.path.exists(ENCRYPTED_FILES_PATH + file_path + '.ura')):
        print(f'File {file_path} does not exist in the prison realm!')
        return False
    else:
        return True
    
def cmdRed():
    os.system('color 0c')

    time.sleep(2)

    os.system('color 07')
    os.system('cls')

def cmdGreen():
    os.system('color 0a')

    time.sleep(2)

    os.system('color 07')
    os.system('cls')