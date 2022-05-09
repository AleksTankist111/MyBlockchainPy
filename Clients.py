from Blockchains import Blockchain
from assetNode import *
from Transactions import Transaction


class Client:
    address = ""
    # TODO: вставить сюда блокчейн и функции по паблишингу новой ноды в него
    pass


if __name__ == '__main__':
    client = Client()
    bc = Blockchain(client_address=client.address)
    tr1 = Transaction(data={"from": "test1", "to": "test2", "amount": 5}, typeof="sell", fee=0.2)
    tr2 = Transaction(data={"from": "test2", "to": "test1", "amount": 5}, typeof="sell", fee=0.5)
    n = Node((tr1, tr2))
    print(bc.get_last_node().pred)
    bc.add_node(n, "", "")

    print(bc.get_last_node().hash)