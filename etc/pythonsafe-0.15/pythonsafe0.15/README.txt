PythonSafe Password Manager

PythonSafe is run under the Python interpreter.  You can extract the files using:

tar -zxvf pythonsafe[version].tar.gz (on unix-based systems)
or an equivalent windows zip file manager (try 7zip)

Once the files have been extracted, type the following command to run pythonsafe:

python main.py (for console mode)
python mainapp.py (for gui mode - requires python 2.5)

You will be immediately asked to enter or choose a master password.  This is the
password that will be used to encrypt your password database.  Don't forget it,
if you lose it you will irrevocably lose all access to your saved passwords.

Once you have chosen a password you will be presented with the menu screen.  From
here you can add or retrieve passwords.  Don't forget to hit save before you exit.

Your passwords are saved in an encrypted file called 'passwords.data'.


