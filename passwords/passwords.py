import hashlib
import binascii

def hashString(string):
    encodedPassword = string.encode('utf-8')
    hasher = hashlib.sha256(encodedPassword)
    digest = hasher.digest() 
    digestAsHex = binascii.hexlify(digest)
    digestAsHexString = digestAsHex.decode('utf-8')
    return digestAsHexString


def part1(wordsFile, passwordsFile, crackedFile):
    # build a digestToWord dictionary
    digestToWord = {}
    words = [line.strip().lower() for line in open(wordsFile)]
    for word in words:
        digestAsHexString = hashString(word)
        if digestAsHexString not in digestToWord:
            digestToWord[digestAsHexString] = word

    # write onto a new file of cracked passwords
    passwords = [line.strip().lower() for line in open(passwordsFile)]
    with open(crackedFile, 'w') as f:
        for password in passwords:
            hash = password.split(":",2) 
            if hash[1] in digestToWord:
                f.write(hash[0]+":"+digestToWord[hash[1]]+"\n")

def part2(wordsFile, passwordsFile, crackedFile):
    # create the list of passwords
    usersList = [line.strip().lower().split(":")[0] for line in open(passwordsFile)]
    digestsList = [line.strip().lower().split(":")[1] for line in open(passwordsFile)]
    digestToUser = {}
    for i in range(len(digestsList)):
        digestToUser[digestsList[i]] = usersList[i]
    crackedPasswords = [] # each entry is [user, password]
    words = [line.strip().lower() for line in open(wordsFile)]
    done = False
    for idx in range(1001, len(words)):
        i = words[idx]
        for j in words:
            digestAsHexString = hashString(i+j)
            if digestAsHexString in digestsList:
                crackedPasswords.append([digestToUser[digestAsHexString], i+j])
                if len(crackedPasswords) >= 300:
                    done = True
        if done:
            break
    # write in the crackedFile
    with open(crackedFile, 'w') as f:
        for crackedPassword in crackedPasswords:
            f.write(crackedPassword[0]+":"+crackedPassword[1]+"\n")

def part3(wordsFile, passwordsFile, crackedFile):
    words = [line.strip().lower() for line in open(wordsFile)]
    passwords = [line.strip().lower() for line in open(passwordsFile)]
    with open(crackedFile, 'w') as f:
        for password in passwords:
            a = password.split(":",2)
            b = a[1].split("$")
            user = a[0]
            salt = b[2]
            digest = b[3]
            for word in words: 
                digestAsHexString = hashString(salt+word)
                if digestAsHexString == digest:
                    f.write(user+":"+word+"\n")
                    break

# part1("words.txt", "passwords1.txt", "cracked1.txt")
# part2("words.txt", "passwords2.txt", "cracked2.txt")
part3("words.txt", "passwords3.txt", "cracked3.txt")


## miscellaneous

def checkDuplicates():
    # From this we learned that no user shares the same password
    # This is helpful to optimize memory when cracking for part2
    digestsList = [line.strip().lower().split(":")[1] for line in open("passwords2.txt")]
    s = set()
    for i in digestsList:
        if i in s:
            print("DUPLICATES")
        else:
            s.add(i)