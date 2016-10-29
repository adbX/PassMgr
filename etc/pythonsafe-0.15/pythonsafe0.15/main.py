#! /usr/bin/python

##    main.py - The entry point
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
import sys,os
from lib.manager import PasswordManager
from console import Console

dataFileName = 'passwords.data'
sys.path.append(os.path.join(os.getcwd(),'lib/'))

def runconsole():
    console = Console(dataFileName)
    while 1:
      console.Menu()

if __name__ == '__main__':
    runconsole()

