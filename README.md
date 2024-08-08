

## Turing Machine
Simple little emulator of a turing machine that operates on strings and chars. Just define your symbols, transition function, add an input tape and it should work.

### Nuances

This machine does not allow writing in the 'Blank' area. This would need some kind of a virtual store of symbols you write past the end of symbols, and then join this to the input string at the end.
