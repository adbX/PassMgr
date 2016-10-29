#! /usr/bin/python

##    generator.py - Wx GUI for generating passwords
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
import sys
sys.path.append("c:\\dev\\py\\pythonsafe")
from lib.generator import PasswordGenerator, GeneratorOptions

class GeneratorDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        self.Options = GeneratorOptions()
        self.PWGenerator = PasswordGenerator(self.Options)
        wx.Dialog.__init__(self, parent, id, title, size=(250, 230))

        wx.StaticBox(self, -1, 'Password Options', (5, 5), size=(240, 170))
        self.UpperCaseCheckControl = wx.CheckBox(self, -1 ,'Include Uppercase', (15, 30))
        self.NumbersCheckControl = wx.CheckBox(self, -1 ,'Include Numbers', (15, 55))
        self.SymbolsCheckControl = wx.CheckBox(self, -1 ,'Include Symbols', (15, 80))
        wx.StaticText(self, -1, 'Length', (15, 105))
        self.LengthSpinControl = wx.SpinCtrl(self, -1, '1', (65, 105), (60, -1), min=3, max=40)
        wx.Button(self, 1, 'Generate', (5, 185), (60, -1))
        wx.Button(self, 2, 'Close', (90, 185), (60, -1))

        self.Bind(wx.EVT_BUTTON, self.OnGenerate, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=2)

        self.Centre()
        self.ShowModal()
        self.Destroy()

    def UpdateOptions(self,event):
        self.Options.MustHaveUpper = self.UpperCaseCheckControl.GetValue()
        self.Options.MustHaveNumbers = self.NumbersCheckControl.GetValue()
        self.Options.MustHaveSymbols = self.SymbolsCheckControl.GetValue()
        self.Options.PasswordLength = self.LengthSpinControl.GetValue()
        self.Options.OmitSimilarCharacters = False
        self.PWGenerator.options = self.Options


    def OnGenerate(self,event):
        self.UpdateOptions(event)
        wx.MessageBox(self.PWGenerator.MakePassword())

    def OnClose(self, event):
        self.Close()

app = wx.App(0)
GeneratorDialog(None, -1, 'generator.py')
app.MainLoop()

