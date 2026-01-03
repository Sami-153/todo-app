def findAlphabeticallyLastWord(sentence):
    if sentence=="":
        return ""
    
    lastAlphabeticWord = sentence.split()
    lastAlphabeticWord.sort()
    print(lastAlphabeticWord)
    return lastAlphabeticWord[-1]

print(findAlphabeticallyLastWord("What is the last word in this sentence ?"))