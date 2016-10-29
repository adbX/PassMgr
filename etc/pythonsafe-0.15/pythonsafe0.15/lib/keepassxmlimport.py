#! /usr/bin/python

##    keepassxmlimport.py - Allows importing of KeePass 2.0 XML
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
import xml, os, sys, getpass
from xml.dom.minidom import parse
from objectmodel import PasswordObject
from manager import PasswordManager

plist = {}

def Import(fromfile=''):
    xmlfile = open(fromfile,'r')
    dom1 = parse(xmlfile)
    entries = dom1.getElementsByTagName("Entry")
    for entry in entries:
        HandleEntry(entry)
    xmlfile.close()

def GetGroupNameForTag(node):
    if node.parentNode:
      if node.parentNode.tagName == 'Group':
          if node.parentNode.getElementsByTagName("Name")[0].firstChild:
              return node.parentNode.getElementsByTagName("Name")[0].firstChild.nodeValue

def IsHistory(node):
    if node.parentNode.tagName == "History" or node.parentNode.parentNode.tagName == "History":
        return True
    else:
        return False

def HandleEntry(entry):
    if IsHistory(entry): return
    p = PasswordObject()
    p.Guid = entry.getElementsByTagName('UUID')[0].firstChild.nodeValue
    for stringTag in entry.getElementsByTagName("String"):
        if IsHistory(stringTag): break
        key =  stringTag.getElementsByTagName("Key")[0].firstChild.nodeValue
        value = stringTag.getElementsByTagName("Value")[0].firstChild
        if value: value = value.nodeValue.encode('iso-8859-1')
        #print key, ' = ', value
        if key == 'Title':
            p.SiteId = value
        elif key == 'URL':
            p.SiteUrl = value
        elif key == 'UserName':
            p.UserName = value
        elif key == 'Password':
            p.ChangePassword(value)
        else:
            p.Additional[key] = value

    p.Tags.append(GetGroupNameForTag(entry))
    #print p
    plist[p.Guid] = p
    p = None


if __name__ == '__main__':
    Import(raw_input('What is the filename of the keepass 2.0 xml file?: '))
    datafile = raw_input("Where should I save the new data file? (usually passwords.data): ")
    masterPass = getpass.getpass("Pick a master key for this new data file: ")
    pman = PasswordManager(datafile)
    pman.Passwords = plist
    pman.Save(masterPass)
    print "done"
