# A toki pona to tokex converter v1.1
# Released under the MIT License, which should come with this file
# If not, see https://mit-license.org/ and read <copyright holders> as 5ucur
# (find me at https://github.com/5ucur)

# v1.1 new features:
# checking for non-toki pona chars
# stdin, write to binary file, bytes output
# input sanitisation
# output filename sanitisation (currently not confirmed for Windows!)
# help text (shows when run without arguments)

# Tokex is a hex encoding of the toki pona Latin alphabet,
# made by Abigail Read (https://github.com/AbbyRead)

# Toki pona is a minimalistic constructed language,
# made by Sonja Lang (https://lang.sg/)

# Takes input once run or via stdin, outputs in text or bytes to stdout
# or in bytes to a binary file. Doesn't implement Abigail's full stop
# conversion as of yet

# Now checks for non-toki pona characters and skips them
# Regardless, all errors or wrong output are still due to wrong input
# (garbage in, garbage out), and the _user's_ problem (also see license)


# For stdin and stdout
import sys, os

# Conversion dictionary
conv_dict = {
    "¤": "0", # Padding value, for words of odd length
    "i": "1",
    "u": "2",
    "w": "3",
    "j": "4",
    "s": "5",
    "o": "6",
    "l": "7",
    "n": "8",
    "m": "9",
    "a": "A",
    "p": "B",
    "k": "C",
    "t": "D",
    "e": "E",
    " ": "FF", # Space value, full byte, FFs as placeholder
}

# For later, if there's an output file argument
out_file = ""

# Custom filename sanitisation function
def clean(x: str):
    # Allow if the character given is alphanumeric, or fullstop, or slash
    if x.isalnum() or x in "./":
        return True
    else:
        return False

# Input sanitisation and exception handling
try:
    # Check if there's stdin and use it
    if len(sys.argv) > 1:
        # If stdin is a file, read its contents into the input var
        if os.path.isfile(sys.argv[1]):
            with open(sys.argv[1], "r") as in_file:
                in_raw = in_file.read()

        # Otherwise, use stdin literal
        else:
            in_raw = sys.argv[1]

        # If there's a second argument, and it's not a file already
        if len(sys.argv) > 2:
            if not os.path.isfile(sys.argv[2]):
                # Sanitise the argument and remember it as output filename
                out_file = "".join(x for x in sys.argv[2] if clean(x))
            else:
                print("Output file argument found, but file exists. Skipping output.")

    # No stdin? Use internal input
    else:
        # Print usage hints (in next version, will be available with --help)
        print(
            'Usage:',
            'python converter.py "text with spaces"',
            'python converter.py textwithoutspaces',
            'python converter.py input_file',
            'python converter.py <any-of-the-above-inputs> [output_file]',
            'python converter.py',
            '    (for internal input & no file output; you ran this)',
            'File output is binary only.',
            '',
            'Please input text (spaces allowed) to convert. '+
            'Characters not found in toki pona will be _ignored_.',
            sep="\n")
        # But also allow internal input
        in_raw = input("; ")

    # Process raw input:
    #  Put to lowercase
    #  Remove any leading/trailing whitespace
    #  Split into words
    in_text = in_raw.casefold().strip().split()

# Handle any exception that may arise
except Exception as e:
    print(f"An error occurred and the program must close:\n{e}")
    exit()

# Pad words that need padding, with a character
# that won't be found in any regular input
for word in in_text:
    if len(word) % 2:
        in_text[in_text.index(word)] += "¤"

# Reassemble the text by reinserting spaces
in_text = " ".join(in_text)

# If the reassembled text is a char too short, fix that
if len(in_text) % 2:
    in_text += "¤"

# List for output later
out_list = []

# List comprehension that takes pairs from the processe input string
for pair in [in_text[i:i+2] for i in range(0, len(in_text), 2)]:
    # Checks both halves of the pair, and assigns
    # the relevant hex digit or F for unallowed chars
    outLeft = conv_dict[pair[0]] if conv_dict.get(pair[0]) else "F"
    outRight = conv_dict[pair[1]] if conv_dict.get(pair[1]) else "F"
    # Make the hex digit pair for output
    out_pair = outLeft + outRight

    # Filtering out any double padding
    if out_pair != "00":
        out_list.append(out_pair)

    # Assemble the hex digit pairs into a full string ready for output
    out_str = "".join(out_list)

    # Replace space & error Fs with 0s, to facilitate reading
    # as 00 gets blanked out in some debuggers
    out_str = out_str.replace("F", "0")
    # Fix any doubled 00s arising from spacing & padding
    while "0000" in out_str:
        out_str = out_str.replace("0000", "00")
    # Strip trailing 00s
    out_str = out_str.rstrip("00")
    # Make sure the output is of even length
    # If odd length and the string ends in the pading 0, remove it
    if len(out_str) % 2:
        if out_str[-1] == "0":
            out_str = out_str[:-1]
        # If not padded, pad it
        else:
            out_str += "0"

# If the output filename argument was provided
if out_file:
    # Write the output in bytes into the file
    with open(out_file, "wb") as file:
        file.write(bytes.fromhex(out_str))
        # Write the EOF marker
        file.write(bytes.fromhex("FF"))
    print(f"Output written to {out_file}")

# Otherwise, output the finished string to stdout
# (uncomment one or more prints; in the next version, this will be choosable
# with arguments)
# Each one adds EOF marker FF
else:
    # in rows, pair by pair
    #print("\n".join([out_str[i:i+2] for i in range(0, len(out_str), 2)]) + "\nff")

    # in one row, in pairs
    print(" ".join([out_str[i:i+2] for i in range(0, len(out_str), 2)]), "ff")

    # in one row, in full
    #print(out_str+"ff")

    # in byte form
    #print(bytes.fromhex(out_str+"ff"))
