#! /usr/bin/python

##    pmgr.py - Backend manager class
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
import sys, pickle
from search import Search
from objectmodel import PasswordObject
from storage import SecureFileStore

class PasswordManager(object):
    ''' 
    allow adding, removing, saving, loading of passwords and getting by site
    '''
  
    def __init__(self,filenm):
        self.FileStore = SecureFileStore(filenm)
        self.Passwords = {}

    def Load(self,key):
        self.__Deserialise(self.FileStore.Decrypt(key))
  
    def Save(self,key):
        self.FileStore.Encrypt(self.__Serialise(),key)
 
    def AddEntry(self,p):
        self.Passwords[p.Guid] = p

    def DeleteEntry(self,p):
        del self.Passwords[p.Guid]

    def UpdateEntry(self,p):
        self.Passwords[p.Guid] = p

    def GetList(self, searchTerm='', sorted=True):
        returnList = []
        if searchTerm:
            searcher = Search(self.Passwords.values())
            returnList = searcher.DoSearch(searchTerm)
        else:
            returnList = self.Passwords.values()
        if sorted: returnList.sort()
        return returnList

    def Export(self):
        string = ''
        for p in self.GetList():
            string += p.AsCSV()
        return string

    def __Serialise(self):
        return pickle.dumps(self.Passwords)
  
    def __Deserialise(self,string):
        try:
            self.Passwords = pickle.loads(string)
        except:
            print 'unable to deserialise string: ', sys.exc_info()[0]
            self.Passwords = {}
        return self.Passwords     

if __name__ == '__main__':
    p1 = PasswordManager('test.dat')
    p1.AddEntry(PasswordObject('test'))
    p1.Save('key')
    p1 = None
    p2 = PasswordManager('test.dat')
    p2.Load('key')
    print p2.GetList('test')[0]
