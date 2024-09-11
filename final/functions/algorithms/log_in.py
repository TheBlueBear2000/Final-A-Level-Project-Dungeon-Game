import json

from functions.algorithms.hashPassword import hashPassword
from classes.global_data import constants_structure
constants = constants_structure()

def do_log_in(username, password):
    # Hash password
    hashed_password = hashPassword(password)
    
    # Open accounts file
    with open(constants.FILE_PATH + "data/accounts.json", 'r') as accountsFile:
        accounts = json.load(accountsFile)
        
    for account in accounts: # Check each account with a linear search 
                            # (the list is not sorted by either username or password, so no other kind is possible)
        # Main login check
        if account["username"] == username   and   account["hashed_password"] == hashed_password: 
            return {"returnType": 1,
                    "account_details": account}
            
    # If at this point, the account does not exist
    return {"returnType": -1,
            "returnMessage": "Sorry, your username or password is incorrect"}
