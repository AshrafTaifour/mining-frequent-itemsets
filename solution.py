
filepath = "retail.txt"
basketsContainer = []
basketsTable = {}
with open(filepath, "r") as fp:
    line = fp.readline()
    while line:
        line = line.strip('\n')
        basketsContainer.append(line)
        line = fp.readline()



print(basketsContainer)
print(len(basketsContainer))
