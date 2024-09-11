import json
import shutil

def delete_savegame(account_id, savegame_id):
    from classes.global_data import constants_structure
    constants = constants_structure()
    
    # Load accounts
    with open(constants.FILE_PATH + "data/accounts.json", 'r') as accountsDB:
        accountsDBJson = json.load(accountsDB)
        
    # Remove savegame on account data
    for i, account in enumerate(accountsDBJson):
        if account["UUID"] == account_id:
            for j, savegame in enumerate(account["savegames"]):
                if savegame["display_details"]["id"] == savegame_id:
                    accountsDBJson[i]["savegames"].pop(j)
                    break
    # Save accounts
    with open(constants.FILE_PATH + "data/accounts.json", 'w') as accountsDB:
        json.dump(accountsDBJson, accountsDB, indent=4)
        accountsDB.close()
        
    # Delete savegame files
    shutil.rmtree(constants.FILE_PATH + f"data/account_games/{account_id}_games/{savegame_id}_levels")
