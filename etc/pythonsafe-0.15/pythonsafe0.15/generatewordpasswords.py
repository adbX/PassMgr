#! /usr/bin/python

##    generatewordpasswords.py - A "rememberable" password generator
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
import random, os

wordlist1filename = 'words4.txt'
wordlist2filename = 'words5.txt'

if not os.path.exists(wordlist1filename) or not os.path.exists(wordlist2filename):
    raise "You must configure two files with (long) lists of words or syllables to use"

wordlist1 = open(wordlist1filename,'r').readlines()
wordlist2 = open(wordlist2filename,'r').readlines()

specials = "~!@#$%^&*()_-+={}|[]:;<>?."
numbers = '1234567890'
password = ''
word1 = ''
word2 = ''
mutations = {'a':'4', 'i':'1', 's':'$', 'n':'^', '1':'!'}

def MakeWords():
    global word1, word2
    word1 = wordlist1[random.randint(0,len(wordlist1)-1)].strip()
    word2 = wordlist2[random.randint(0,len(wordlist2)-1)].strip()

def Mutate(char):
    for c in mutations.keys():
        if c == char:
            return mutations[c]
    return char


def AddElement():
   global password
   elem = elements.pop(random.randint(0,len(elements)-1))
   if elem == 'word1':
       password += word1
   elif elem == 'word2':
       password += word2
   elif elem == 'special':
       password += specials[random.randint(0,len(specials)-1)]
   elif elem == 'number':
       password += numbers[random.randint(0,len(numbers)-1)]
   elif elem == 'upper':
       if len(password) > 0:
         num = random.randint(0,len(password)-1)
         password = password[0:num] + password[num].upper() + password[num+1:]
   elif elem == 'mutate':
       if len(password) > 0:
         num = random.randint(0,len(password)-1)
         password = password[0:num] + Mutate(password[num]) + password[num+1:]

def Generate():
    global password, elements
    password = ''
    MakeWords()
    elements = ['word1','word2','special','number','upper','upper','mutate'] # add elements to list for longer password
    while len(elements) > 0:
        AddElement()
    return password

def Print(howmany):
    for i in range(howmany):
        print Generate() + " "

def Write():
    f = open('output.txt','w')
    for i in range(500):
        f.write(Generate() + '\n')
    f.close()

if __name__ == '__main__':
    Print(20)    
    #Write()
    raw_input()

