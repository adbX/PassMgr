#! /usr/bin/python

##    search.py - Allow searching for objects
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
from objectmodel import PasswordObject

class Search(object):
    def __init__(self, collection=[]):
        self.Passwords = collection

    """
    Allow searching on
    SiteId,SiteUrl, UserName, EmailAddress, Password, PasswordList, Tags, Additional
    """
    def DoSearch(self,searchTerm=''):
        searchTerm = searchTerm.lower().strip().encode()
        if searchTerm == '':
            return self.Passwords
        returnedList = {}
        for pw in self.Passwords:
            if pw.Guid == searchTerm or pw.GetTitle() == searchTerm:
                return [pw,]
            elif searchTerm in pw.SiteId.lower() or pw.SiteId.lower() in searchTerm:
                returnedList[pw.Guid] = pw
            elif pw.SiteUrl and searchTerm in pw.SiteUrl.lower():
                returnedList[pw.Guid] = pw
            elif pw.UserName and searchTerm in pw.UserName.lower():
                returnedList[pw.Guid] = pw
            elif pw.EmailAddress and searchTerm in pw.EmailAddress.lower():
                returnedList[pw.Guid] = pw
            elif pw.Password and searchTerm in pw.Password.lower():
                returnedList[pw.Guid] = pw
            elif pw.PasswordList: 
                for listitem in pw.PasswordList:
                    if searchTerm in listitem.lower():
                        returnedList[pw.Guid] = pw
            elif pw.Tags: 
                for tag in pw.Tags:
                    if searchTerm in tag.lower():
                        returnedList[pw.Guid] = pw
            elif pw.Additional: 
                for adKey,adValue in pw.Additional.iteritems():
                    if adKey and adValue:
                        if searchTerm in adKey.lower() or searchTerm in adValue.lower():
                            returnedList[pw.Guid] = pw
        return returnedList.values()


if __name__ == '__main__':
    lst = []
    lst.append(PasswordObject('bob','www.test.com','bob@bob.com'))
    s = Search(lst)
    for pw in s.DoSearch('bob/bob@bob.com'):
        print str(pw)



