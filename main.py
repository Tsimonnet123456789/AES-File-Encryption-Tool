# ChatGPT assisted in the creation of the project
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

if __name__ == '__main__':
    begin = 0

    while True:
        if begin > 0:
            end = input("Type 'exit' to leave or press Enter to continue: ").strip().lower()
            if end == "exit":
                break

        begin += 1
        print("This tool provies AES encryption at rest")
        w5 = 0
        while (w5 != 1):
            print("Do you wish to encrypt or decrypt\na:encrypt\nb:decrypt")
            st = (input("enter the letter for the encryption you want to use"))
            if (st == "a" or st == "b"):
                w5 = 1
            else:
                print("That is not a valid option")


        w =0
        while(w != 1):
            print("Pick a level of encryption\na:128\nb:192\nc:256")
            en = (input("enter the letter for the encryption you want to use"))
            if(en == "a"or en == "b" or en == "c"):
                w =1
            else:
                print("That is not a valid option")

        w1 = 0
        while (w1 != 1):
            print("Do you wish to use a file or folder?\na:file\nb:folder")

            fl = (input("enter the letter for the document type"))
            if (fl == "a" or fl == "b"):
                w1 = 1
            else:
                print("That is not a valid option")
        w2 = 0
        while (w2 != 1):
            print("Do you wish to use cryptographic keys or password generated keys?\na:cryptographic key\nb:password generated keys")
            key = (input("enter the letter for the key"))
            if (key == "a" or key == "b"):
                w2 = 1
            else:
                print("That is not a valid option")
        if (key == "a" and st == "a"):
            w6 = 0
            while (w6 != 1):
                print("You have chosen cryptographic key do you want\na:the program to generate\nb: provide it in hexadecimal")
                key2 = (input("enter the letter for the key"))
                if (key2 == "a" or key2 == "b"):
                    w6 = 1
                else:
                    print("That is not a valid option")


        # encode for a password
        if (key == "b" and st == "a"):


            files_encrypted = 0
            password = input("Enter the password: ")

            # set key size
            if en == "a":
                key_size = 16
            elif en == "b":
                key_size = 24
            else:
                key_size = 32


            def encrypt_file(filepath):
                global files_encrypted

                if not os.path.isfile(filepath):
                    print("File not found:", filepath)
                    return False

                salt = get_random_bytes(16)
                aes_key = PBKDF2(password, salt, dkLen=key_size, count=100000, hmac_hash_module=SHA256)

                with open(filepath, "rb") as file:
                    data = file.read()

                cipher = AES.new(aes_key, AES.MODE_GCM)
                ciphertext, tag = cipher.encrypt_and_digest(data)

                out_file = filepath + ".enc"

                with open(out_file, "wb") as file:
                    file.write(salt)  # 16 bytes
                    file.write(cipher.nonce)  # 16 bytes
                    file.write(tag)  # 16 bytes
                    file.write(ciphertext)

                print("Encrypted:", filepath)
                print("Saved as:", out_file)

                files_encrypted += 1
                return True


            # FILE
            if fl == "a":
                filepath = input("Enter file path: ").strip()
                encrypt_file(filepath)

            # FOLDER
            elif fl == "b":
                folderpath = input("Enter folder path: ").strip()

                if not os.path.isdir(folderpath):
                    print("Folder not found:", folderpath)
                else:
                    for root, dirs, files in os.walk(folderpath):
                        for name in files:
                            full_path = os.path.join(root, name)

                            if not full_path.endswith(".enc"):
                                encrypt_file(full_path)

            if files_encrypted > 0:
                print("Encryption complete.")
            else:
                print("No files were encrypted.")






        if (key == "a"and st == "a"):


            # set key size based on AES level
            if en == "a":
                key_size = 16
            elif en == "b":
                key_size = 24
            else:
                key_size = 32

            if key2 == "a":
                aes_key = get_random_bytes(key_size)
                print("Generated key (SAVE THIS):", aes_key.hex())

            elif key2 == "b":
                hex_key = input("Enter hex key: ").strip()

                try:
                    aes_key = bytes.fromhex(hex_key)
                except:
                    print("Invalid hex key")
                    exit()

                if len(aes_key) != key_size:
                    print("Invalid key length")
                    exit()

            else:
                print("Invalid option")
                exit()

            files_encrypted = 0


            def encrypt_file(filepath):
                if not os.path.isfile(filepath):
                    print("File not found:", filepath)
                    return False

                iv = get_random_bytes(16)

                with open(filepath, "rb") as file:
                    data = file.read()

                cipher = AES.new(aes_key, AES.MODE_CBC, iv)
                encrypted_data = cipher.encrypt(pad(data, AES.block_size))

                out_file = filepath + ".enc"

                with open(out_file, "wb") as file:
                    file.write(iv)
                    file.write(encrypted_data)

                print("Encrypted:", filepath)
                print("Saved as:", out_file)
                return True

            # file or folder
            if fl == "a":
                filepath = input("Enter file path: ").strip()

                if encrypt_file(filepath):
                    files_encrypted += 1

            elif fl == "b":
                folderpath = input("Enter folder path: ").strip()

                if not os.path.isdir(folderpath):
                    print("Folder not found:", folderpath)
                else:
                    for root, dirs, files in os.walk(folderpath):
                        for name in files:
                            full_path = os.path.join(root, name)

                            if not full_path.endswith(".enc"):
                                if encrypt_file(full_path):
                                    files_encrypted += 1

            if files_encrypted > 0:
                print("Encryption complete.")
            else:
                print("No files were encrypted.")



        # decode for password
        if (key == "b" and st == "b"):


            files_decrypted = 0
            password = input("Enter the password: ")

            # set key size
            if en == "a":
                key_size = 16
            elif en == "b":
                key_size = 24
            else:
                key_size = 32


            def decrypt_file(filepath):
                global files_decrypted

                if not os.path.isfile(filepath):
                    print("File not found:", filepath)
                    return False

                try:
                    with open(filepath, "rb") as file:
                        salt = file.read(16)  # must match encrypt
                        nonce = file.read(16)
                        tag = file.read(16)
                        ciphertext = file.read()

                    aes_key = PBKDF2(password, salt, dkLen=key_size, count=100000, hmac_hash_module=SHA256)

                    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
                    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

                    output_file = os.path.splitext(filepath)[0] + ".dec"

                    with open(output_file, "wb") as file:
                        file.write(decrypted_data)

                    print("Decrypted:", filepath)
                    print("Saved as:", output_file)

                    files_decrypted += 1
                    return True

                except:
                    print("Decryption failed (wrong password or file modified):", filepath)
                    return False


            # FILE
            if fl == "a":
                filepath = input("Enter encrypted file path: ").strip()
                decrypt_file(filepath)

            # FOLDER
            elif fl == "b":
                folderpath = input("Enter folder path: ").strip()

                if not os.path.isdir(folderpath):
                    print("Folder not found:", folderpath)
                else:
                    for root, dirs, files in os.walk(folderpath):
                        for name in files:
                            full_path = os.path.join(root, name)

                            if full_path.endswith(".enc"):
                                decrypt_file(full_path)

            if files_decrypted > 0:
                print("Decryption complete.")
            else:
                print("No files were decrypted.")

        if (key == "a" and st == "b"):


            # set key size based on AES level
            if en == "a":
                key_size = 16
            elif en == "b":
                key_size = 24
            else:
                key_size = 32

            hex_key = input("Enter hex key: ").strip()

            try:
                aes_key = bytes.fromhex(hex_key)
            except:
                print("Invalid hex key")
                exit()

            if len(aes_key) != key_size:
                print("Invalid key length")
                exit()

            files_decrypted = 0


            def decrypt_file(filepath):
                global files_decrypted

                if not os.path.isfile(filepath):
                    print("File not found:", filepath)
                    return

                try:
                    with open(filepath, "rb") as file:
                        iv = file.read(16)
                        encrypted_data = file.read()

                    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
                    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

                    output_file = os.path.splitext(filepath)[0] + ".dec"

                    with open(output_file, "wb") as file:
                        file.write(decrypted_data)

                    print("Decrypted:", filepath)
                    print("Saved as:", output_file)
                    files_decrypted += 1

                except:
                    print("Decryption failed:", filepath)


            if fl == "a":
                filepath = input("Enter encrypted file path: ").strip()
                decrypt_file(filepath)

            elif fl == "b":
                folderpath = input("Enter folder path: ").strip()

                if not os.path.isdir(folderpath):
                    print("Folder not found:", folderpath)
                else:
                    for root, dirs, files in os.walk(folderpath):
                        for name in files:
                            full_path = os.path.join(root, name)

                            if full_path.endswith(".enc"):
                                decrypt_file(full_path)

            if files_decrypted > 0:
                print("Decryption complete.")
            else:
                print("No files were decrypted.")