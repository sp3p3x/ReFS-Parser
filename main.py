import os, re


def cls():
    os.system("clear")


def println(data):
    print(data, end="\n\n")


def extractMLog(dumpPath):
    print("Reading file...\n")
    rawData = open(dumpPath, "rb").read()

    println("Extracting MLogs...")

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
    cls()


def parseLogFile(path):
    pass


def cli(dumpPath, logfilePath):
    while True:

        choice = input(
            f"""
        {'ReFS Parser':^30}\n
        [1]  Extract LogFile
        [2]  Parse LogFile
        [3/e] Exit            

        Choice: """
        )

        if choice == "1":
            cls()
            extractMLog(dumpPath)
        elif choice == "2":
            cls()
            parseLogFile(logfilePath)
        elif choice == "3" or choice.lower() == "e":
            cls()
            exit()
        else:
            println("Enter valid input!")
            cls()


def main(dumpPath, logfilePath):
    cli(dumpPath, logfilePath)


if __name__ == "__main__":
    dumpFile = "../Chall-Test/UpdatedFile.001"
    logFile = "LogFile"
    main(dumpFile, logFile)
