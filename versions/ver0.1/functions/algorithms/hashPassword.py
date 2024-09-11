


def hashPassword(password):
    # Put the first and last two letters in the middle of the password
    # AppleSeed337 -> AppleSAp37eed337
    password = password[:len(password)//2] + password[:2] + password[-2:] + password[len(password)//2:]

    # Put the product of all the numbers in the password at the start of it
    # AppleSeed337 -> 63AppleSeed337
    passwordCharacters = list(password)
    product = 1
    for character in passwordCharacters:
        if character.isdigit():	
            product *= int(character)
    password = str(product) + password

    # Reduce the ascii value of each of the characters by 10
    # AppleSeed337 -> 7ffb[I[[Z))-
    passwordCharacters = list(password)
    passwordCharacters = [chr(ord(character) - 10) for character in passwordCharacters]
    password = "".join(passwordCharacters)

    # Add a salt of "Xj8/" to the end of the password
    # AppleSeed337 -> AppleSeed337Xj8/
    password += "Xj8/"

    # Move the last letter to the front of the password for the the ascii 
    # total of the password number divided and rounded by 100 of turns
    # AppleSeed337 -> pleSeed337Ap
    asciiTotal = sum([ord(character) for character in password])
    for i in range(asciiTotal // 100):
        password = password[len(password)-1] + password[:-1]

    # Alternate the first and last letters of the password, moving inwards 
    # (if there are an odd number of letters, add a P to the end to make it even)
    # AppleSeed337 - > A7p3p3ldeeSe
    if len(password) % 2 != 0:
        password = password + "P"	
        tempPassword = ""
        for i in range(len(password)//2):
            tempPassword += password[i] + password[-i]

    # Overall, the password is very scrambled:
    # AppleSeed337 -> AppleSAp37eed337 -> 1323AppleSAp37eed337 -> ')()7ffb[I7f)-[[Z))- 
    # -> ')()7ffb[I7f)-[[Z))-Xj8/ -> ')()7ffb[I7f)-[[Z))-Xj8/ -> [I7f)-[[Z))-Xj8/')()7ffb 
    # -> [bIf7ff7))-([)['Z/)8)j-X
    
    return password


