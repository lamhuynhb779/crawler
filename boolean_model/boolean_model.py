import os
import glob
import re

path = "docs/"
os.chdir(path)

def writeToFile(file_name, data):
	txt = open(file_name, 'a')
	txt.truncate()
	txt.write(data)
	txt.close()

def replaceSymbol(currentList):
	replacedList = []; l = ['.', ',', ';', ':', '?', '(', ')', '!']
	for i in currentList:
		for j in l:
			if i.find(j)>=0:
				i = i.replace(j,"")
		replacedList.append(i)
	return replacedList

def toLowercase(currentList):
	return [element.lower() for element in currentList]

def indexing(terms, docIds):
    numCurrentDoc = 1
    for i in range(0, len(terms)):
        if terms[i]==" ":
            numCurrentDoc += 1
        else:
            docIds.append(numCurrentDoc)
    return terms, docIds

def removeValue(theList, val):
   return [value for value in theList if value != val]

def sortAlphaBeta(listTerm, listDocID):
    l = len(listTerm)
    for i in range(0, l):
        for j in range(i+1, l):
            if listTerm[i] > listTerm[j]:
                listTerm[i], listTerm[j] = listTerm[j], listTerm[i]
                listDocID[i], listDocID[j] = listDocID[j], listDocID[i]
    return listTerm, listDocID

def mappingEachTermWithDocIDs(uniqueTerms, allTerms, allDocIDs):
    mappingTermWithDocIDs = []
    for term in uniqueTerms:
        start = allTerms.index(term)
        # Nếu count > 1 nghĩa là có hơn 1 từ giống nhau trong terms
        # Thì count + start - 1 > start
        # Ngược lại, Nếu chỉ có duy nhất 1 từ
        # Thì count + start - 1 = start
        end = allTerms.count(term) + start - 1

        if end == start:
            end = start + 1

        # Lưu lại vị trí của doc tương ứng với từng từ trong setTerms
        # Ví dụ term = is
        # terms     = ['a', 'a', 'animal', 'animal', 'cat', 'chicken', 'dog', 'eat', 'faithful', 'i', 'is', 'is', 'love', 'to', 'very', 'weird']
        # setTerms  = ['a', 'eat', 'love', 'cat', 'dog', 'animal', 'faithful', 'to', 'is', 'i', 'very', 'weird', 'chicken']
        # -> listDoc[8] = [10, 11] tưng ứng với setTerms[8]
        listDoc = []
        for i in range(start, end):
            listDoc.append(allDocIDs[i])
            listDoc = list(set(listDoc))

        mappingTermWithDocIDs.append(listDoc)
    return mappingTermWithDocIDs

def getAllWords():
    terms               = []
    docIds              = []
    setTerms            = []
    term_docFreq_list   = []
    splitDoc = " "

    # Read folder
    files       = glob.glob("*.txt") # ['doc2.txt', 'doc3.txt', 'doc1.txt']
    numDoc      = 0
    nameDocs    = []
    for file in files:
        fileStream = open(file) # <_io.TextIOWrapper name='doc2.txt' mode='r' encoding='UTF-8'>
        nameDocs.append(fileStream.name)

        # Pre-process content
        content = fileStream.read().encode('ascii', 'ignore').decode('utf-8')
        content = content.replace('.', '-').replace('"', '-').replace('!', '-')

        # Split each word by ' ' or '-' or '  '
        contentToArray = re.split(' |-|  ', content)
        terms.extend(contentToArray)

        # Use the " " element to split between documents
        terms.extend(splitDoc)
        
        # close stream
        fileStream.close()

    # term is ['Cat', 'is', 'a', 'weird', 'animal', ' ', 'I', 'love', 'to', 'eat', 'chicken', ' ', 'Dog', 'is', 'a', 'very', 'faithful', 'animal', ' ']
    # Pre-process content
    terms = replaceSymbol(terms)
    terms = toLowercase(terms)

    # Đánh chỉ mục cho từng term
    terms, docIds = indexing(terms, docIds)
    # Result:
    # ['cat', 'is', 'a', 'weird', 'animal', ' ', 'i', 'love', 'to', 'eat', 'chicken', ' ', 'dog', 'is', 'a', 'very', 'faithful', 'animal', ' ']
    # [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3]

    # Remove the " " element to split between documents in terms
    terms = removeValue(terms, splitDoc)

    # Sort terms by alpha beta
    terms, docIds = sortAlphaBeta(terms, docIds)

    # Get unique terms
    setTerms = list(set(terms))

    mappingTermWithDocIDs = mappingEachTermWithDocIDs(setTerms, terms, docIds)

    return setTerms, mappingTermWithDocIDs

# Test

setterms, mappingTermWithDocIDs = getAllWords()

words = '\n'.join(setterms)

writeToFile("dictionary.txt", words)
