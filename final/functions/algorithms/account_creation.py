import pygame
import json

from functions.algorithms.hashPassword import hashPassword
from classes.global_data import constants_structure
constants = constants_structure()

def addAccount(inputUsername, inputPassword, inputPasswordOne, inputDisplayName, inputImageURL):
    # PASSWORD VALIDATION
    # Passwords match
	if inputPassword != inputPasswordOne:
		return {"returnType": -1, 
				"returnMessage": "Passwords do not match"}

    # Password too short
	elif len(inputPassword) < 8:
		return {"returnType": -1,
				"returnMessage": "Password is too short (min 8)"}

    # Password too long
	elif len(inputPassword) > 30:
		return {"returnType": -1,
				"returnMessage": "Password is too long (max 30)"}
    
    # Password does not have digit
	elif not any(char.isdigit() for char in inputPassword):
		return {"returnType": -1,
				"returnMessage": "Password needs to contain a digit"}

    # Password does not have lowercase character
	elif not any(char.islower() for char in inputPassword):
		return {"returnType": -1,
				"returnMessage": "Password needs to contain a lowercase character"}

    # Password does not have uppercase character
	elif not any(char.isupper() for char in inputPassword):
		return {"returnType": -1,
				"returnMessage": "Password needs to contain an uppercase character"}


    # USERNAME VALIDATION
    # Username too short
	elif len(inputUsername) < 3:
		return {"returnType": -1,
				"returnMessage": "Username is too short (min 3)"}

    # Username too long
	elif len(inputUsername) > 16:
		return {"returnType": -1,
				"returnMessage": "Username is too long (max 16)"}

    # Username contains special characters
	elif any(not(c.isalpha() or c.isdigit()) for c in inputUsername):
		return {"returnType": -1,
				"returnMessage": "Usernames cannot contain special characters (only A-Z, a-z and 0-9)"}

    # Username already exists (also gather current highest UUID)
	highestUUID = 0
	for account in json.load(open(constants.FILE_PATH + "data/accounts.json", 'r')):
		highestUUID = max(highestUUID, account["UUID"])
		if account["username"] == inputUsername:
			return {"returnType": -1,
				"returnMessage": "Username already in use"}


    # If the code has made it to this point, then the password is valid and the username is not already being used
    
    # Create the account structure and add it to the database
	account = { "UUID": 	highestUUID + 1,
		"username": 		inputUsername,
		"hashed_password": 	hashPassword(inputPassword),
		"display_name":		inputDisplayName,
		"profileImage":		inputImageURL,
		"config":			json.load(open(constants.FILE_PATH + "data/default_config.json")),
		"savegames":		[]}

	# Save data
	accountsDB = open(constants.FILE_PATH + "data/accounts.json", 'r+') 
	accountsDBJson = json.load(accountsDB)
	accountsDBJson.append(account)
	accountsDB.seek(0)
	json.dump(accountsDBJson, accountsDB, indent=4)
	accountsDB.close()
	# Return pass message
	return {"returnType": 1,
			"returnMessage": "Successfully saved",
			"account_details": account}
