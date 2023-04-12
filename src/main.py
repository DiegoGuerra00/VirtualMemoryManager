from queue import Queue
import json


class PageTableEntry:
    def __init__(self, valid, frame):
        self.valid = valid
        self.frame = frame


def main():
    pageFaults = 0

    fifoQueue = Queue(maxsize=256)  # Guarda apenas o índice das entradas na table
    pageTable = [PageTableEntry(False, None) for _ in range(256)]
    memory = [None] * 256  # Armazena apenas os dados, sendo o frame o índice

    addresses = open("assets/addresses.txt", "r")
    pages = loadJson()

    """
    O frame é o índice do array representando a memória física.
    A page number buscada será o índice da page table
    Se for válido busca na memoria no indice indicado pelo frame da page table
    Se nao for válido busca na swap e carrega na memoria e page table
    """
    virtualMemory(pageTable, fifoQueue, memory, addresses, pages)


def virtualMemory(pageTable, fifoQueue, physicalMemory, addresses, swap):
    pageFaults = 0
    for address in addresses:
        print("Acessando endereço {}".format(address))
        pageNumber, pageOffset = translateAddress(address)
        pageNumber = convertBinToDec(str(pageNumber))
        pageOffset = convertBinToDec(str(pageOffset))

        print("Buscando page number: {}".format(pageNumber))

        # FIXME: nunca entre no primeiro if pq ta errado, provavelmente
        if PageTableEntry(True, pageNumber) in pageTable:
            i = pageTable.index(PageTableEntry(True, pageNumber))
            # TODO: Levar em conta o offset
            print("Valor presente na memória")
            print("Acessado valor {}: ".format(physicalMemory[i]))
        else:
            print("Valor não presente na memória...Buscando na swap")
            # Busca na swap
            pageFaults += 1

            for page in swap:
                if page["page"] == int(pageNumber):
                    # TODO: Tratar FIFO cheia
                    newFrame = findFreeFrame(pageTable, fifoQueue)
                    pageTable[int(pageNumber)].valid = True
                    pageTable[int(pageNumber)].frame = newFrame
                    fifoQueue.put(newFrame)

                    physicalMemory[int(pageNumber)] = page["data"]


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
