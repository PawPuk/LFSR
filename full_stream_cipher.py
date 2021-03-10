from lfsr import Lfsr
from typing import Tuple


class Node:
    def __init__(self, value, index):
        self.value = value
        # 1-based index
        self.index = index


class FullStreamCipher:
    def __init__(self, lfsrs: Tuple, parse_tree: Tuple):
        """

        :param lfsrs: tuple of LFSRs
        :param parse_tree: parse tree representing used boolean function
        """
        self.lfsrs = lfsrs
        self.parse_tree = parse_tree
        self.validate_arguments()

    def validate_arguments(self):
        if len(self.lfsrs) < 2:
            raise ValueError("FullStreamCipher's lfsrs argument requires tuple of length at least 2")

    def shift(self):
        output_bits = tuple([lfsr.shift() for lfsr in self.lfsrs])
        return self.execute_parse_tree(output_bits)

    def execute_parse_tree(self, output_bits):
        root = Node(self.parse_tree[0], 1)
        if isinstance(root.value, str):
            return self.perform_operation(output_bits, root.value, root.index)
        elif isinstance(root.value, int):
            # parse_tree contains 1-based indices of output_bits (for user's convenience)
            return output_bits[root.value-1]
        else:
            raise TypeError("Incorrect type for the root of parse_tree of the boolean function")

    def perform_operation(self, output_bits, operation, parent_index: int):
        try:
            left_child = Node(self.parse_tree[parent_index*2-1], parent_index*2)
            right_child = Node(self.parse_tree[parent_index*2], 1+parent_index*2)
            for child in (left_child, right_child):
                if isinstance(child.value, str):
                    child.value = self.perform_operation(output_bits, child.value, child.index)
                elif isinstance(child.value, int):
                    child.value = output_bits[child.value-1]
                else:
                    raise TypeError("Incorrect type for one of the nodes of parse_tree of the boolean function")
            if operation == 'xor':
                return (left_child.value + right_child.value) % 2
            if operation == 'and':
                if left_child.value == 0 or right_child.value == 0:
                    return 0
                return 1
            if operation == 'or':
                if left_child.value == 1 or right_child.value == 1:
                    return 1
                return 0

        except IndexError:
            raise IndexError("Invalid parse_tree. One of the binary connectives lacks two variables")
