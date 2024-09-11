import pygame
import json

from functions.algorithms.hashPassword import hashPassword
from classes.global_data import constants_structure
constants = constants_structure()


def do_log_in(username, password):
    hashed_password = hashPassword(password)
    
    with open(constants.FILE_PATH + "data/accounts.json", 'r') as accountsFile:
        accounts = json.load(accountsFile)
        
    for account in accounts:
        if account["username"] == username   and   account["hashed_password"] == hashed_password: # Main login check
            return {"returnType": 1,
                    "account_details": account}
    # if at this point, the account does not exist
    return {"returnType": -1,
            "returnMessage": "Sorry, your username or password is incorrect"}