from hashlib import sha256


def generate():
    alphabet = ('abcdefghijklmnopqrstuvwxyz'
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                '0123456789!@#$%^&*()-_')

    my_key = 'm@st3RP@$$w0rd'


    def create_hex(salt, plaintext):
        return sha256(salt + plaintext).hexdigest()


    def make_password(plaintext, service):
        salt = create_hex(my_key, service)[:20]
        hsh = create_hex(salt, plaintext)
        return ''.join((salt, hsh))


    def password(plaintext, service, length=10, alpha=alphabet):
        raw_hex = make_password(plaintext, service)

        # Convert the hex to dec
        num = int(raw_hex, 16)

        num_chars = len(alpha)

        chars = []
        while len(chars) < length:
            num, index = divmod(num, num_chars)
            chars.append(alpha[index])

        print ''.join(chars)

    master_pass = raw_input("Enter your master password: ")
    service = raw_input("Enter the service/website: ")
    password(master_pass, service)
generate()