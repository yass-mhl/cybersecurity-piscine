import hmac
import hashlib
import time
import sys
import argparse
import os

# Comment créer un nouveau jeton OTP
# Il faut entrer une clef secrète de 64 caractères hexadécimaux et un compteur (timestampp en l'occurence)
# Le compteur est divisé par 30 pour obtenir une nouvelle valeur toutes les 30 secondes
# Ensuite, on recupere les 4 derniers bits du hash HMAC-SHA1 de la clef secrète et du compteur
# On utilise ces 4 bits pour déterminer un offset dans le hash
# On extrait 4 bytes à partir de l'offset et on les convertit en entier
# On retire le bit le plus significatif pour obtenir un entier de 31 bits
# On retourne le modulo de cet entier par 1,000,000 pour obtenir un code à 6 chiffres

def generate_otp(key, counter):
    hmac_result = hmac.new(key, counter.to_bytes(8, byteorder='big'), hashlib.sha1).digest() # Create a HMAC-SHA1 hash of the counter using the key as the secret
    offset = hmac_result[-1] & 0x0F # Use the last 4 bits of the hash to determine the offset
    binary = hmac_result[offset:offset+4] # Extract 4 bytes from the hash starting at the offset
    otp = int.from_bytes(binary, byteorder='big') & 0x7FFFFFFF # Convert the 4 bytes to an integer and remove the most significant bit
    return otp % 1000000 # Return the integer modulo 1,000,000 to get a 6-digit code

def save_key(key):
    with open("ft_otp.key", "wb") as key_file:
        key_file.write(key)

def load_key(file_name):
    if not os.path.isfile(file_name):
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)
    with open(file_name, "rb") as key_file:
        return key_file.read()


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--generate", help="Generate a new key and save it to ft_otp.key")
    group.add_argument("-k", "--key", help="Generate a new one-time password using the key provided or load a key from a file")
    args = parser.parse_args()

    if args.generate:
        if os.path.isfile(args.generate):
            with open(args.generate, "r") as file:
                key = bytes.fromhex(file.read().strip())
        elif len(args.generate) == 64:
            key = bytes.fromhex(args.generate)
        else:
            print("Error: key must be 64 hexadecimal characters.")
            sys.exit(1)
        
        save_key(key)
        print("Key was successfully saved in ft_otp.key.")
    elif args.key:
        if os.path.isfile(args.key):
            key = load_key(args.key)
        elif len(args.key) == 64:
            key = bytes.fromhex(args.key)
        else:
            print("Error: key must be 64 hexadecimal characters or a file.")
            sys.exit(1)
        
        counter = int(time.time() // 30)
        otp = generate_otp(key, counter)
        print("{:06d}".format(otp))


if __name__ == "__main__":
    main()
