from lfsr import Lfsr
from full_stream_cipher import FullStreamCipher


def prepare_table():
    LFSR1 = Lfsr(initial_state=1010, taps=(4,))
    LFSR2 = Lfsr(initial_state=1100, taps=(4,))
    return LFSR1, LFSR2


def logic_table(operation: str):
    if operation not in ["or", "and", "xor"]:
        raise ValueError("Incorrect operation")
    LFSR1, LFSR2 = prepare_table()
    my_tuple = LFSR1, LFSR2
    parse_tree = operation, 1, 2
    for _ in range(4):
        fullStreamCipher = FullStreamCipher(my_tuple, parse_tree)
        print(str(LFSR1.state[-1]) + " "+operation+" " + str(LFSR2.state[-1]) + " = " + str(fullStreamCipher.shift()))


def geffe_generator():
    LFSR1 = Lfsr(initial_state=10101010, taps=(8,))
    LFSR2 = Lfsr(initial_state=11001100, taps=(8,))
    LFSR3 = Lfsr(initial_state=11110000, taps=(8,))
    my_tuple = LFSR1, LFSR2, LFSR3
    parse_tree = "xor", "and", "and", 1, 2, "not", 3, 1
    for _ in range(8):
        fullStreamCipher = FullStreamCipher(my_tuple, parse_tree)
        print(str(LFSR1.state[-1]) + ", " + str(LFSR2.state[-1]) + ", " + str(LFSR3.state[-1]) +
              " => " + str(fullStreamCipher.shift()))


geffe_generator()
# logic_table("xor")
# logic_table("or")
# logic_table("and")

# print(LFSR1.state)
# print(LFSR1.calculate_feedback_bit())
# print(LFSR1.shift())
# print(LFSR1.state)
# print(LFSR1.calculate_feedback_bit())
