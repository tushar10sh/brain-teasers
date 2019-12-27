import sys
from copy import deepcopy

DEBUG_MODE = True

def createBranch(combinationlist, inputlist):
	numBranches = 0
	for i in range(len(inputlist)):
		if inputlist[i][0] == inputlist[0][0]:
			numBranches += 1
		else:
			break
	initialLength = len(combinationlist)
	combinationlistbackup = deepcopy(combinationlist)
	if DEBUG_MODE:
		print("NumBranches: ", numBranches)
		print("combinationlist: ", combinationlist)
	for i in range(numBranches-1):
		temp = deepcopy(combinationlistbackup)
		combinationlist.extend(temp)
	for i in range(numBranches):
		for j in range(initialLength):
			combinationlist[j + i*(initialLength)].append(deepcopy(inputlist[0]))
		inputlist.remove(inputlist[0])
	if DEBUG_MODE:
		print("combinationlist: ", combinationlist)
	return (combinationlist, inputlist)

def createCombinationList(combinationlist, inputlist, rem):
	if DEBUG_MODE:
		print ("rem : {} , inputlist : {}".format(rem, inputlist))

	if rem > 0 and len(inputlist) == 0:
		return False
	maxoflist = inputlist[0]

	if maxoflist[0] < rem:
		rem = rem - maxoflist[0]
		(tempcombinationlist, reducedInputlist) = createBranch( deepcopy(combinationlist), deepcopy(inputlist))
		if rem > 0 and len(reducedInputlist) == 0:
			print("Undoing branching")
			for i in range(len(combinationlist)):
				combinationlist[i].append(deepcopy(inputlist[0]))
			print("combinationlist: ", combinationlist)
			inputlist.remove(inputlist[0])
		else:
			combinationlist = deepcopy(tempcombinationlist)
			inputlist = reducedInputlist
		return createCombinationList(combinationlist, inputlist, rem)
	elif maxoflist[0] == rem:
		(combinationlist, inputlist) = createBranch( deepcopy(combinationlist), inputlist)
		return combinationlist
	else:
		inputlist.remove(maxoflist)
		return createCombinationList(combinationlist, inputlist, rem)

def generateResultList( combinationlist, inputlist, truncatedPi):
	piList = []
	spacesToInsert = len(combinationlist)-1
	restrictedInputList = [ inputlist[combinationlist[i][1]] for i in range(len(combinationlist)) ]
	start = 0
	end   = 1
	if DEBUG_MODE:
		print("Spaces to insert: ", spacesToInsert)
	while spacesToInsert>=0 and end <= len(truncatedPi):
		if DEBUG_MODE:
			print("piList: ", piList)
		if truncatedPi[start:end] in restrictedInputList:
			piList.append( truncatedPi[start:end] )
			spacesToInsert -= 1
			start = end
		end += 1

	if end != len(truncatedPi):
		if truncatedPi[start:] in restrictedInputList:
			piList.append(truncatedPi[start:])

	if len(piList) == ( len(restrictedInputList) -1) and restrictedInputList[-1] not in piList:
		piList.append(restrictedInputList[-1])

	if ''.join(piList) == truncatedPi:
		return ' '.join(piList)
	else:
		return False

def generateSubLists(inputList, truncatedPi):
	lengthOfPI = len(truncatedPi)
	lengthIndexList = [ (len(num), idx) for idx, num in enumerate(inputList) ]
	lengthIndexList = sorted(lengthIndexList, reverse=True)
	if DEBUG_MODE:
		print("lengthIndexList : ", lengthIndexList)	
	probableCombinationList = createCombinationList([[]], deepcopy(lengthIndexList), lengthOfPI)
	if DEBUG_MODE:
		print("probableCombinationList: ", probableCombinationList)
	results = []
	for i in range(len(probableCombinationList)):
			match = True
			for j in range(len(probableCombinationList[i])):
				if inputList[probableCombinationList[i][j][1]] not in truncatedPi:
					match = False
					break
			if match:
				if DEBUG_MODE:
					print("matched probable combination: ", probableCombinationList[i])
				resultList = generateResultList(deepcopy(probableCombinationList[i]), inputList, truncatedPi)
				if resultList:
					results.append( (len(probableCombinationList[i])-1, resultList))
	return results

def main(truncatedPi, listofFavNums):
	listOfValidNums = []
	for i in range(len(listofFavNums)):
		if listofFavNums[i] in truncatedPi:
			listOfValidNums.append(listofFavNums[i])
	results = generateSubLists(listOfValidNums, truncatedPi)
	print(results)

if __name__ == '__main__':
	# truncatedPi = sys.argv[1]
	# listOfFavNums = sys.argv[2:]
	# truncatedPi = '3141592653589793238462643383279'
	truncatedPi = '31415926'
	listOfFavNums = ['3', '1', '4', '1', '5', '9', '2', '6', '8']
	# listOfFavNums = ['31', '4', '1', '592']
	# listOfFavNums = ['314', '49', '9901', '15926535897', '14', '9323', '8462643383279', '4', '793']
	#listOfFavNums = ['314159265358','9901', '15926535897', '14', '9323', '9793238462643383279', '314', '49', '4', '793']
	# listOfFavNums = ['314159265358979323846264338327', '9', '141592653589793238462643383279', '3', '14']
	main(truncatedPi, listOfFavNums)
	# print(createCombinationList([[]], [(20,0), (20, 1), (20, 2), (10,1), (5,2), (2,3), (1,4)], 22))


"""
	sample input
	'3141592653589793238462643383279'
	['314', '49', '9901', '15926535897', '14', '9323', '8462643383279', '4', '793']

	sample output
   [(3, '314 15926535897 9323 8462643383279')]	
	
	sample input
	'3141592653589793238462643383279'
	['314159265358','9901', '15926535897', '14', '9323', '9793238462643383279', '314', '49', '4', '793', '8462643383279']

	sample output
	[(1, '314159265358 9793238462643383279')]	
	
	sample input 
	'3141592653589793238462643383279'
	['314159265358979323846264338327', '9', '141592653589793238462643383279', '3']
	
	sample output
"""

"""
def generateResultList_backup( combinationlist, inputlist, truncatedPi):
	print("Input combination list", combinationlist)
	truncatedPiWithSpaces = truncatedPi
	prev_idx = len(truncatedPi)
	for i in range(len(combinationlist)):
		try:
			idx = truncatedPiWithSpaces[:prev_idx+1].index(inputlist[combinationlist[i][1]])
			if idx != 0 and idx < prev_idx:
				truncatedPiWithSpaces = truncatedPiWithSpaces[:idx] + ' ' + truncatedPiWithSpaces[idx:]
				prev_idx = idx
		except:
			return False
	print("local result ", truncatedPiWithSpaces)
	return truncatedPiWithSpaces
"""

