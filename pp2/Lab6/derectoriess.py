import os

def listOfAllFiles():
    path = r"C:\Users\user\Desktop\Lab6"
    print("All folders in this path:")
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            print(i)
    print("\nAll files in this path:")
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)):
            print(i)
    print("\nAll files and folders:")
    for i in os.listdir(path):
        print(i)
listOfAllFiles()

def testForExistenceReadabilityWritabilityExecutability():
    path = "lab6"
    if os.access(path, os.F_OK):
        print("Your file exists!!!!")
    else:
        print("Your file does not exist :(")
    if os.access(path, os.R_OK):
        print("I can read your file :D")
    else:
        print("I can not read your file :(")
    if os.access(path, os.W_OK):
        print("I can write something in your file! That is good :D")
    else:
        print("I can not write anything in your file :(")
    if os.access(path, os.X_OK):
        print("I can execute your file, oh yeah :D")
    else:
        print("I can not execute your file, sad :(")

def findingFilenameAndDirectory():
    path = "lab6/builtin.py"
    if os.access(path, os.F_OK):
        print("Your path exists :D, trying to find the directory and filename")
        x = os.path.split(path)
        print("The directory of the file:", x[0])
        print("The name of file:", x[1])
    else:
        print("Your path does not exist")

def countingLines():
    path = "lab6/text.txt"
    with open(path, "r") as f:
        count = sum(1 for line in f if line.strip())
    print("The amount of lines in this file is:", count)

def listToFile():
    path = "lab6/text.txt"
    my_list = [1, "Askar", "Lenovo laptops are the best!", 4, "I hate stairs"]
    with open(path, "w") as f:
        print("Let me write this list to your file:\n")
        print(my_list)
        f.write(" ".join(map(str, my_list)))
    with open(path, "r") as f:
        print(f.read())

def AtxtToZtxt():
    path = "lab6"
    for i in range(65, 90):
        name = os.path.join(path, chr(i) + ".txt")
        with open(name, "a"):
            pass
    for i in os.listdir(path):
        print(i)

def copyPaste():
    path = "lab6/text.txt"
    pathOfSecondfile = "lab6/text1.txt"
    with open(path, "r") as f, open(pathOfSecondfile, "w") as f1:
        f1.write(f.read())
    with open(pathOfSecondfile, "r") as f1:
        for line in f1:
            print(line, end='')

def deletingFileInSpecificPath():
    path = "lab6/text2.txt"
    if os.access(path, os.F_OK):
        print("Your path exists!\nOkay...let me delete your file")
        os.remove(path)
        print("Deleting is successful! :D")
    else:
        print("Your path does not exist :(")