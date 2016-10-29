#! /usr/bin/python

##    generator.py - Password Generator class
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
import random

class GeneratorOptions(object):
  """
    A class to keep a list of options for password generation
  """

  MustHaveUpper = False
  MustHaveNumbers = False
  MustHaveSymbols = False
  PasswordLength = 8
  OmitSimilarCharacters = False


class PasswordGenerator(object):
  """
    Password Generator with configurable options
  """
  UPPERCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  LOWERCHARS = "abcdefghijklmnopqrstuvwxyz"
  NUMBERS = "0123456789"
  SYMBOLS = "~!@#$%^&*()_-+={}|[]:;<>?."

  def __init__(self, pwOptions, customcharset=''):
    self.options = pwOptions
    if customcharset:
      self.charset = customcharset
    else:
      self.PickCharset()

  def PickCharset(self):
    self.charset = self.UPPERCHARS + self.LOWERCHARS + self.NUMBERS + self.SYMBOLS
    if self.options.OmitSimilarCharacters:
      self.charset = self.charset.strip('O0Il')
  
  def ContainsAny(self, string, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in string for c in set]

  def MakePassword(self):
    if self.options.PasswordLength < 5: # Recursion error otherwise
      return 'Password length too short'
    pwd = []
    for i in range(self.options.PasswordLength):
      pwd.append(self.charset[random.randint(0,len(self.charset)-1)])
    passwd = ''.join(pwd)
    self.generatedPassword = passwd
    self.CheckOptionsCompliance()
    return passwd

  def CheckOptionsCompliance(self):
    if self.options.MustHaveUpper and not self.ContainsAny(self.generatedPassword,self.UPPERCHARS):
      self.MakePassword()
    if self.options.MustHaveNumbers and not self.ContainsAny(self.generatedPassword,self.NUMBERS):
      self.MakePassword()
    if self.options.MustHaveSymbols and not self.ContainsAny(self.generatedPassword,self.SYMBOLS):
      self.MakePassword()
 
