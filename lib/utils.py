from lib.constants import CUR_DIR
from progress.spinner import Spinner
from configparser import ConfigParser
import requests, bz2, os, json

class PackagesParser:

    def __init__(self, url):
        if str(url).endswith('/'):
            self.baseUrl = url[-1:]
        else:
            self.baseUrl = url
        self.url = url + "/Packages.bz2"
        self.url_1 = url + "/Packages.gz"
        self.url_2 = url + "/Packages"
        self.path = ''
        self.pathTxt = ''
        self.packages = {self.baseUrl:{}}
        self.numOfPackages = int

    def get(self):
        self.path = FileUtilities.getRealPath(CUR_DIR + '/tmp/Packages.bz2')
        self.pathTxt = FileUtilities.getRealPath(CUR_DIR + '/tmp/Packages.txt')
        try:
            res = requests.get(self.url)
            res.raise_for_status()
            with open(self.path, 'wb') as f:
                for block in res.iter_content(1024):
                    f.write(block)
                f.close()
            with bz2.BZ2File(self.path, 'r') as fp:
                resultListBytes = fp.readlines()
                with open(self.pathTxt, 'w') as f:
                    for x in resultListBytes:
                        f.write(x.decode('utf-8'))
                f.close()
        except Exception as e:
            print(e)
    
    def getPackageDict(self):
        file = open(self.pathTxt, 'r')
        fileRead = file.readlines()
        subpackages = {}
        names = []
        links = []
        versions = []
        print('Grabbing Package Names...')
        for line in fileRead:
            if line.startswith('Name: '):
                line = line.replace('Name: ', '')
                names.append(line)
        print('Grabbing Links...')
        for line in fileRead:
            if line.startswith('Filename: '):
                if 'https://' not in line:
                    newLine = line.replace('Filename: ', '')
                    if newLine.startswith('./') == True:
                        newLine = newLine[2:]
                    newLine1 = self.baseUrl + "/" + newLine
                    links.append(newLine1)
        print('Grabbing Package Versions...')
        for line in fileRead:
            if line.startswith('Version: '):
                line = line.replace('Version: ', '')
                versions.append(line)
        print('Finished Grabbing Packages...')
        print('Found %d packages' % len(names))
        for x in range(len(names)):
            subpackages.update({names[x]:{'version':versions[x], 'link':links[x]}})
        self.packages[self.baseUrl] = subpackages
        self.numOfPackages = len(names)
        file.close()
        os.remove(self.path)
        os.remove(self.pathTxt)

    def reloadSource(self):
        self.get()
        self.getPackageDict()
        print('Packages Updated.')
        
        

class FileUtilities:

    @staticmethod
    def getRealPath(path):
        return os.path.realpath(path)
        
    @staticmethod
    def refreshPackages():
        os.remove(FileUtilities.getRealPath(CUR_DIR + '/tmp/Packages.txt'))
    
    @staticmethod
    def saveDictToJson(d):
        data = json.dumps(d, indent=4, sort_keys=True)
        with open(FileUtilities.getRealPath(CUR_DIR + '/tmp/Packages.json'), 'w') as f:
            f.write(data)

    @staticmethod
    def downloadFile(link, name):
        downloadPath = FileUtilities.getRealPath(CUR_DIR + '/downloads/%s.deb' % name)
        os.system('wget -q -O %s %s' % (downloadPath, link))
    
    @staticmethod
    def downloadFileUDID(link, name, udid):
        downloadPath = FileUtilities.getRealPath(CUR_DIR + '/downloads/%s.deb' % name)
        os.system('wget -q -O %s %s --header="%s"' % (downloadPath, link, "X-Unique-ID: " + udid))