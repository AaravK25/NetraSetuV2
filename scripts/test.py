file_name = "my_document.txt"
text_to_write = "This is the first line.\nThis is the second line."

with open(file_name, 'w') as file:
    file.write(text_to_write)

print(f"Text written to '{file_name}' (overwriting if it existed).")