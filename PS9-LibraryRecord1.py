#
#       LIBRARY MEMBER RECORDING PROGRAM
#

from random import randint

# File directories
FN_CREDENTIALS = "members.txt"

# Input / Output separator
SEPARATOR = "--------------------------------"

# Menu options
OPTIONS = [["List members", "Edit members", "Change member\'s details", "Calculate top readers", "Calculate total books read", "Calculate average number of books read", "Leave the program"], ["Add a member", "Delete a member", "Go back"], ["Change name", "Change number of books read", "Go back"]]

# Current stage in menu
stage = 0

# List of members
listOfMembers = []

# List all array options
def listOptions(o):
    print(SEPARATOR)
    for count, option in enumerate(o):
        print(f" {count+1} - {option}")

# Check whether the answer is suitable
def checkAnswer(answer):
    try:
        if int(answer) > 0 and int(answer) <= len(OPTIONS[stage]):
            return True
        else:
            print(f"Error: Wrong syntax. There is no option number \'{answer}\'.")
            return False
    except:
        print("Error: Wrong syntax. A proper answer should consist of just a number.")
        return False

# Generate User ID
def generateID(name, surname):
    result = str(randint(1, 1000))
    for i in range(3-len(result)):
        result = "0" + result
    result += name[0].upper() + surname[0].upper()
    for member in listOfMembers:
        while result in member:
            result = str(randint(0, 1000)) + name[0].upper() + surname[0].upper()
    return result

def validate(question):
    while True:
        result = input(f"Are you sure you want to {question}? (y/n)\n").lower()
        if result == 'y':
            return True
        if result == 'n':
            return False
        else:
            print("Error: Wrong answer. Your answer must be either \'y\' or \'n\'")

# Save members to the file
def loadMembers():
    with open(FN_CREDENTIALS, "r") as file:
        for line in file.readlines():
            newMember = (line.replace("\n", "").split('|')[0], line.replace("\n", "").split('|')[1], line.replace("\n", "").split('|')[2], int(line.replace("\n", "").split('|')[3]))
            listOfMembers.append(newMember)
        file.close()

def saveMembers():
    with open(FN_CREDENTIALS, "w") as file:
        for member in listOfMembers:
            file.write(f"{member[0].strip()} | {member[1].strip()} | {member[2].strip()} | {member[3]}\n")
        file.close()

# Check wether the number of books is valid
def checkBooksRead():
    try:
        nRead = int(input("Enter a number of books the member has read: "))
        if nRead >= 0:
            return nRead
        else:
            print("Error. The reader cannot read less than 0 books.")
    except:
        print("Error. The answer must consist of only numbers.")

def getTopThree(array):
    result = [0, 0, 0]

    for i in range(len(array)):
        if array[result[1]][3] <= array[i][3]:
            if array[result[0]][3] <= array[i][3]:
                result[0] = i
            else:
                result[1] = i
        else:
            result[2] = i

    return result



# Main loop
if __name__ == "__main__":
    loadMembers()

    shouldLeave = False
    
    while shouldLeave == False:
        listOptions(OPTIONS[stage])
        print(SEPARATOR)
        answer = input()
        print(SEPARATOR)

        if checkAnswer(answer):

            # Leave the program or go back to initial stage
            if int(answer) == len(OPTIONS[stage]):
                if stage == 0:
                    saveMembers()
                    print("Leaving the program...")
                    shouldLeave = True
                else:
                    stage = 0

            elif stage == 0:

                # List members
                if int(answer) == 1:
                    print("User ID | First name | Surname | Number of books read")
                    for member in listOfMembers:
                        print(f"{member[0]} | {member[1]} | {member[2]} | {member[3]}")
                
                # Calculate top readers
                elif int(answer) == 4:

                    # Create an array of top readers
                    topReaders = []

                    if len(listOfMembers) == 0:
                        print("Error: List of library members is empty")
                        continue

                    topReaders = getTopThree(listOfMembers)

                    for i in range(len(topReaders)):
                        print(f"The top {i+1} reader is: {listOfMembers[topReaders[i]][1].strip()} {listOfMembers[topReaders[i]][2].strip()}")
                        print(f"- They have read {listOfMembers[topReaders[i]][3]} books. Their User ID is: {listOfMembers[topReaders[i]][0]}")

                # Calculate total books read
                elif int(answer) == 5:
                    total = 0
                    for member in listOfMembers:
                        total += member[3]

                    print("The total number of books read is: ", total)
                
                # Calculate average number of books read
                elif int(answer) == 6:

                    # Get a total number
                    total = 0
                    for member in listOfMembers:
                        total += member[3]

                    print("The average number of books read is: ", str(total/(len(listOfMembers))))


                else:
                    stage = int(answer) - 1

            elif stage == 1:

                # Add a member
                if int(answer) == 1:
                    name = input("Enter a new library member\'s name: ")
                    surname = input("Enter their surname: ")

                    usrId = generateID(name, surname)
                    print("The ID of the user is: " + usrId)

                    nRead = checkBooksRead()

                    if nRead != None and validate(f"add the following data to the member list:\n{usrId} | {name} {surname} | {nRead} "):
                        newMember = (usrId, name, surname, nRead)
                        listOfMembers.append(newMember)

                # Delete member
                elif int(answer) == 2:
                    usrId = input("Enter the user ID assigned to the member you want to delete: ").upper()

                    userFound = False

                    # Search for the member
                    for count, member in enumerate(listOfMembers):
                        if usrId in member[0]:
                            if validate(f"delete {listOfMembers[count][1]} {listOfMembers[count][2]}"):
                                del listOfMembers[count]

                                userFound = True
                            else:
                                userFound = True
                                break
                    if userFound == False:
                        print("Error: Wrong user ID")
                        
            elif stage == 2:

                # Change name
                if int(answer) == 1:
                    usrId = input("Enter the user ID assigned to the member whom you want to rename: ").upper()

                    userFound = False

                    # Search for the member
                    for count, member in enumerate(listOfMembers):
                        if usrId in member[0]:

                            name = input("Enter a new name for the member: ")
                            surname = input("Enter their new surname: ")

                            if validate(f"rename {listOfMembers[count][1]} {listOfMembers[count][2]}"):

                                listOfMembers.append((listOfMembers[count][0], name, surname, listOfMembers[count][3]))

                                del listOfMembers[count]

                                userFound = True
                                break
                            else:
                                userFound = True
                                break
                    if userFound == False:
                        print("Error: Wrong user ID")
                    
                # Change number of books read
                elif int(answer) == 2:
                    usrId = input("Enter the user ID assigned to the member whose number of books you want to change: ").upper()

                    userFound = False

                    # Search for the member
                    for count, member in enumerate(listOfMembers):
                        if usrId in member[0]:

                            nRead = checkBooksRead()

                            if nRead != None and validate(f"change a number of books read by {listOfMembers[count][1]} {listOfMembers[count][2]}"):

                                listOfMembers.append((listOfMembers[count][0], listOfMembers[count][1], listOfMembers[count][2], nRead))

                                del listOfMembers[count]

                                userFound = True
                            else:
                                userFound = True
                                break
                    if userFound == False:
                        print("Error: Wrong user ID")
