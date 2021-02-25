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
        # utilizing python's int range (this will be used as the second hashing method)
        return (int(pair[0]) * int(pair[1])) % 50993

    # first pass will take the original data in the form of a list, it will count all singletons and hash all pairs (keeping the count of the buckets)
    def firstPassPCY(self, originalData: list, chunkSize: int):
        countSingletons = dict()
        hashedPairs = dict()
        # to avoid out of index errors
        if(chunkSize > len(originalData)):
            chunkSize = len(originalData)

        # select a basket
        for i in range(chunkSize):
            for j in range(0, len(originalData[i])):
                # add basket to hashtable ()
                if originalData[i][j] not in countSingletons:
                    countSingletons[originalData[i][j]] = 1
                else:
                    countSingletons[originalData[i][j]] += 1
                # hash pair of items and add their count to the bit vector
                for k in range(j+1, len(originalData[i])):
                    tupl = originalData[i][j], originalData[i][k]
                    hashNum = PCY.hashPair(tupl)

                    if hashNum not in hashedPairs:
                        hashedPairs[hashNum] = 1
                    else:
                        hashedPairs[hashNum] += 1

        # will return count of singletons, and the hashed pairs
        return countSingletons, hashedPairs

    def firstPassMultiHash(self, originalData: list, chunkSize: int):
        countSingletons = dict()
        hashedPairsOne = dict()
        hashedPairsTwo = dict()
        # to avoid out of index errors
        if(chunkSize > len(originalData)):
            chunkSize = len(originalData)

        # select a basket
        for i in range(chunkSize):
            for j in range(0, len(originalData[i])):
                # add basket to hashtable ()
                if originalData[i][j] not in countSingletons:
                    countSingletons[originalData[i][j]] = 1
                else:
                    countSingletons[originalData[i][j]] += 1
                # hash pair of items and add their count to the bit vector
                for k in range(j+1, len(originalData[i])):
                    tupl = originalData[i][j], originalData[i][k]
                    hashOne = PCY.hashPair(tupl)
                    hashTwo = PCY.hashPair(tupl, 2)

                    if hashOne not in hashedPairsOne:
                        hashedPairsOne[hashOne] = 1
                    else:
                        hashedPairsOne[hashOne] += 1

                    if hashTwo not in hashedPairsTwo:
                        hashedPairsTwo[hashTwo] = 1
                    else:
                        hashedPairsTwo[hashTwo] += 1

        # will return count of singletons, and the hashed pairs for first hash function and second hash function
        return countSingletons, hashedPairsOne, hashedPairsTwo

    # will take hashedPairs and set their index in the bitvector to 1 if they are equal to or exceed the support threshold.
    def createBitVector(self, hashedPairs: dict, chunkSize: int, support: int) -> BitVector:
        # max size for bitvector so we can hash any potential combination
        bitVector = BitVector(size=50993)
        for bucket in hashedPairs:  # length of hashCount
            if(hashedPairs[bucket] >= support):
                bitVector[bucket] = 1

        return bitVector

    # takes bitvector (check if pair hash to 1), take countSingleton and check if both items are frequent
    def countHashedPairs(self, bitvector, countSingletons: dict, originalData: list, chunkSize: int, support: int) -> dict:
        # to avoid out of index errors
        if(chunkSize > len(originalData)):
            chunkSize = len(originalData)

        countPairs = dict()
        for i in range(chunkSize):
            for j in range(len(originalData[i])):
                for k in range(j+1, len(originalData[i])):
                    # select two items
                    firstItem, secondItem = int(
                        originalData[i][j]), int(originalData[i][k])
                    tupl = firstItem, secondItem
                    # hash both items
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

    # we need to take count of singletons, previous bitvector (to check if pair hash to a value of 1) and the original file to go through all valid pairs.
    # then we return the second bitvector which will be used in the third pass
    # this will be the second pass
    def multiStageSecondHash(self, bitvectorOne, countSingletons: dict, originalData: list, chunkSize: int, support: int):
        secondHashedPairs = dict()
        if(chunkSize > len(originalData)):
            chunkSize = len(originalData)

        for i in range(chunkSize):
            for j in range(len(originalData[i])):
                for k in range(j+1, len(originalData[i])):
                    # select two items
                    firstItem, secondItem = int(
                        originalData[i][j]), int(originalData[i][k])
                    tupl = firstItem, secondItem
                    # hash both items
                    hashresult = PCY.hashPair(tupl)
                    # if bitvectorOne is 1 (bucket is frequent)
                    if bitvectorOne[hashresult]:
                        # if both singletons are frequent
                        if countSingletons[str(firstItem)] >= support and countSingletons[str(secondItem)] >= support:
                            # will use second hash function
                            secondHashRes = PCY.hashPair(tupl, 2)
                            #print(f"{tupl} will be hashed with a result of {secondHashRes}")
                            if secondHashRes not in secondHashedPairs:
                                secondHashedPairs[secondHashRes] = 1

                            else:
                                secondHashedPairs[secondHashRes] += 1
        return secondHashedPairs

    def multiStageThirdpass(self, bitvectorOne, bitvectorTwo, countSingletons, originalData, chunkSize, support):
        # to avoid out of index errors
        if(chunkSize > len(originalData)):
            chunkSize = len(originalData)

        countPairs = dict()
        for i in range(chunkSize):
            for j in range(len(originalData[i])):
                for k in range(j+1, len(originalData[i])):
                    # select two items
                    firstItem, secondItem = int(
                        originalData[i][j]), int(originalData[i][k])
                    tupl = firstItem, secondItem
                    # hash both items
                    hashresultOne = PCY.hashPair(tupl)
                    hashresultTwo = PCY.hashPair(tupl, 2)

                    # if bitvector is 1 (bucket is frequent for first hash table)
                    if bitvectorOne[hashresultOne]:
                        # if both singletons are frequent
                        if countSingletons[str(firstItem)] >= support and countSingletons[str(secondItem)] >= support:
                            # if bitvector is 1 (bucket is frequent for second hash table)
                            if bitvectorTwo[hashresultTwo]:
                                # if pair not in dictionary add them
                                if tupl not in countPairs:
                                    countPairs[tupl] = 1

                                else:
                                    countPairs[tupl] += 1
        return countPairs

    def runPCY(self, chnkSize: int, supp: int):
        start = time.perf_counter()
        # open file and create a list for each line
        fp = "retail.txt"
        basketsContainer = aPriori.parseFile(0, fp)
        ##################################### PASS 1 #####################################
        countSingletons, hashCount = PCY.firstPassPCY(
            0, basketsContainer, chnkSize)

        bitVector = PCY.createBitVector(0, hashCount, chnkSize, supp)
        del hashCount

        ##################################### PASS 2 #####################################
        pairCount = PCY.countHashedPairs(
            0, bitVector, countSingletons, basketsContainer, chnkSize, supp)
        del basketsContainer, bitVector, countSingletons

        freqPairs = aPriori.findFrequentPairs(0, pairCount, supp)
        del pairCount

        end = time.perf_counter()
        print(f"PCY finished at {(end - start) * 1000:0.3f} ms")

    def runMultiStage(self, chnkSize: int, supp: int):
        start = time.perf_counter()
        # open file and create a list for each line
        fp = "retail.txt"
        originalData = aPriori.parseFile(0, fp)
        ##################################### PASS 1 #####################################
        countSingletons, hashedPairOne = PCY.firstPassPCY(
            0, originalData, chnkSize)

        bitVectorOne = PCY.createBitVector(0, hashedPairOne, chnkSize, supp)
        del hashedPairOne

        ##################################### PASS 2 #####################################
        hashedPairTwo = PCY.multiStageSecondHash(
            0, bitVectorOne, countSingletons, originalData, chnkSize, supp)

        bitVectorTwo = PCY.createBitVector(0, hashedPairTwo, chnkSize, supp)
        del hashedPairTwo

        ##################################### PASS 3 #####################################
        pairCount = PCY.multiStageThirdpass(
            0, bitVectorOne, bitVectorTwo, countSingletons, originalData, chnkSize, supp)
        del originalData, bitVectorOne, bitVectorTwo, countSingletons

        freqPairs = aPriori.findFrequentPairs(0, pairCount, supp)
        del pairCount

        end = time.perf_counter()
        print(f"Multistage finished at {(end - start) * 1000:0.3f} ms")

    def runMultiHash(self, chnkSize: int, supp: int):
        start = time.perf_counter()
        # open file and create a list for each line
        fp = "retail.txt"
        originalData = aPriori.parseFile(0, fp)
        ##################################### PASS 1 #####################################
        countSingletons, hashedPairOne, hashedPairTwo = PCY.firstPassMultiHash(
            0, originalData, chnkSize)

        bitVectorOne = PCY.createBitVector(0, hashedPairOne, chnkSize, supp)
        del hashedPairOne

        bitVectorTwo = PCY.createBitVector(0, hashedPairTwo, chnkSize, supp)
        del hashedPairTwo

        ##################################### PASS 2 #####################################
        # same process as the third pass for multistage
        pairCount = PCY.multiStageThirdpass(
            0, bitVectorOne, bitVectorTwo, countSingletons, originalData, chnkSize, supp)
        del originalData, bitVectorOne, bitVectorTwo, countSingletons

        freqPairs = aPriori.findFrequentPairs(0, pairCount, supp)
        del pairCount

        end = time.perf_counter()
        print(f"Multistage finished at {(end - start) * 1000:0.3f} ms")

    def runAtPercent(self, dataSetPercent: int, supportPercent: int, algorithm: str):
        dataSetPercent = math.floor(88163 * (dataSetPercent/100))
        supportPercent = math.floor(dataSetPercent * (supportPercent / 100))
        if algorithm is "PCY":
            PCY.runPCY(0, dataSetPercent, supportPercent)
        elif algorithm is "Multistage":
            PCY.runMultiStage(0, dataSetPercent, supportPercent)
        elif algorithm is "Multihash":
            PCY.runMultiHash(0, dataSetPercent, supportPercent)
        else:
            print("Please enter: 'PCY', 'Multistage', or 'Multihash' for algorithm")
        print(f"dataset size {dataSetPercent} support is {supportPercent}")


if __name__ is "__main__":
    algorithm = "Multihash"
    PCY.runAtPercent(0, 1, 10, algorithm)
    # print(freqPairs)
    # print(len(countSingletons))
