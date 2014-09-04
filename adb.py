import os
import subprocess
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    CYAN = '\033[0;36m'

class MyADB:
  def __init__(self):
    pass

  def lookup(self, command):
    return getattr(self, 'do_' + command.upper(), None)

  def do_LIST(self,path='/'):
    '''return a list of files'''
    cmd = ("adb shell ls -l \"" + path + "\"")
    files = subprocess.getstatusoutput(cmd)
    if files[0] == 0:
      f = files[1].split('\n')
      return f
    return []

class Menu:
  def __init__(self):
    self.intro()
    self.adb = MyADB()

  def intro(self):
    print("--------------------------------------")
    print("This is my \"personal\" ADB")
    print("I'll increase functionality as I need")
    self.contact()
    print("--------------------------------------")
    print("\n")

  def main(self):

    options = { 0:"Main Menu",
                1:"List files (/)" }

    print("Select your option:\n")

    for i in options:
      print('\t' + str(i) + ' - ' +options[i])

  def contact(self):
    print(bcolors.OKGREEN + "Tiago Maluta (@maluta)" + bcolors.ENDC)

  def do_1(self):
    '''...'''
    path = ['/']
    local_input='-1'
    while local_input not in '0':
      print("Listing:","".join(path))
      lst = self.adb.lookup('list')("".join(path))
      #
      for i,c in enumerate(lst):
        desc = c.split()
        if desc[0][0] == 'd': #dir
          p = ''
          for x in desc:
            m = re.match('[0-9]{2}:[0-9]{2}',x)
            if m != None:
              index = m.group(0)
              pos = desc.index(index)
              p = " ".join(desc[pos+1:])
              break
          print("\t",i+1,'-',bcolors.OKBLUE + p + bcolors.ENDC )
        elif desc[0][0] == 'l': #symlink
          print("\t",i+1,'-',bcolors.OKBLUE + desc[::-1][2] + bcolors.ENDC)
        else:
          print("\t",i+1,'-',bcolors.CYAN + desc.pop() + bcolors.ENDC)
      #
      local_input = input("> ")
      choice = lst[int(local_input)-1].split()
      if choice[0][0] == 'd':
        p = ''
        for x in choice:
          m = re.match('[0-9]{2}:[0-9]{2}',x)
          if m != None:
            index = m.group(0)
            pos = choice.index(index)
            p = " ".join(choice[pos+1:])
            break
        path.append(p+'/')
      elif choice[0][0] == 'l':
        path.append(choice[::-1][2]+'/')
      else:
        print("It's not a directory")

  def loop(self):
    option = '-1'
    while option not in '0':

      self.main()
      option = input("# ")

      if option == '1':
        self.do_1()

def main():
  menu = Menu() # ui
  menu.loop()

if __name__ == "__main__":
  main()
