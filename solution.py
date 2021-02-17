
filepath = "retail.txt"
basketsContainer = []

with open(filepath, "r") as fp:
    line = fp.readline()
    while line:
        #removes new line at end
        line = line.strip('\n')
        #splits every number in the basket
        line = line.split()
        basketsContainer.append(line)
        line = fp.readline()




#print(basketsContainer)
#print(len(basketsContainer))

def firstPass(lst: list) -> dict:
    basketsTable = {}
    #select a basket
    for i in lst:
        for j in i:
            if j not in basketsTable:
                basketsTable[j] = 1
            else:
                basketsTable[j] += 1
            

    return basketsTable


dct = firstPass(basketsContainer)
print(dct)
