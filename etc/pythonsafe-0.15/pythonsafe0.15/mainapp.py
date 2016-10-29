#! /usr/bin/python

##    mainapp.py - Wx GUI for managing passwords
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
import wx
import sys, os
sys.path.append(os.path.join(os.getcwd(),'lib/'))

from lib.manager import PasswordManager
from lib.objectmodel import PasswordObject

dataFile = 'passwords.data'

class MainApp(wx.App):
    def OnInit(self):
        self.frame = MainWindow()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

class MainWindow(wx.Frame):
    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, size=(275,350), title='PythonSafe password manager'):
        wx.Frame.__init__(self,parent,id,title,pos,size)
        panel = wx.Panel(self,-1)

        self.manager = PasswordManager(dataFile)
        #menu
        menuFile = wx.Menu()
        menuFile.Append(1, "&Generator")
        menuFile.Append(2, "&About")
        menuFile.AppendSeparator()
        menuFile.Append(3, "E&xit")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile,"&File")
        self.SetMenuBar(menuBar)
        wx.StaticText(panel,-1,"Master Password: ", wx.Point(125,0))
        self.showButton =wx.Button(self, 10, "Load", wx.Point(10, 45), wx.Size(120,20))
        self.passwordListView = wx.ListView(self, 20, wx.Point(10,120), wx.Size(120,120))
        self.pwSelection=wx.ComboBox(self, 30, "", wx.Point(10, 80), wx.Size(120, -1), self.passwords, wx.CB_DROPDOWN)

        self.masterPassInput = wx.TextCtrl(panel, -1, "", wx.Point(125,20), wx.Size(120, -1), style = wx.TE_PASSWORD)
        self.showButton = wx.Button(panel, 10, "Load", wx.Point(125, 45), wx.Size(120, 20))
        self.saveButton = wx.Button(panel, 11, "Save", wx.Point(125, 220), wx.Size(60, 20))
        self.insertButton = wx.Button(panel, 12, "Insert", wx.Point(185, 220), wx.Size(60, 20))


        self.pwSelection = wx.ListBox(panel, 30, wx.Point(0, 0), wx.Size(120, 300))

        #modification controls
        self.SiteIdText = wx.TextCtrl(panel, 100, "", wx.Point(125, 70), wx.Size(120,-1))
        self.SiteUrlText = wx.TextCtrl(panel, 110, "", wx.Point(125, 95), wx.Size(120,-1))
        self.SiteUsernameText = wx.TextCtrl(panel, 120, "", wx.Point(125, 120), wx.Size(120,-1))
        self.SitePasswordText = wx.TextCtrl(panel, 130, "", wx.Point(125, 145), wx.Size(120,-1), style = wx.TE_PASSWORD)
        self.showPasswordButton = wx.Button(panel, 135, "...", wx.Point(245, 145), wx.Size(15, -1))
        self.SiteTagsText = wx.TextCtrl(panel, 140, "", wx.Point(125, 170), wx.Size(120,-1))
        self.SiteAdditionalText = wx.TextCtrl(panel, 150, "", wx.Point(125, 195), wx.Size(120,-1))
        
        self.Bind(wx.EVT_MENU, self.OnGenerate, id=1)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=2)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnLoadClick, id=10)
        self.Bind(wx.EVT_BUTTON, self.OnSaveClick, id=11)
        self.Bind(wx.EVT_BUTTON, self.OnInsertClick, id=12)
        self.Bind(wx.EVT_BUTTON, self.OnPasswordClick, id=135)
        self.Bind(wx.EVT_LISTBOX, self.ShowSelectedPassword, id=30)

    def PopulatePasswordsList(self):
        self.masterPass = self.masterPassInput.GetValue()
        self.manager.Load(self.masterPass)
        for pw in sorted(self.manager.Passwords.values()):
            self.pwSelection.Append(pw.GetTitle())


    def ShowSelectedPassword(self, event):
        self.selectedPasswd = self.manager.GetList(self.pwSelection.GetStringSelection())[0]
        self.SiteIdText.SetValue(self.selectedPasswd.SiteId)
        self.SiteUrlText.SetValue(str(self.selectedPasswd.SiteUrl))
        self.SiteUsernameText.SetValue(str(self.selectedPasswd.UserName))
        self.SitePasswordText.SetValue(str(self.selectedPasswd.Password))
        self.SiteTagsText.SetValue(str(self.selectedPasswd.Tags))
        self.SiteAdditionalText.SetValue(str(self.selectedPasswd.Additional))

    def OnLoadClick(self, event):
        self.PopulatePasswordsList()

    def OnSaveClick(self, event):
        self.selectedPasswd.SiteId = self.SiteIdText.GetValue()
        self.selectedPasswd.SiteUrl = self.SiteUrlText.GetValue()
        self.selectedPasswd.UserName = self.SiteUsernameText.GetValue()
        self.selectedPasswd.Password = self.SitePasswordText.GetValue()
        self.manager.Passwords[self.selectedPasswd.Guid] = self.selectedPasswd
        self.manager.Save(self.masterPass)

    def OnInsertClick(self, event):
        newpassword = PasswordObject()
        newpassword.SiteId = self.SiteIdText.GetValue()
        newpassword.SiteUrl = self.SiteUrlText.GetValue()
        newpassword.UserName = self.SiteUsernameText.GetValue()
        newpassword.Password = self.SitePasswordText.GetValue()
        self.manager.Passwords[newpassword.Guid] = newpassword
        self.manager.Save(self.masterPass)

    def OnPasswordClick(self, event):
        pw = self.SitePasswordText.GetValue()
        if wx.TheClipboard.Open():
            wx.TheClipboard.Clear()
            wx.TheClipboard.SetData(wx.TextDataObject(pw))
            wx.TheClipboard.Close()
        wx.MessageBox("The password (%s) has been copied to the clipboard" % (pw, ))

    def OnGenerate(self, event):
        wx.MessageBox("Not integrated yet, please run generator.py")

    def OnAbout(self, event):
        wx.MessageBox("PythonSafe Alpha v0.15")

    def OnQuit(self, event):
        self.Close()

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()
