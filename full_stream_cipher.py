from typing import Tuple


class FullStreamCipher:
    def __init__(self, lfsrs: Tuple, parse_tree: Tuple):
        """

        :param lfsrs: tuple of LFSRs
        :param parse_tree: parse tree representing used boolean function
        """
        self.lfsrs = lfsrs
        self.parse_tree = parse_tree
        self.index = 0
        self.validate_arguments()

    def validate_arguments(self):
        if len(self.lfsrs) < 2:
            raise ValueError("FullStreamCipher's lfsrs argument requires tuple of length at least 2")

    def shift(self):
        output_bits = tuple([lfsr.shift() for lfsr in self.lfsrs])
        return self.execute_parse_tree(output_bits)

    def execute_parse_tree(self, output_bits):
        root = self.parse_tree[self.index]
        self.index += 1
        if isinstance(root, str):
            return self.perform_operation(output_bits, root)
        elif isinstance(root, int):
            # parse_tree contains 1-based indices of output_bits (for user's convenience)
            return output_bits[root-1]
        else:
            raise TypeError("Incorrect type for the root of parse_tree of the boolean function")

    def perform_operation(self, output_bits, operation):
        try:
            children = list()
            if operation == 'not':
                children.append(self.parse_tree[self.index])
                self.index += 1
            elif operation in ['xor', 'and', 'or']:
                children.extend([self.parse_tree[self.index], self.parse_tree[self.index+1]])
                self.index += 2
            else:
                raise ValueError('Unrecognized operation')
            for index in range(len(children)):
                child = children[index]
                if isinstance(child, str):
                    children[index] = self.perform_operation(output_bits, child)
                elif isinstance(child, int):
                    children[index] = output_bits[child-1]
                else:
                    raise TypeError("Incorrect type for one of the nodes of parse_tree of the boolean function")
            if operation in ['xor', 'and', 'or']:
                left_child, right_child = children
                if operation == 'xor':
                    return (left_child + right_child) % 2
                if operation == 'and':
                    if left_child == 0 or right_child == 0:
                        return 0
                    return 1
                if operation == 'or':
                    if left_child == 1 or right_child == 1:
                        return 1
                    return 0
            else:
                return (children[0]+1) % 2

        except IndexError:
            raise IndexError("Invalid parse_tree. One of the binary connectives lacks two variables")
