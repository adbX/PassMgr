#! /usr/bin/python

##    pconsole.py - Console interface
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

# Module imports
import sys, getpass
from lib.manager import PasswordManager
from lib.objectmodel import PasswordObject
from lib.generator import PasswordGenerator, GeneratorOptions
import generatewordpasswords

class Console(object):
    def __init__(self,filenm):
        self.key = getpass.getpass('Enter/Choose master password: ')
        self.manager = PasswordManager(filenm)
        self.manager.Load(self.key)

    def Menu(self):
        print self.Usage()
        choice = raw_input()
        if choice == '1':
            chosen = self.ShowPasswords()
            if not type(chosen) == str:
                print str(chosen)
            else:
                print "No passwords found" 
        elif choice == '2':
            self.AddModifyScreen(PasswordObject())
        elif choice == '3':
            chosen = self.ShowPasswords()
            self.AddModifyScreen(chosen)
        elif choice == '4':
            chosen = self.ShowPasswords()
            self.ChangePassword(chosen)
        elif choice == '5':
            chosen = self.ShowPasswords()
            if self.VerifyChoice():
                self.manager.DeleteEntry(chosen)
                print 'Deleted password %s' % chosen
        elif choice == '6':
            print self.CreateRandom()
        elif choice == '7':
            print self.CreateMemorable()
        elif choice == '8':
            self.manager.Export(self.key)
        elif choice == '9':
            self.ChangeMaster()
        elif choice == '0':
            self.manager.Save(self.key)
            print "Saved passwords to file"
            sys.exit()
        elif choice == 'Q':
            if self.VerifyChoice():
                sys.exit()

    def VerifyChoice(self):
        return raw_input('Are you sure? (y)es or (n)o: ') == 'y'

    def CreateRandom(self, length = 0):
        opt = GeneratorOptions()
        if length == 0: #prompt
            chosenLength = raw_input("Enter length (default 8): ")
        if length == 0 and chosenLength:
            opt.PasswordLength = int(chosenLength)
        else:
            opt.PasswordLength = 8
        opt.MustHaveUpper = True
        opt.MustHaveNumbers = True
        opt.OmitSimilarCharacters = True
        opt.MustHaveSymbols = True
        gen = PasswordGenerator(opt)
        return gen.MakePassword()

    def CreateMemorable(self):
        return generatewordpasswords.Generate()

    def GetInput(self, prompt, existing=''):
        if type(existing) is str and len(existing) > 0:
            print prompt + " (press enter to accept default - '%s')" % existing
        else: 
            print prompt
        input = raw_input()
        if input == '': return existing
        return input

    def GetPassword(self):
        input1 = 'a'
        input2 = 'b'
        while input1 != input2:
            if len(input1) > 2:
                print "Passwords don't match"
            else:
                print "Password Examples: %s %s %s" % (self.CreateMemorable(), self.CreateMemorable(), self.CreateRandom(8))
            input1 = getpass.getpass('Password: ')
            input2 = getpass.getpass('Repeat  : ')
        return input1
  
    def AddModifyScreen(self, pw):
        pw.SiteId = self.GetInput("Title: ",pw.SiteId )
        pw.SiteUrl = self.GetInput("Url: ",pw.SiteUrl )
        pw.UserName = self.GetInput("Username: ",pw.UserName )
        pw.EmailAddress = self.GetInput("Email Address: ",pw.EmailAddress )
        pw.Password = self.GetPassword()
        while 1:
            tag = raw_input("Tag/Categorise this password entry (leave blank to skip): ")
            if not tag: break
            pw.Tags.append(tag)
        while 1:
            key = raw_input("Enter additional data key (leave blank to skip): ")
            if not key: break
            value = raw_input("Enter value for " + key + ": ")
            pw.Additional[key] = value
        self.manager.AddEntry(pw)
        pw = None

    def ShowPasswords(self):
        searchTerm = self.GetInput("Search Term (blank to show all): ")
        pwList = self.manager.GetList(searchTerm)
        for i in range(len(pwList)):
            print i, ') ', pwList[i].GetTitle()
        if len(pwList) == 0:
            return "No passwords in database"
        elif len(pwList) == 1:
            return pwList[0]
        else:
            choice = raw_input('Which password? ')
            if not choice:
                return ''
            chosen = pwList[int(choice)]
            return chosen

    def ChangePassword(self, pw):
        newPass = self.GetPassword()
        pw.ChangePassword(newPass)
        self.manager.Update(pw)

    def ChangeMaster(self):
        oldkey = self.key
        print "Please enter a new master key:"
        newkey = self.GetPassword()
        self.key = newkey
        print "Done! You must save and exit to apply this change!"
    
    def Usage(self):
        return '''
            1) Get password
            2) Add a record
            3) Modify a record
            4) Change a password
            5) Delete a record
            6) Generate a random password
            7) Generate a memorable password
            8) Export
            9) Change master password
            0) Save and Exit
            Q) Exit without saving
        '''
