fl = "b"
key = "b"
en ="a"
if (key == "b"):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    import os

    password = input("Enter the password: ")

    # set key size based on AES level
    if en == "a":
        key_size = 16
    elif en == "b":
        key_size = 24
    else:
        key_size = 32

    aes_key = password.encode().ljust(key_size, b'\0')[:key_size]

    def decrypt_file(filepath):
        with open(filepath, "rb") as file:
            iv = file.read(16)
            encrypted_data = file.read()

        cipher = AES.new(aes_key, AES.MODE_CBC, iv)

        try:
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        except:
            print("Failed:", filepath)
            return

        # output file ends with .dec
        if filepath.endswith(".enc"):
            output_file = filepath[:-4] + ".dec"
        else:
            output_file = filepath + ".dec"

        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        print("Decrypted:", filepath)

    # --- FILE ---
    if fl == "a":
        filepath = input("Enter the encrypted file path: ")
        decrypt_file(filepath)

    # --- FOLDER ---
    elif fl == "b":
        folderpath = input("Enter the folder path: ")

        for root, dirs, files in os.walk(folderpath):
            for name in files:
                full_path = os.path.join(root, name)

                # only decrypt .enc files
                if full_path.endswith(".enc"):
                    decrypt_file(full_path)

    print("Decryption complete.")









# if (fl == "a" and key == "b"):
#     from Crypto.Cipher import AES
#     from Crypto.Util.Padding import unpad
#
#     filepath = input("Enter the encrypted file path: ")
#     password = input("Enter the password: ")
#
#     # set key size based on AES level
#     if en == "a":
#         key_size = 16
#     elif en == "b":
#         key_size = 24
#     else:
#         key_size = 32
#
#     aes_key = password.encode().ljust(key_size, b'\0')[:key_size]
#
#     with open(filepath, "rb") as file:
#         iv = file.read(16)              # get IV from file
#         encrypted_data = file.read()   # rest is ciphertext
#
#     cipher = AES.new(aes_key, AES.MODE_CBC, iv)
#
#     try:
#         decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
#     except:
#         print("Decryption failed (wrong password or wrong AES level)")
#         exit()
#
#     # output file
#     if filepath.endswith(".enc"):
#         output_file = filepath[:-4] + ".dec"
#     else:
#         output_file = filepath + ".dec"
#
#     with open(output_file, "wb") as file:
#         file.write(decrypted_data)
#
#     print("File decrypted successfully.")
#     print("Saved as:", output_file)