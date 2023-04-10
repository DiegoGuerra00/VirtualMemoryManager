from queue import Queue
import json


class PageTableEntry:
    def __init__(self, valid, frame):
        self.valid = valid
        self.frame = frame


def main():
    pageFaults = 0

    fifoQueue = Queue(maxsize=256)
    pageTable = [PageTableEntry(False, None) for _ in range(256)]
    memory = [None] * 256

    addresses = open("assets/addresses.txt", "r")
    pages = loadJson()

    for address in addresses:
        print(address)
        pageNumber, pageOffset = translateAddress(address)

        # FIXME: Certeza que não vai funcionar
        if PageTableEntry(True, pageNumber) in pageTable:
            i = pageTable.index(PageTableEntry(True, pageNumber))
            # TODO: Levar em conta o offset
            print("Acessado valor {} da memória física".format(memory[i]))
        else:
            pageFaults += 1
            # Busca na swap


def findFreeFrame(pageTable, fifoQueue):
    for i, entry in enumerate(pageTable):
        if not entry.valid:
            # Se tiver um frame vazio o retorna
            return i
        else:
            # Não existem frames livres, precisa chamar o FIFO
            frameToRemove = fifoQueue.get()
            pageTable[frameToRemove].valid = False
            return frameToRemove


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
