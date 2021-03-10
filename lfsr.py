class Lfsr:
    def __init__(self, initial_state: int = 1110011011, taps: tuple = (3, 5, 10)):
        """Class representing Linear Feedback Shift Register

        :param initial_state: initial state of the register
        :param taps: bits that influence the input
        """
        self.state = list(str(initial_state))
        self.taps = taps

    def calculate_feedback_bit(self):
        """Calculates feedback bit

        :return: feedback bit (int)
        """
        tap_bits = [int(self.state[tap-1]) for tap in self.taps]
        feedback = sum(tap_bits) % 2
        return feedback

    def shift(self):
        """Performs the shift operation on LFSR

        :return: output bit (int) obtained after the shift (the last bit of the register)
        """
        feedback = self.calculate_feedback_bit()
        new_state = [feedback]
        new_state.extend(self.state[:-1])
        output_bit = int(self.state[-1])
        self.state = new_state
        return output_bit
