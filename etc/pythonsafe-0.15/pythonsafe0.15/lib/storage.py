#! /usr/bin/python

##    storage.py - Backend file storage class
##    This file is part of PythonSafe.
##
##    PythonSafe is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    PythonSafe is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with PythonSafe.  If not, see <http://www.gnu.org/licenses/>.
##
##    PythonSafe is Copyright Richard Beales 2009-2010
##    PythonSafe's website can be found at http://pythonsafe.sourceforge.net/
##    The author's website can be found at http://www.richbeales.net/


# Password Safe and generator - use a master password phrase to get to all passwords
# which are stored in an encrypted file.

# Module imports
import os, sys, time
#from Crypto.Cipher import Blowfish # From the python-crypto package
from rijndael import rijndael

class SecureFileStore(object):
  ''' Class to persist to file and encrypt at the same time '''
  def __init__(self,fname):
    self.filename = fname
  
  def Encrypt(self,fstream,key):
    if len(key) > 32: raise ValueError('Key too long')
    key = key.ljust(32)
    f = open(self.filename,'wb')
    padding = len(fstream) % 32
    fstream += " " * (32-padding)
    obj = rijndael(key, block_size = 32)
    string = ''
    for i in range(len(fstream)/32):
      string += obj.encrypt(fstream[i*32:i*32+32]) 
    fstream = string
    f.write(fstream)
    f.close()

  def Decrypt(self,key):
    if len(key) > 32: raise ValueError('Key too long')
    key = key.ljust(32)
    try:
      f = open(self.filename,'rb')
      fstream = f.read()
      f.close()
      obj = rijndael(key, block_size = 32)
      string = ''
      for i in range(len(fstream)/32):
        string += obj.decrypt(fstream[i*32:i*32+32]) 
      return string
    except:
      print 'unable to read file: ', sys.exc_info()[0]
      return ''
  
if __name__ == '__main__':
    s = SecureFileStore('test.txt')
    s.Encrypt('blah blah blah','key')
    print s.Decrypt('key')

