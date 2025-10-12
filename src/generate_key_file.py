from encryption import generate_key

key = generate_key()
with open("key.key", "wb") as key_file:
    key_file.write(key)

print("Encryption key generated and saved to key.key")
print("Keep this file safe! Without it, you cannot decrypt passwords.")
