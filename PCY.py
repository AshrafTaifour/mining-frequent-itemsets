
import time
# USES PYTHON3.7 PLEASE RUN THE SCRIPT USING python3.7 command (with numpy and bitvector installed)
from BitVector import BitVector
# the following is the link to the library https://engineering.purdue.edu/kak/dist/BitVector-3.4.9.html
# parsing file is the same action so we will import the implemntation in Apriori.py
from APriori import aPriori

# initialize bitvector with values of 0 and size 10
bv = BitVector(size=10)
print(bv)

bv[5] = 1
print(bv)

basketsContainer = aPriori.parseFile(0, "retail.txt")
print(basketsContainer)
# create bitvector

# pass 1 you count freq of singletons AND you use the hash function on EVERY pair and map the count to the bitvector
# pass 2 you check if pair i,j (if i is freq, if j is freq) AND if i,j hashes to a frequent bitvector
