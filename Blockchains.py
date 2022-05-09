from assetNode import *


class Blockchain:
    def __init__(self, client_address: str):
        self.__nodes: list[Node, ...] = []
        generic = GenericNode()
        generic.publish_to(client_address=client_address, owner="")
        self.__nodes.append(generic)

    def get_last_node(self):                            # Сделать асинхронным?
        return self.__nodes[-1]

    def add_node(self, node: Node, client, owner):      # Сделать ассинхронным?
        last_node = self.get_last_node()
        node.publish_to(last_node, client, owner)
        if last_node == self.get_last_node():
            self.__nodes.append(node)
            node.confirm_publishing()
            self.check_validity()

    def len(self):
        return len(self.nodes)

    def check_validity(self):
        cur_test = self.__nodes[-1]
        if cur_test.hash != cur_test.calculate_hash():
            raise Exception(f"Error! Blockchain corrupted. Block {cur_test.node_id} has incorrect hash!")
        else:
            pred_hash = cur_test.pred
            for i in reversed(range(self.len()-1)):
                cur_test = self.__nodes[i]
                new_hash = cur_test.calculate_hash()
                if new_hash != pred_hash:
                    raise Exception(f"Error! Blockchain corrupted. Block's {cur_test.node_id} children has \
                        wrong pred hash!")
                if new_hash != cur_test.hash:
                    raise Exception(f"Error! Blockchain corrupted. Block {cur_test.node_id} has incorrect hash!")

    @property
    def nodes(self):
        return self.__nodes[:]
