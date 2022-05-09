from hashlib import sha256
from sys import getsizeof


class Transaction:
    def __init__(self, data=None, typeof: str = "test", fee: float = 0):
        if data is None:
            data = {}
        if type(data) is not dict:
            raise Exception(f"Error: data has a wrong format ({type(data)}), expected: dict")
        self.fee = fee
        self.data = data
        self.type = typeof

    def __repr__(self):
        return f"<Transaction with fee={self.fee} and data={self.data}>"

    def get_size(self) -> int:
        size = getsizeof(self.data)
        for key in self.data.keys():
            size += getsizeof(key)
            size += getsizeof(self.data[key])
        return size

