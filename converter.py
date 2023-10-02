# A toki pona to tokex converter
# Released under the MIT License, which should come with this file
# If not, see https://mit-license.org/ and read <copyright holders> as 5ucur
# (find me at https://github.com/5ucur)

# Tokex is a hex encoding of the toki pona Latin alphabet,
# made by Abigail Read (https://github.com/AbbyRead)

# Toki pona is a minimalistic constructed language,
# made by Sonja Lang (https://lang.sg/)

# Currently only takes input once run (no stdin),
# and only outputs in text, to stdout
# Also, doesn't implement Abigail's EOF marker or
# full stop conversion as of yet

# Coded in good faith that all input will be valid toki pona and nothing else
# Therefore, all errors or wrong output is due to wrong input
# (garbage in, garbage out), and the _user's_ problem (also see license)

# Conversion dictionary
conv_dict = {
    "X": "0", # Padding value, for words of odd length
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

# Put to lowercase
# Remove any leading/trailing whitespace
# Split into words
in_text = input("; ").casefold().strip().split()

# Pad words that need padding, with a character
# that won't be found in toki pona input
for word in in_text:
    if len(word) % 2:
        in_text[in_text.index(word)] += "X"

# Reassemble the text by reinserting spaces
in_text = " ".join(in_text)

# If the reassembled text is a char too short, fix that
if len(in_text) % 2:
    in_text += "X"

# List for output later
out_list = []

# List comprehension that takes pairs from the processe input string
for pair in [in_text[i:i+2] for i in range(0, len(in_text), 2)]:
    # Without checking (good faith),
    # get dict values of both chars in pair 
    out_pair = conv_dict[pair[0]] + conv_dict[pair[1]]

    # Filtering out any double padding
    if out_pair != "00":
        out_list.append(out_pair)

    # Assemble the pairs into a full string ready for output
    out_str = "".join(out_list)

    # Make sure the output is of even length
    # If odd length,
    if len(out_str) % 2:
        # and the string is padded,
        if out_str[-1] == "0":
            # unpad it
            out_str = out_str[:-1]
        # If not padded,
        else:
            # pad it
            out_str += "0"
    # Replace space FFs with 00s, to facilitate reading
    # as 00 gets blanked out in some debuggers
    out_str = out_str.replace("FF", "00")

# Output the finished string: (uncomment one or more prints)
# in rows, pair by pair
#print("\n".join([out_str[i:i+2] for i in range(0, len(out_str), 2)]))

# in one row, in pairs
print(" ".join([out_str[i:i+2] for i in range(0, len(out_str), 2)]))

# in one row, in full
#print(out_str)
