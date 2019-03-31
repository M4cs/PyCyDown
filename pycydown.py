from lib.utils import (
    FileUtilities,
    PackagesParser
)
from configparser import ConfigParser
from lib.constants import CUR_DIR
import os, ntpath, webbrowser

class Commands:

    def __init__(self):
        self.repo = ''
        self.prefix = '$pycydown> '
        self.packages = {}
        self.loadedRepo = {}
        self.numToName = {}
        self.queue = []
        self.queuedNames = []
        self.udid = ''

    def main(self):
        self.help()
        while True:
            terminal = input(self.prefix).lower()
            if terminal[0:4] == 'help':
                self.helpm()
            elif terminal[0:4] == 'exit':
                webbrowser.open_new_tab('https://twitter.com/intent/follow?&region=follow_link&screen_name=maxbridgland&tw_p=followbutton')
                break
            elif terminal[0:4] == 'list':
                self.listPackages()
            elif terminal[0:7] == 'setrepo':
                self.setrepo()
            elif terminal[0:4] == 'grab':
                self.grab()
            elif terminal[0:5] == 'queue':
                for x in self.queuedNames:
                    print(x)
            elif terminal[0:5] == 'clear':
                self.queue.clear()
                self.queuedNames.clear()
            elif terminal[0:7] == 'setudid':
                self.setudid()
            elif terminal[0:4] == 'save':
                self.save()
            elif terminal[0:4] == 'load':
                self.load()
            elif terminal[0:8] == 'download':
                count = 0
                if self.udid == '':
                    for x in self.queue:
                        FileUtilities.downloadFile(x, self.queuedNames[count])
                        count += 1
                else:
                    for x in self.queue:
                        FileUtilities.downloadFileUDID(x, self.queuedNames[count], self.udid)
            else:
                print('Unknown Command | Use "help" command to display help menu.')
        exit()

    def helpm(self):
        if not self.repo:
            repo = ''
        else:
            repo = 'Loaded Repository: ' + self.repo
        if not self.queue:
            queue = ''
        else:
            queue = 'Queued Downloads: ' + str(len(self.queue))
        if not self.udid:
            udid = ''
        else:
            udid = 'UDID: ' + str(self.udid)
        print('''
%s
%s
%s
======== Help Menu ========

help      Display this menu
setrepo   Load repo from 
          config
setudid   Set UDID for 
          headers
queue     Show queued
clear     Clear queue
list      List available
          packages
download  Download queued
          packages
load      Load Config
save      Save Config
grab      Grab a package
          from repo
exit      Exit program
            ''' % (repo, queue, udid))
    
    def setrepo(self):
        print('Enter Repository')
        self.repo = input('$ ')
        loadRepo = PackagesParser(self.repo)
        loadRepo.get()
        print("")
        loadRepo.getPackageDict()
        FileUtilities.saveDictToJson(loadRepo.packages)
        count = 0
        for x in loadRepo.packages[loadRepo.baseUrl]:
            count += 1
            link = loadRepo.packages[self.repo][x]['link']
            self.packages.update({count:link})
        self.loadedRepo = loadRepo.packages

    def listPackages(self):
        if not self.loadedRepo:
            return print('Error: No Repo Loaded\nUse "load" command to load repository')
        count = 0
        for x in self.loadedRepo[self.repo]:
            count += 1
            print(str(count) + " | " + x.replace('\n', ''))
            self.numToName.update({count:x.replace('\n', '')})
    
    def setudid(self):
        print('Please Enter Device\'s UDID')
        udid = input('$ ')
        self.udid = udid

    def grab(self):
        if not self.loadedRepo:
            return print('Error: No Repo Loaded\nUse "load" command to load repository')
        while True:
            try:
                self.listPackages()
                print("\nChoose a package number from above to download.")
                choice = int(input('$ '))
                name = self.numToName[choice]
                while True:
                    print('Requested Package: %s' % name)
                    print('Are you sure you want to add this to the queue? (Y\\N)')
                    ans = str(input('$ ')).upper()
                    if ans == 'Y':
                        self.queue.append(self.packages[choice])
                        self.queuedNames.append(self.numToName[choice])
                        break
                    elif ans == 'N':
                        print('Cancelling')
                        break
                    else:
                        print('Please Choose Y or N')
                print('Would You Like To Add Another Package To The Queue? (Y\\N)')
                ans = str(input('$ ')).upper()
                if ans == 'Y':
                    pass
                elif ans == 'N':
                    break
                else:
                    print('Please Choose Y or N')
            except ValueError:
                print('Please Choose A Number')
        
    def save(self):
        print('Enter Name To Save Config To')
        name = input('$ ')
        config = ConfigParser()
        config['DEFAULT'] = {
            'repo': self.repo
        }
        if self.udid != '':
            config['DEFAULT'].update({'udid':self.udid})
        with open(FileUtilities.getRealPath(CUR_DIR + '/config/' + name + '.cfg'), 'w') as f:
            config.write(f)
    
    def load(self):
        from glob import iglob
        path = FileUtilities.getRealPath(CUR_DIR + "/config/*.cfg")
        for file in iglob(path, recursive=True):
            if len(file) == 0:
                return print('\nError: No Config Files Saved')
            print(str(ntpath.basename(file)).replace('.cfg', ''))
        print("")
        print('Choose Config From Above')
        name = input('$ ')
        if os.path.exists(FileUtilities.getRealPath(CUR_DIR + '/config/' + name + '.cfg')) == False:
            return print('\nError: Config File Not Found')
        config = ConfigParser()
        config.read(FileUtilities.getRealPath(CUR_DIR + '/config/' + name + '.cfg'))
        self.repo = config['DEFAULT']['repo']
        loadRepo = PackagesParser(self.repo)
        loadRepo.get()
        print("")
        loadRepo.getPackageDict()
        FileUtilities.saveDictToJson(loadRepo.packages)
        count = 0
        for x in loadRepo.packages[loadRepo.baseUrl]:
            count += 1
            link = loadRepo.packages[self.repo][x]['link']
            self.packages = {}
            self.packages.update({count:link})
        self.loadedRepo = loadRepo.packages
        if 'udid' in config['DEFAULT'].keys():
            self.udid = config['DEFAULT']['udid']
        print('Finished Loading Config: ', name + '\n')

        
try:
    print("""
PyCyDownloader
By: @maxbridgland

Download public packages and packages linked
to UDID's through the command line.

Donate:
https://paypal.me/MaxBridgland

""")
    run = Commands()
    run.main()
except KeyboardInterrupt:
    print('Goodbye')
    exit()