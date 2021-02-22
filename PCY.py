import math
import time
# USES PYTHON3.7 PLEASE RUN THE SCRIPT USING python3.7 command (with numpy and bitvector installed)
from BitVector import BitVector
# the following is the link to the library https://engineering.purdue.edu/kak/dist/BitVector-3.4.9.html
# parsing file is the same action so we will import the implemntation in Apriori.py
from APriori import aPriori


class PCY:
    @staticmethod
    def hashPair(pair: tuple, num=1) -> int:
        if num == 1:
            # using a large prime number
            return (int(pair[0]) + int(pair[1])) % 50021
        return (pair[0] + pair[1]) % 50993  # utilizing python's int range

    def firstPass(self, originalData: list, chunkSize: int):
        basketsTable = dict()
        hashCount = dict()
        # to avoid out of index errors
        if(chunkSize > len(originalData)):
            chunkSize = len(originalData)

        # select a basket
        for i in range(chunkSize):
            for basket in range(0, len(originalData[i])):
                # add basket to hashtable ()
                if basket not in basketsTable:
                    basketsTable[basket] = 1
                else:
                    basketsTable[basket] += 1
                # hash pair of items and add their count to the bit vector
                for j in range(0, len(originalData[basket])):
                    for k in range(j+1, len(originalData[basket])):
                        tupl = originalData[basket][j], originalData[basket][k]
                        hashNum = PCY.hashPair(tupl)
                        if hashNum not in hashCount:
                            hashCount[hashNum] = 1
                        else:
                            hashCount[hashNum] += 1

        return basketsTable, hashCount

    def createBitVector(self, hashCount: dict, chunkSize: int, support: int) -> BitVector:
        # bitvector's size is 10% of chunksize
        bitVectorSize = math.floor(chunkSize/10)
        bitVector = BitVector(size=bitVectorSize)
        for i in range(50021):  # length of hashCount
            # if it's frequent
            if i in hashCount:
                if(hashCount[i] >= support):
                    bitVector[i] = 1
            else:
                pass

        return bitVector

    def countAllPairs(self, potentialPairs: list, originalData: list) -> dict:
        countAllPairs = {}
        for pair in potentialPairs:
            print(f"counting all occurances of pair {pair}...")
            for basket in originalData:
                # if both pair items are in the basket
                if pair[0] in basket and pair[1] in basket:
                    # if pair not in dictionary, add them
                    if pair not in countAllPairs:
                        countAllPairs[pair] = 1
                    # pair already in hash table/dictionary
                    else:
                        # increment count of pair
                        countAllPairs[pair] += 1
                # if pair aren't in basket
                else:
                    pass

        return countAllPairs


    # create bitvector
    # pass 1 you count freq of singletons AND you use the hash function on EVERY pair and map the count to the bitvector
    # pass 2 you check if pair i,j (if i is freq, if j is freq) AND if i,j hashes to a frequent bitvector
if __name__ is "__main__":
    # open file and create a list for each line
    # initialize bitvector with values of 0 and size 10
    bitVector = BitVector(size=10)
    print(bitVector)
    fp = "retail.txt"
    basketsContainer = aPriori.parseFile(0, fp)

    countSingletons, countHash = PCY.firstPass(0, basketsContainer, 10000)
    bv = PCY.createBitVector(0, countHash, 10000, 100)
    print(bv)
    #dct = aPriori.countSingletons(0, basketsContainer, 1000000)

    #freqSingletons = aPriori.findFrequentSingletons(0, dct, 880)
    # print(freqSingletons)
