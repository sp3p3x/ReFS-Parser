import re


def extractMLog(rawData):
    mlogPat = re.compile(rb"MLog")
    mlogMatches = mlogPat.finditer(rawData)
    mlogPos = []
    for match in mlogMatches:
        mlogPos.append(match.start())

    mlogSize = mlogPos[1] - mlogPos[0]
    print(f"MLog matches found at: {[hex(i) for i in mlogPos]}\n")
    print(f"MLog Size: {mlogSize}\n")
    print(f"MLog Count: {len(mlogPos)}\n")
    startPos = input("Range to extract MLog [start]: ")
    endPos = input("Range to extract MLog [end]: ")

    if startPos == "":
        startPos = 0
    else:
        try:
            startPos = int(startPos)
            startPos = startPos - 1
        except:
            print("Invalid input!")

    if endPos == "":
        endPos = len(mlogPos)
    else:
        try:
            endPos = int(endPos)
        except:
            print("Invalid input!")

    mlogData = rawData[mlogPos[startPos] : mlogPos[endPos - 1] + mlogSize]

    print(f"\nWriting {(endPos)-(startPos)} MLog's into LogFile...")

    with open("LogFile", "wb") as logfile:
        logfile.write(mlogData)

    print("MLog data written to LogFile...")


def parseLogFile(path):
    pass


def main(dumpPath, logfilePath):
    if input("Extract LogFile? [y] ").lower() == "y":
        print("Reading file...\n")
        rawData = open(dumpPath, "rb").read()
        extractMLog(rawData)
    else:
        parseLogFile(logfilePath)


if __name__ == "__main__":
    dumpFile = "../Chall-Test/UpdatedFile.001"
    logFile = "LogFile"
    main(dumpFile, logFile)
