from hashlib import sha256

ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')

def hex(salt, plaintext):
    return sha256(salt + plaintext).hexdigest()

SECRET_KEY = 's3cr3t'

def make_password(plaintext, service):
    salt = hex(SECRET_KEY, service)[:20]
    hsh = hex(salt, plaintext)
    return ''.join((salt, hsh))

def password(plaintext, service, length=10, alpha=ALPHABET):
    raw_hex = make_password(plaintext, service)

    # Convert the hexdigest into decimal
    num = int(raw_hex, 16)

    # What base will we convert `num` into?
    num_chars = len(alpha)

    # Build up the new password one "digit" at a time,
    # up to a certain length
    chars = []
    while len(chars) < length:
        num, index = divmod(num, num_chars)
        chars.append(alpha[index])

    print ''.join(chars)

master_pass = raw_input("Enter your master password: ")
service = raw_input("Enter the service/website: ")
password(master_pass, service)