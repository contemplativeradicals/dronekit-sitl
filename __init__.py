#!/usr/bin/python

from __future__ import print_function
import re
import sys
import os
import subprocess
import string
import time
import json
import tarfile
import sys
import urllib
import urllib2
import os
import json
import shutil
from subprocess import Popen

sitl_host = 'http://d3jdmgrrydviou.cloudfront.net'
self = os.path.dirname(os.path.realpath(__file__))

def version_list():
    sitl_list = '{}/versions.json'.format(sitl_host)

    req = urllib2.Request(sitl_list, headers={'Accept':'*/*'})
    raw = urllib2.urlopen(req).read()
    versions = json.loads(raw)
    return versions

def download_sitl(system, target, version):
    sitl_file = "{}/{}/sitl-{}-v{}.tar.gz".format(sitl_host, system, target, version)

    if not os.path.isdir(self + '/sitl/' + system + '-' + version):
        print("Downloading SITL from %s" % sitl_file)

        testfile = urllib.URLopener()
        testfile.retrieve(sitl_file, self + '/sitl.tar.gz')

        tar = tarfile.open(self + '/sitl.tar.gz')
        tar.extractall(path=self + '/sitl/' + system + '-' + version)
        tar.close()

        print('Extracted.')
    else:
        print("SITL already Downloaded.")

def launch(system, version, args):
    args = [self + '/sitl/' + system + '-' + version + '/ArduCopter.elf'] + args
    print('Execute:', str(args))

    p = Popen(args, cwd=self)
    p.communicate()

def detect_target():
    if sys.platform == 'darwin':
        return 'osx'
    if sys.platform == 'windows':
        return 'win'
    return 'linux'

def reset():
    # delete local sitl installations
    shutil.rmtree(self + '/sitl/')
    print('SITL directory cleared.')
