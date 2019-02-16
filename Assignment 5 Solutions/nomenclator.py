# Ritvik Khanna (1479093) and Bisan Hasasneh (1505703) CMPUT299 Win2018
# Assignment 5 - Substitution Cipher Hacking
# This uses code from Hacking Secret Ciphers with Python by Al Sweigart
# Not much changes were made to this program except the part where the codebook is used.
import sys, random


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():

    # For testing purpose
    myMessage = 'At the University of Alberta, examinations take place in December and April for the Fall and Winter terms.' #For decryption
    #myMessage = 'Lj jia ! py Lmfacjl, # jlka bmlwa sx Oawanfac lxo Lbcsm ypc jia Ylmm lxo $ jacnr.' #For encryption
    
    myKey = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    myMode = 'encrypt' # set to 'encrypt' or 'decrypt'

    codeBook = {'university':'!', 'examination':'@', 'examinations':'#', 'WINTER':'$'}       
    checkValidKey(myKey) #Checking if the key is valid - same as original function

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, codeBook,myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey,codeBook, myMessage)

    print('The %sed message is:' % (myMode))
    print(translated)
    
def encryptMessage(subKey,codeBook,message):
    # Using the codebook first for encryption
    dictlower = {k.lower(): v for k,v in codeBook.items()}
    words = [word for word in message.split()]

    for i in range(len(words)):
        word = words[i].lower()
        if word in dictlower.keys():
            words[i]=dictlower[word]

    message1 = (' ').join(words)
    #After the encryption using the codebook encrypt with key substitution. 
    translated = ''
    charsA = LETTERS
    charsB = subKey

    for symbol in message1:
        if symbol.upper() in charsA:
             # encrypt/decrypt the symbol
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it
            translated += symbol

    return translated


def decryptMessage(subKey,codeBook,message):
    # First decrypt all the characters using the given key
    translated = ''
    charsA = subKey
    charsB = LETTERS

    for symbol in message:
        if symbol.upper() in charsA:
             # encrypt/decrypt the symbol
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it
            translated += symbol

    #After that replace the values with their keys from the codebook for decryption.

    translated = [word for word in translated.split()]
    
    for i in range(len(translated)):

        for key in codeBook.keys():

            if translated[i]==codeBook[key]:

                translated[i] = key

    translated = (' ').join(translated)    

    return translated
    

        
def checkValidKey(key):
    keyList = list(key)
    lettersList = list(LETTERS)
    keyList.sort()
    lettersList.sort()
    if keyList != lettersList:
        sys.exit('There is an error in the key or symbol set.')


def getRandomKey():
    key = list(LETTERS)
    random.shuffle(key)
    return ''.join(key)


if __name__ == '__main__':
    main()
