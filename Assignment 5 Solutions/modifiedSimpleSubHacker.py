# Ritvik Khanna (1479093) and Bisan Hasasneh (1505703) CMPUT299 Win2018
# Assignment 5 - Substitution Cipher Hacking
# This uses code from Hacking Secret Ciphers with Python by Al Sweigart
# as well as the checkWord function from lecture slides

import os, re, copy, pprint, simpleSubCipher, makeWordPatterns


if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main() # create the wordPatterns.py file
import wordPatterns



LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

def main():
    # for testing purposes
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    # Determine the possible valid ciphertext translations.
    print('Hacking...')
    decryptedtext = hackSimpleSub(message)
    print()
    print(decryptedtext)

   

def getBlankCipherletterMapping():
    # Returns a dictionary value that is a blank cipherletter mapping.
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}


def addLettersToMapping(letterMapping, cipherword, candidate):
    # The letterMapping parameter is a "cipherletter mapping" dictionary
    # value that the return value of this function starts as a copy of.
    # The cipherword parameter is a string value of the ciphertext word.
    # The candidate parameter is a possible English word that the
    # cipherword could decrypt to.

    # This function adds the letters of the candidate as potential
    # decryption letters for the cipherletters in the cipherletter
    # mapping.

    letterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])
    return letterMapping


def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map, and then add only the
    # potential decryption letters if they exist in BOTH maps.
    intersectedMapping = getBlankCipherletterMapping()
    for letter in LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely.
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersectedMapping[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    # Cipher letters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other
    # letter. (This is why there is a loop that keeps reducing the map.)
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True
    while loopAgain:
        # First assume that we will not loop again:
        loopAgain = False

        # solvedLetters will be a list of uppercase letters that have one
        # and only one possible mapping in letterMapping
        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        # If a letter is solved, than it cannot possibly be a potential
        # decryption letter for a different ciphertext letter, so we
        # should remove it from those other lists.
        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        # A new letter is now solved, so loop again.
                        loopAgain = True
    return letterMapping


def hackSimpleSub(message):
    # returns a string of the decrypted message
    intersectedMap = getBlankCipherletterMapping()
    cipherwordList = nonLettersOrSpacePattern.sub('', message.upper()).split()
    for cipherword in cipherwordList:
        # Get a new cipherletter mapping for each ciphertext word.
        newMap = getBlankCipherletterMapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue # This word was not in our dictionary, so continue.

        # Add the letters of each candidate to the mapping.
        for candidate in wordPatterns.allPatterns[wordPattern]:
            newMap = addLettersToMapping(newMap, cipherword, candidate)

             # Intersect the new mapping with the existing intersected mapping.
        intersectedMap = intersectMappings(intersectedMap, newMap)

    intersectedMap = removeSolvedLettersFromMapping(intersectedMap)

    hackedMessage = decryptWithCipherletterMapping(message, intersectedMap)

    # perform further analysis
    mapping = hacker(hackedMessage,message)
    intersectedMap = intersectMappings(mapping, intersectedMap)
    intersectedMap = removeDuplicate(intersectedMap)
    finalMap = removeSolvedLettersFromMapping(intersectedMap)

    finalHacked = decryptWithCipherletterMapping(message, finalMap)

    return(finalHacked)
    


def decryptWithCipherletterMapping(ciphertext, letterMapping):
    # Return a string of the ciphertext decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with an _ underscore.

    # First create a simple sub key from the letterMapping mapping.
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            # If there's only one letter, add it to the key.
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # With the key we've created, decrypt the ciphertext.
    return simpleSubCipher.decryptMessage(key, ciphertext)


def hacker(Decrypted,ciphertext):
    # Performs further analysis on Decrypted to solve letters that have not yet been solved
    
    # strings that will contains only letters, underscores, and spaces
    decrypted = ''
    encrypted = ''

    # to save ambiguous words, their position in the message, and their corresponding encryption
    wordPosition = []
    _Words = []
    cipherWords =[]
    # to save the positions of the underscores in each ambiguous word
    _Positions = []

    # to save found matches in the dictionary
    newDecrypted = []



    # remove all symbols that are not letters, spaces, or underscores from both the decrypted and encrypted messages
    Decrypted = Decrypted.upper()
    ciphertext = ciphertext.upper()
    for symbol in Decrypted:

        if symbol in LETTERS:

            decrypted += symbol

        elif symbol == ' ':

            decrypted += symbol

        elif symbol == '_':

            decrypted += symbol


    for symbol in ciphertext:

        if symbol in LETTERS:

            encrypted += symbol

        elif symbol == ' ':

            encrypted += symbol

    
        
    # these are lists of the words in each message
    encryptedWords = [word for word in encrypted.split()]
    decryptedWords = [word for word in decrypted.split()]

   
    # to find all words with underscores
    for word in decryptedWords:

        if word.find('_') != -1:
            # underscore found, save the ambiguous word and its position in the message
            _Words.append(word)
            wordPosition.append(decryptedWords.index(word))

    
    # get the encrypted versions of words with underscores
    for counter in wordPosition:

        cipherWords.append(encryptedWords[counter])

    

    for word in _Words:
        # for all words with underscores:
        if word.count('_') == 1:
            # append the underscore position
            _Positions.append(word.find('_'))

        else:
            # multiple underscores, append a list of all underscore positions
            _Positions.append([])
            y = _Positions.index([])
            for i in range(len(word)):

                if word[i] == '_':

                    _Positions[y].append(i)


    # form the regex and search for matches
    for word in _Words:
        word = word.upper()
        regexList = []
        regexList.append('^')

        for symbol in word:

            if symbol in LETTERS:
                regexList.append(symbol)

            elif symbol == '_':
                regexList.append('[A-Z]')

        regexList.append('$')
        regexWord = ''.join(regexList)
        newDecrypted.append(checkWord(regexWord))


    # Map all the possible letters from the found dictionary words
    newMap = getBlankCipherletterMapping()
    n = 0     # n is the index of the ambiguous word we are working on
    while n < len(_Words):
        _pos = _Positions[n]
        if type(_pos) == list:
            # multiple underscores in the word
            for pos in _pos:
                # for each underscore
                symbol = cipherWords[n][pos]
                for word in newDecrypted[n]:
                    # map possible letters
                    possible = word[pos]
                    newMap[symbol].append(possible)

        elif type(_pos) == int:
            # only one underscore in the word
            pos = _pos
            symbol = cipherWords[n][pos]
            for word in newDecrypted[n]:
                    # map possible letters
                    possible = word[pos]
                    newMap[symbol].append(possible)

        n +=1

    return newMap
    
            
def removeDuplicate(mapping):
    # removes duplictate keys
    for key in mapping.keys():

        for item in mapping[key]:

            mapping[key] = list(set(item))

    return mapping

                    


    
        

def checkWord(regex):
    # searches dictionary.txt for all words that match regex
    reList = []
    wordFile = open('dictionary.txt')
   
    for line in wordFile:
        regex = re.compile(regex)
        if re.match(regex,line[:-1]):

            reList.append(line[:-1])
    return reList  

    
    

                


if __name__ == '__main__':
    main()
