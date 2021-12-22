print("Welcome to Encrypted Database Tool! Type help for getting the instructions about the commands!")
while 1:
    print("----------")
    command = input('Enter a command: ')
    if command.lower() == "exit":
        break
    if command.lower() == "help":
        f = open("instructions.txt")
        print("----------")
        print(f.read())
    else:
        command = command.split(" ")
        if command[0] != "add" and command[0] != "show" and command[0] != "remove":
            print("Wrong command! Type help to see the commands!")
        if command[0] == "show" and len(command) != 4:
            print("Wrong syntax of show command! Type help to see the commands!")
        if (command[0] == "add" or command[0] == "remove") and len(command) != 2:
            if command[0] == "add":
                print("Wrong syntax of add command! Type help to see the commands!")
            if command[0] == "remove":
                print("Wrong syntax of remove command! Type help to see the commands!")
