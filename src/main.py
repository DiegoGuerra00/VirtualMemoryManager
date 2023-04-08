from queue import Queue
import json


class PageTableEntry:
    def __init__(self, valid, frame):
        self.valid = valid
        self.frame = frame


def main():
    pageFaults = 0

    pageQueue = Queue(maxsize=256)
    pageTable = [PageTableEntry(False, None) for _ in range(256)]
    # TODO implementar memório física (array representando os 64kB)

    addresses = open("assets/addresses.txt", "r")
    pages = loadJson()

    for address in addresses:
        print(address)
        pageNumber, pageOffset = translateAddress(address)


def findFreeFrame(pageTable):
    for i, entry in enumerate(pageTable):
        if not entry.valid:
            # Se tiver um frame vazio o retorna
            return i
        else:
            # Não existem frames livres, precisa chamar o FIFO
            return -1


# Recebe o binário como string e converte para decimal
def convertBinToDec(binNumber):
    return int(binNumber, 2)


def translateAddress(address):
    pageNumber = address[:8]
    pageOffset = address[8:]

    return pageNumber, pageOffset


def loadJson():
    with open("assets/pages.json", "r") as f:
        pages = json.load(f)

    return pages


if __name__ == "__main__":
    main()
