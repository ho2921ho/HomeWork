
# 과제1
def range2(*arg):
    mylist = []
    if len(arg) == 3:
        start = arg[0]
        stop = arg[1]
        step = arg[2]
        while start < stop:
            mylist.append(start)
            start +=step
    elif len(arg) == 2:
        start = arg[0]
        stop = arg[1]
        while start < stop:
            mylist.append(start)
            start += 1
    elif len(arg) == 1:
        start = 0
        stop = arg[0]
        while start < stop:
            mylist.append(start)
            start += 1
    else:
        raise TypeError()
        
    return mylist
    

# 과제2
    
f = open(r'C:\Users\dongkeon\Desktop\abc.txt')
fileLines = f.readlines()

for line in fileLines:
    if int(line.split(':')[1]) > 80:
        print(line)
        
f.close()
