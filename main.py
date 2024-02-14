import os, re


def cls():
    os.system("clear")


def println(data):
    print(data, end="\n\n")


def patMatch(data, patten):
    matches = patten.finditer(data)
    positions = []
    for match in matches:
        positions.append(match.start())

    return positions


def extractMLog(dumpPath):
    print("Reading file...\n")

    with open(dumpPath, "rb") as dumpfile:
        rawData = dumpfile.read()

    println("Extracting MLogs...")

    mlogPat = re.compile(rb"MLog")
    mlogPos = patMatch(rawData, mlogPat)

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


def parseMLog(data):
    cls()

    signature = data[:4]
    entryID = data[4:8]
    entySize = data[12:16]
    entryUUID = data[16:32]
    control = data[32:36]
    currentMLLSN = data[40:48]
    prevMLLSN = data[48:56]
    entryHeaderSize = data[84:88]

    entryHeader = {}

    keys = [
        "Signature",
        "Entry ID",
        "Enty Size",
        "Entry UUID",
        "Control",
        "Current ML LSN",
        "Previous ML LSN",
        "Entry Header Size",
    ]

    values = [
        signature,
        entryID,
        entySize,
        entryUUID,
        control,
        currentMLLSN,
        prevMLLSN,
        entryHeaderSize,
    ]

    for i in range(len(keys)):
        entryHeader[keys[i]] = values[i]

    currentMLLSN = data[120:128]
    checksum = data[128:136]
    prevMLLSN = data[144:152]
    dataAreaSize = data[152:156]
    logRecordHDRSize = data[160:164]
    logRecordSize = data[164:168]
    type_unknown = data[168:176]

    logRecordHeader = {}

    keys = [
        "Current ML LSN",
        "Checksum",
        "Previous ML LSN",
        "Data Area Size",
        "Log Record HDR Size",
        "Log Record Size",
        "Type [unknown]",
    ]

    vaues = [
        currentMLLSN,
        checksum,
        prevMLLSN,
        dataAreaSize,
        logRecordHDRSize,
        logRecordSize,
        type_unknown,
    ]

    for i in range(len(keys)):
        logRecordHeader[keys[i]] = values[i]

    for i in range(len(entryHeader)):
        println(f"{list(entryHeader.keys())[i]:<20}:  {list(entryHeader.values())[i]}")

    for i in range(len(logRecordHeader)):
        println(
            f"{list(logRecordHeader.keys())[i]:<20}:  {list(logRecordHeader.values())[i]}"
        )

    input()
    cls()


def parseLogFile(path):
    println("Reading File...")

    with open(path, "rb") as logfile:
        logFileData = logfile.read()

    mlogPat = re.compile(rb"MLog")
    mlogPos = patMatch(logFileData, mlogPat)

    mlogSize = mlogPos[1] - mlogPos[0]
    print(f"MLog matches found at: {[hex(i) for i in mlogPos]}\n")
    print(f"MLog Size: {mlogSize}\n")
    print(f"MLog Count: {len(mlogPos)}\n")

    inp = input("View each entry? [y] ").lower()

    if inp == "y":
        for i in range(len(mlogPos)):
            if i != len(mlogPos) - 1:
                parseMLog(logFileData[mlogPos[i] : mlogPos[i + 1]])
            else:
                parseMLog(logFileData[mlogPos[i] :])
    else:
        cls()
        return None


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
    dumpFilePath = "../Chall-Test/UpdatedFile.001"
    logFilePath = "LogFile"
    main(dumpFilePath, logFilePath)
