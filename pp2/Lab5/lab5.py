import re
with open("row.txt", "r", encoding="utf-8") as file:
    txt = file.read()
    txt1= "ajbjb jjdfndjfn njnfjdsn JBIJBNKFmn ab ab AkdjnfkdfjfjB ahfbdhfb"
def findab():
    x = re.findall("ab", txt)
    print (x)
#findab()
def findabb():
    x = re.findall("ab{2,3}", txt)
    print(x)
#findabb()
def findlowercase():  
    x= re.findall("[a-z]", txt)
    print(x)
#findlowercase()
def findAa():
    x = re.findall("[A-Z][a-z]", txt)
    print(x)
#findAa()
def startaendb():
    x = re.findall("^a.*b$", txt1)
    print(x)
#startaendb()
def replacespace():
    x = re.sub("\s", ":", txt)
    x = re.sub("[.]", ":", x)
    x = re.sub(",", ":", x)
    print(x)
#replacespace()
def snaketocamel():
    x = txt.split("_")
    for i in range(1, len(x)):
        x[i] = x[i].capitalize()
    for x in x:
        print(x, end='')
#snaketocamel()
def camelToSnake():
    x = re.sub(r"([A-Z][a-z]+)", r" \1", txt).strip()
    print(x)
#camelToSnake()
def splitUpper():
    x = txt
    for i in range(0, len(x)):
        if x[i].isupper():
            x1 = x[:i]
            x2 = x[i + 1:]
            x = x1 + ' ' + x2
    l = re.split("\s", x)
    l2 = []
    for i in l:
        if len(i) != 0:
            l2.append(i)
    print(l2)
#splitUpper()
def splitUpper2():
    x = re.sub(r"([A-Z][a-z]+)", r" \1", txt).strip()
    print(x)
#splitUpper2()