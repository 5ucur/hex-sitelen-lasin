# tokex-convert-py
A toki pona to tokex converter, v1.1

Takes input once run or via stdin, outputs in text or bytes to stdout, or in bytes to a binary file. Doesn't implement the Tokex full stop conversion as of yet.

Since v1.1, checks for non-toki pona characters and skips them. Regardless, all wrong output is due to wrong input (garbage in, garbage out), and the _user's_ problem (also see license).

### v1.1 new features:
- Checking for non-toki pona characters
- Stdin from file or console, output to binary file, output in bytes format
- Input sanitisation
- Output filename sanitisation (currently not confirmed for Windows!)
- Help text (shows when run without arguments)

## What is Tokex?
[Tokex](https://github.com/AbbyRead/Tokex/) is a hex encoding of the toki pona Latin alphabet, created by [Abigail Read](https://github.com/AbbyRead).

## What is toki pona?
[Toki pona](https://tokipona.org/) is a minimalistic constructed language, made by [Sonja Lang](https://lang.sg/)
