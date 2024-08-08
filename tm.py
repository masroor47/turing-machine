

class BadTapeInputException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors



class TuringMachine:
    def __init__(self, 
                 states, 
                 alphabet, 
                 symbols, 
                 init_state, 
                 transition_function):
        self.MAX_STEPS = 1000
        self.states = states
        self.alphabet = alphabet
        self.symbols = symbols
        self.state = init_state
        self.transition_function = self.dictify(transition_function)
        self.head_idx = 0

    def __call__(self, tape):
        tape = list(tape)
        self.head_idx = 0
        halt = False
        steps = 0
        while not halt:
            # print(f'{self.head_idx = }\n{tape}')
            curr_symbol = tape[self.head_idx] if self.head_idx < len(tape) else 'B'
            if (self.state, curr_symbol) not in self.transition_function:
                halt = True
                break

            new_state, symbol_to_write, direction = self.transition_function[(self.state, curr_symbol)]
            direction = direction.lower()

            if new_state not in self.states:
                raise BadTapeInputException(f'New state {new_state} is not in set of allowed states')
            if symbol_to_write not in self.symbols:
                raise BadTapeInputException(f'Symbol to write {symbol_to_write} not in set of allowed symbols')
            if direction not in ('l', 'r'):
                raise BadTapeInputException(f'Direction {direction} not "l" or "r"')
            if self.head_idx == 0 and direction == 'l':
                raise BadTapeInputException('Trying to move head to the left at leftmost position')

            self.state = new_state
            if self.head_idx >= len(tape):
                if symbol_to_write != 'B':
                    raise BadTapeInputException('Trying to write non-blank symbol in the blank area')
                # don't write 'B', the blank area is imaginary
            else:
                tape[self.head_idx] = symbol_to_write
            self.head_idx += 1 if direction == 'r' else -1

            steps += 1
            if steps > self.MAX_STEPS:
                # probably diverges
                # can someone write code to verify for sure if it diverges?
                break

        return ''.join(tape), self.head_idx, halt
            
    def dictify(self, transition_function):
        dictified = {}
        for row in transition_function:
            state, symbol = row[:2] 
            dictified[(state, symbol)] = row[2:]
        return dictified


def make_bit_flipper_tm():
    states = {'q', 'p', 's', 't', 'f'}
    alphabet = {'0', '1'}
    symbols = {'N', 'Z', '0', '1', 'B'}
    init_state = 'q'
    trans = [
        ('q', '0', 'p', 'N', 'R'),
        ('q', '1', 'p', 'Z', 'R'),
        ('p', '0', 'p', '1', 'R'),
        ('p', '1', 'p', '0', 'R'),
        ('p', 'B', 's', 'B', 'L'),
        # ('p', 'B', 'p', 'B', 'R'), # diverges if the following tuple is replaced with the above
        ('s', '0', 's', '0', 'L'),
        ('s', '1', 's', '1', 'L'),
        ('s', 'N', 't', '1', 'R'),
        ('s', 'Z', 't', '0', 'R'),
        ('t', '0', 'f', '0', 'L'),
        ('t', '1', 'f', '1', 'L'),
    ]

    return states, alphabet, symbols, init_state, trans

if __name__ == '__main__':
    states, alphabet, symbols, init_state, trans = make_bit_flipper_tm()
    M = TuringMachine(states, alphabet, symbols, init_state, trans)
    tape_1 = '11001100'

    tape_out, head_idx, halted = M(tape_1)
    print(f"TM {'halted' if halted else 'diverged'} with result tape:\n{tape_out}\n{head_idx = }")


