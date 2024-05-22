import os, re, sys


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


def parseEntryHeader(data):

    signature = data[:4]
    entryID = data[4:8]
    # unknown bytes: 4
    entrySize = data[12:16]
    entryUUID = data[16:32]
    control = data[32:36]
    # unknown bytes: 4
    currentMLLSN = data[40:48]
    prevMLLSN = data[48:56]
    # unknown bytes: 28
    entryHeaderSize = data[84:88]
    # unknown bytes: 32

    keys = [
        "Signature",
        "Entry ID",
        "Entry Size",
        "Entry UUID",
        "Control",
        "Current ML LSN",
        "Previous ML LSN",
        "Entry Header Size",
    ]

    values = [
        signature,
        entryID,
        entrySize,
        entryUUID,
        control,
        currentMLLSN,
        prevMLLSN,
        entryHeaderSize,
    ]

    println(f"{'Entry Header':-^55}")

    for i in range(len(keys)):
        println(f"{keys[i]:.<20}:  {values[i]}")


def parseLogRecordHeader(data):
    currentMLLSN = data[120:128]
    checksum = data[128:136]
    # unknown bytes: 8
    prevMLLSN = data[144:152]
    dataAreaSize = data[152:156]
    # unknown bytes: 4
    logRecordHDRSize = data[160:164]
    logRecordSize = data[164:168]
    typeValue = data[168:176]

    keys = [
        "Current ML LSN",
        "Checksum",
        "Previous ML LSN",
        "Data Area Size",
        "Log Record HDR Size",
        "Log Record Size",
        "Type",
    ]

    values = [
        currentMLLSN,
        checksum,
        prevMLLSN,
        dataAreaSize,
        logRecordHDRSize,
        logRecordSize,
        typeValue,
    ]

    println(f"{'Log Record Header':-^55}")

    for i in range(len(keys)):
        if keys[i] == "Data Area Size":
            println(
                f"{keys[i]:.<20}:  {values[i]} -> {hex(int.from_bytes(values[i],'little'))} -> {int(hex(int.from_bytes(values[i],'little'))[2:],16)}"
            )
        else:
            println(f"{keys[i]:.<20}:  {values[i]}")


def parseRedoRecord(data):
    redoRecordSize = data[176:180]
    opcode = data[180:184]
    tableKeysCount = data[184:188]
    tableKeysOffset = data[188:192]
    valueCount = data[192:196]
    valueOffset = data[196:200]
    # unknown bytes: 20
    recordMark = data[220:224]
    sequenceNumber = data[224:228]
    endMark = data[228:232]

    keys = [
        "Redo Record Size",
        "Opcode",
        "Table Keys Count",
        "Table Keys Offset",
        "Value Count",
        "Value Offset",
        "Record Mark",
        "Sequence Number",
        "End Mark",
    ]

    values = [
        redoRecordSize,
        opcode,
        tableKeysCount,
        tableKeysOffset,
        valueCount,
        valueOffset,
        recordMark,
        sequenceNumber,
        endMark,
    ]

    println(f"{'Redo Record Header':-^55}")

    for i in range(len(keys)):
        println(f"{keys[i]:.<20}:  {values[i]}")


def parseMLog(data):
    cls()

    parseEntryHeader(data)

    parseLogRecordHeader(data)

    parseRedoRecord(data)

    foo = input("Press [q] to return to menu! ")
    cls()
    return foo


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
                if parseMLog(logFileData[mlogPos[i] : mlogPos[i + 1]]).lower() == "q":
                    break
            else:
                if parseMLog(logFileData[mlogPos[i] :]).lower() == "q":
                    break
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
        [3/q] Exit            

        Choice: """
        )

        if choice == "1":
            cls()
            extractMLog(dumpPath)
        elif choice == "2":
            cls()
            parseLogFile(logfilePath)
        elif choice == "3" or choice.lower() == "q":
            cls()
            exit()
        else:
            println("Enter valid input!")
            cls()


def main(dumpPath, logfilePath):
    cli(dumpPath, logfilePath)


if __name__ == "__main__":
    if sys.argv[0] != "":
        dumpFilePath = os.path.join(sys.argv[0])
        logFilePath = os.path.join(sys.argv[0])
        main(dumpFilePath, logFilePath)
    else:
        print("Usage: python3 main.py {path to logfile/dumpfile}")
