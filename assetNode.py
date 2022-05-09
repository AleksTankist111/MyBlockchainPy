from __future__ import annotations

from typing import Optional

from Transactions import Transaction
from Wallets import Wallet
from dataclasses import dataclass


@dataclass(eq=True, frozen=False)
class Body:
    transactions: tuple[Transaction, ...]
    fee: int
    node_id: Optional[int]
    client: Optional[str]
    owner: Optional[str]
    pred: Optional[str]
    seed: int

    def __hash__(self):
        return hash((self.transactions, self.fee, self.node_id, self.client, self.owner, self.pred, self.seed))


class Node:
    __MAX_SIZE = 8 * 1024           # использовать getsizeof
    __GAS = 0.01                    # constant for now

    @classmethod
    def __RULE(cls, hashed: str):    # поиграть с правилами
        if hashed[:3] == '123':
            return True
        else:
            return False

    @classmethod
    def _hashing(cls, self):
        self.__hash = str(hash(self.__body))
        while not self.__RULE(self.__hash):
            self.__body.seed += 1
            self.__hash = str(hash(self.__body))

    def __init__(self, transactions: tuple[Transaction, ...] = ()):
        if sum(transaction.get_size() for transaction in transactions) > self.__MAX_SIZE:
            raise Exception("Error: Too big data on the node.")
        self.__body = Body(transactions=transactions, fee=sum(transaction.fee for transaction in transactions),
                           node_id=None, client=None, owner=None, pred=None, seed=0)
        self.__hash = None
        self.__is_published = False

    def publish_to(self, last_node, client_address: str, owner: str) -> Node:
        # here should be also implemented algorithm of third-party approving transaction?
        if not self.__is_published:
            self.__body.owner = owner
            self.__body.client = client_address
            self.__body.node_id = last_node.node_id + 1
            self.__body.pred = last_node.hash
            self._hashing(self)
            return self
        else:
            raise Exception("Error while hashing: Node has already published")

    def confirm_publishing(self):
        if self.__is_published:
            raise Exception("Error while confirming publishing: Node has already published")
        self.__is_published = True

    def calculate_hash(self):
        return str(hash(self.__body))

    # Properties
    @property
    def transactions(self):
        return self.__body.transactions

    @property
    def owner(self):
        return self.__body.owner

    @property
    def hash(self):
        return self.__hash

    @property
    def pred(self):
        return self.__body.pred

    @property
    def client(self):
        return self.__body.client

    @property
    def fee(self):
        return self.__body.fee

    @property
    def node_id(self):
        return self.__body.node_id

    @property
    def gas(self):
        return self.__GAS


class GenericNode(Node):
    def __init__(self):
        super().__init__()
        self.__body = Body(transactions=tuple(), fee=0,
                           node_id=None, client=None, owner=None, pred=None, seed=0)
        self.__hash = None
        self.__is_published = False

    def publish_to(self, client_address: str, owner: str) -> Node:
        if not self.__is_published:
            self.__body.owner = owner
            self.__body.client = client_address
            self.__body.pred = 0
            self.__body.node_id = 0
            self._hashing(self)

            return self
        else:
            raise Exception("Error while hashing: Node has already published")

    @property
    def transactions(self):
        return self.__body.transactions

    @property
    def owner(self):
        return self.__body.owner

    @property
    def pred(self):
        return self.__body.pred

    @property
    def client(self):
        return self.__body.client

    @property
    def fee(self):
        return self.__body.fee

    @property
    def node_id(self):
        return self.__body.node_id


# TESTING:
if __name__ == '__main__':
    aaa = hash(Body(None, None, None, None, None, None, seed=0))
    print(aaa)
    aaa = hash(Body(None, None, None, None, None, None, seed=2))
    print(aaa)
    x = Body(None, None, None, None, None, None, seed=0)
    bbb = hash(x)
    print(bbb)
    x.seed += 2
    print(hash(x))
    b = Transaction()
    b.fee = 5
    c = Transaction()
    c.fee = 10
    a = Node(transactions=(b, c))
    x = GenericNode()
    print(a.transactions)
