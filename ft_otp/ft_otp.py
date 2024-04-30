import hmac
import hashlib
import time
import sys
import argparse
import os

def generate_otp(key, counter):
    hmac_result = hmac.new(key, counter.to_bytes(8, byteorder='big'), hashlib.sha1).digest()
    offset = hmac_result[-1] & 0x0F
    binary = hmac_result[offset:offset+4]
    return int.from_bytes(binary, byteorder='big') & 0x7FFFFFFF

def save_key(key):
    with open("ft_otp.key", "wb") as key_file:
        key_file.write(key)

def load_key(file_name):
    with open(file_name, "rb") as key_file:
        return key_file.read()

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--generate", help="Generate a new key and save it to ft_otp.key")
    group.add_argument("-k", "--key", help="Generate a new one-time password using the key provided")
    args = parser.parse_args()

    if args.generate:
        if len(args.generate) != 64:
            print("Error: key must be 64 hexadecimal characters.")
            sys.exit(1)
        key = bytes.fromhex(args.generate)
        save_key(key)
        print("Key was successfully saved in ft_otp.key.")
    elif args.key:
        key = load_key(args.key)
        counter = int(time.time() // 30)  # Divisé par 30 pour obtenir une nouvelle valeur toutes les 30 secondes
        otp = generate_otp(key, counter)
        print("{:06d}".format(otp))

if __name__ == "__main__":
    main()
