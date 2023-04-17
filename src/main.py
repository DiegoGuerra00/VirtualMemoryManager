from queue import Queue
import json, random


class PageTableEntry:
    def __init__(self, valid, frame):
        self.valid = valid
        self.frame = frame


def main():
    fifoQueue = Queue(maxsize=256)  # Guarda apenas o índice das entradas na table
    pageTable = [PageTableEntry(False, None) for _ in range(256)]
    memory = [None] * 256  # Armazena apenas os dados, sendo o frame o índice

    addresses = open("assets/addresses.txt", "r")
    pages = loadJson()

    virtualMemory(pageTable, fifoQueue, memory, addresses, pages)


def virtualMemory(pageTable, fifoQueue, physicalMemory, addresses, swap):
    pageFaults = 0
    for address in addresses:
        print("\nAcessando endereço {}".format(address))
        pageNumber, pageOffset = translateAddress(address)
        pageNumber = convertBinToDec(str(pageNumber))
        pageOffset = convertBinToDec(str(pageOffset))

        print("Buscando page number: {}".format(pageNumber))

        for page in pageTable:
            if page.valid == True and page.frame == pageNumber:
                # FIXME: offset não funciona aparentemente
                print("Frame: {} Valido: {}".format(page.frame, page.valid))
                print("Valor presente na memória")
                print(
                    "Acessado valor {} a partir do offset {}".format(
                        physicalMemory[page.frame][pageOffset:], pageOffset
                    )
                )
                break
        else:
            # Busca na swap
            print("Valor não presente na memória...Buscando na swap")
            pageFaults += 1

            for page in swap:
                if page["page"] == pageNumber:
                    newFrame = findFreeFrame(pageTable, fifoQueue)
                    pageTable[int(newFrame)].valid = True
                    pageTable[int(newFrame)].frame = pageNumber
                    fifoQueue.put(newFrame)

                    physicalMemory[int(pageNumber)] = page["data"]

    print("Ocorreram um total de {} page faults".format(pageFaults))


def generateJson():
    swap = []
    for i in range(256):
        dict = {
            "page": i,
            "data": "".join([format(random.randint(0, 1), "b") for _ in range(256)]),
        }

        swap.append(dict)

    with open("assets/swap.json", "w") as f:
        json.dump(swap, f, indent=2)


def generateAddresses():
    addresses = []
    for _ in range(1000):
        tmp = ""
        for _ in range(16):
            tmp += str(random.randint(0, 1))
        addresses.append(tmp)

    with open("assets/addresses.txt", "w") as f:
        for address in addresses:
            f.write(str(address))
            f.write("\n")


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
    with open("assets/swap.json", "r") as f:
        pages = json.load(f)

    return pages


if __name__ == "__main__":
    generateJson()
    generateAddresses()
    main()
