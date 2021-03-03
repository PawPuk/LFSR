from lfsr import Lfsr
# from full_stream_cipher import FullStreamCipher

LFSR1 = Lfsr()
LFSR2 = Lfsr(initial_state=110011011)
# my_tuple = LFSR1,
# fullStreamCipher = FullStreamCipher(my_tuple, None)

print(LFSR1.state)
print(LFSR1.calculate_feedback_bit())
print(LFSR1.shift())
print(LFSR1.state)
print(LFSR1.calculate_feedback_bit())
