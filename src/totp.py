import time
import hashlib
import hmac
import base64
import math


class TOTP:

    """Class for storing and using TOTP data
    
    A class for storing parameters for and generating TOTP codes.
    Includes a number of util functions useful for TOTP applications 
    """

    def __init__(self, key:str, algorithm:str="sha1", digits:int=6, period:int=30):
        
        #some sanitisation and padding for the key input
        key = key.replace(" ","")
        paddingSize = len(key) % 8
        self.key = key+"="*paddingSize

        self.algorithm = algorithm
        self.digits = digits
        self.period = period
    

    def generateCode(self, givenTime:int=time.time()) -> str:
        """Generate a TOTP code for the time passed in, or the current time."""
        
        #convert and pad time and key value for digest
        timeCounter = self.counterFromTime(givenTime)
        timeCounter = str(hex(timeCounter)[2:])
        timeCounter = '0'*(16-len(timeCounter)) + timeCounter
        byteTime = bytes.fromhex(timeCounter)
        key = base64.b32decode(self.key)

        #create hex digest of the key and the time counter
        digester = hmac.new(key, byteTime, hashlib.sha1)
        digest = digester.hexdigest()
        offset = int(digest[-1:], 16)

        splitDigest = [digest[i: i + 2] for i in range(0, len(digest), 2)]
        finalDigest = splitDigest[offset:offset+4]

        #generate code from digest
        fullcode = ""
        for i in finalDigest:
            nextnum = str(bin(int(i,16)))
            nextnum = nextnum[2:]
            nextnum = '0'*(8-len(nextnum)) + nextnum
            fullcode += nextnum

        #slice unneeded values to get final code
        fullcode = fullcode[1:]
        code = str(int(fullcode,2))[-self.digits:]
        
        return code


    def counterFromTime(self, givenTime:int=time.time(), period:int=30) -> int:
        """Takes the given time and period, and returns the counter value."""

        return math.floor((givenTime - 0) / period)


    def timeToNextCode(self, givenTime:int, period: int=30):
        """Takes the given time and period and returns the time remaining to the next code."""

        currentCounter = self.counterFromTime(givenTime, period)
        nextCounter = currentCounter + 1

        return nextCounter*period-givenTime


def main():
    """A simple test function allowing command line code TOTP generation"""

    key = input("Enter TOTP key for testing: ")
    totp = TOTP(key)

    currentTime = time.time()
    print("Current code is: "+totp.generateCode())
    print("Time to next code: ",totp.timeToNextCode(currentTime))
    return


if __name__ == "__main__":
    main()

