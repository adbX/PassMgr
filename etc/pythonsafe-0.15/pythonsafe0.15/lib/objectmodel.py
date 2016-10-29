#! /usr/bin/python

##    objectmodel.py - Backend objects
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
import time, uuid

class PasswordObject(object):
    ''' 
    Data structure for an individual password entry 
    '''

    def __init__(self, id="",siteurl="",username="",email="",passwd="",extras=None, guid=uuid.uuid1()):
        self.Guid = guid
        self.SiteId = id.strip().encode()
        self.SiteUrl = siteurl.strip().encode()
        self.UserName = username.strip().encode()
        self.EmailAddress = email.strip().encode()
        self.Password = passwd.strip().encode()
        self.PasswordList = []
        self.LastUpdated = time.strftime("%d/%m/%y", time.localtime())
        self.Tags = []
        if extras is None:
            self.Additional = {}
        else:
            self.Additional = extras

    def GetTitle(self):
        if self.SiteId is None: return
        if self.UserName is None: self.UserName = ""
        if self.UserName != "":
            key = self.SiteId + "/" + self.UserName
        else:
            key = self.SiteId + "/Default"
        return key 

    def ChangePassword(self,passwd):
        self.PasswordList.append(self.Password)
        self.Password = passwd
        self.LastUpdated = time.strftime("%d/%m/%y", time.localtime())
  
    def __str__(self):
        string = "Password for " + self.SiteId
        string += " - Username: %s\n" % self.UserName
        string += " - Password: %s\n" % self.Password
        string += " - Site Url: %s\n" % self.SiteUrl
        string += " - Tagged under: %s\n" % self.Tags
        string += " - Additional info: %s\n" % self.Additional
        return string

    def __cmp__(self, other):
        return cmp(self.GetTitle().lower(), other.GetTitle().lower())

    def __eq__(self, other):
        return self.GetTitle().lower() == other.GetTitle().lower()

    def PrintCSVHeader(self):
        return "Site Id,URL,Username,Password,Email,LastChanged,Tags,PreviousPasswords,Additional" 

    def AsCSV(self):
        return "%s,%s,%s,%s,%s,%s,%s\n" % (self.SiteId,self.SiteUrl,self.UserName,self.Password,self.LastUpdated,self.Tags,self.Additional)


if __name__ == '__main__':
    a = PasswordObject('aaa','bbb','ccc')
    b = PasswordObject('kkk','lll','mmm')
    c = PasswordObject('xxx','yyy','zzz')
    newList = [c,a,b]
    print sorted(newList)[0]

