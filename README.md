# StrongerSubstituitionCipher

## ASSIGNMENT 5
### Submitted By: Ritvik Khanna and Bisan Hasasneh

The code submitted is approximately 80% similar to the simpleSubHacker.py on the website inventwithpython.com/hacking by AI Sweigart.
Changes were made to hackSimpleSub() function and 3 new functions were made. The information regarding them is below:
* 1 - checkWord(): 
This function is used to find similar words using the regex expression for every word in the decrypted text which had ‘_’ in it and returns a list of those words. We use this loop and run it for every word in our message.

* 2 - removeDuplicate():
This function removes all the duplicate values for the mapping. For example after the new mapping the letter ‘H’ in the dictionary was ‘H’:[‘Y’,’Y’] so this function got rid of one ‘Y’ and made it just looked like ‘H’:[‘Y’].

* 3 - hacker():
This is the most important function and the biggest change we made in the program. It takes 2 parameters, the deciphered text (after 1st mapping) and the original cipher text. It creates a list of all words which have ‘_’ in them and also creates another list of the positions of those words in the text. This list is later used to find the corresponding cipherwords from the original ciphertext.
After this we call the checkWord() for every word with ‘_’ and then make a list of all possible words.
After we have that list we iterate through that list and map the cipherword character to the value returned by the checkWord(). This creates a new mapping just for the words containing ‘_’. We return this mapping to hackSimpleSub().

* 4 - hackSimpleSub():
After we get the returned new mapping from the hacker function we intersect the mapping obtained after the first run of hackSimpleSub() and the new mapping we obtained to get a finalMapping to decipher.

Once this finalMapping is obtained, this is passed through remveDuplicate() to get rid of any duplicate values in the mapping.
After this the decryptWithCipherletterMapping() with the final mapping and the original ciphertext. The value returned is stored in a variable and then this variable is returned along with the final decrypted text.


Apart from the changes mentioned in this readme file, nothing was changed to the original file and were obtained from inventwithpython.com/hacking as mentioned in the beginning.
Most of the things are commented throughout the program for better understanding.


If you have any concerns/questions you can email either one of us.
Thanks
Ritvik Khanna & Bisan Hasasneh
