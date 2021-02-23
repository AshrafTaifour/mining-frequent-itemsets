import math
import time
from BitVector import BitVector
# USES PYTHON3.7 PLEASE RUN THE SCRIPT USING python3.7 command (with numpy and bitvector installed)
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
            for j in range(0, len(originalData[i])):
                # add basket to hashtable ()
                if originalData[i][j] not in basketsTable:
                    basketsTable[originalData[i][j]] = 1
                else:
                    basketsTable[originalData[i][j]] += 1
                # hash pair of items and add their count to the bit vector
                for k in range(j+1, len(originalData[i])):
                    tupl = originalData[i][j], originalData[i][k]
                    hashNum = PCY.hashPair(tupl)

                    if hashNum not in hashCount:
                        hashCount[hashNum] = 1
                    else:
                        hashCount[hashNum] += 1

        return basketsTable, hashCount

    def createBitVector(self, hashCount: dict, chunkSize: int, support: int) -> BitVector:
        # max size for bitvector so we can hash any potential combination
        bitVector = BitVector(size=50021)
        for bucket in hashCount:  # length of hashCount
            if(hashCount[bucket] >= support):
                bitVector[bucket] = 1

        return bitVector

    def countHashedPairs(self, bitvector: dict, countSingletons: dict, originalData: list, chunkSize: int, support: int) -> dict:
        countPairs = dict()
        for i in range(chunkSize):
            for j in range(len(originalData[i])):
                for k in range(j+1, len(originalData[i])):
                    firstItem, secondItem = int(
                        originalData[i][j]), int(originalData[i][k])
                    tupl = firstItem, secondItem
                    #print(firstItem, secondItem)
                    hashresult = PCY.hashPair(tupl)
                    # if bitvector is 1 (bucket is frequent)
                    if bitvector[hashresult]:
                        # if both singletons are frequent
                        if countSingletons[str(firstItem)] >= support and countSingletons[str(secondItem)] >= support:
                            # if pair not in dictionary add them
                            if tupl not in countPairs:
                                countPairs[tupl] = 1

                            else:
                                countPairs[tupl] += 1
        return countPairs


if __name__ is "__main__":

    # open file and create a list for each line
    fp = "retail.txt"
    basketsContainer = aPriori.parseFile(0, fp)

    countSingletons, hashCount = PCY.firstPass(0, basketsContainer, 10000)

    bitVector = PCY.createBitVector(0, hashCount, 10000, 100)
    print(bitVector)

    pairCount = PCY.countHashedPairs(
        0, bitVector, countSingletons, basketsContainer, 10000, 100)

    print(pairCount)
