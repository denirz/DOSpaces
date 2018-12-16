from unittest import TestCase
import os
import sys
import subprocess
class Testdofile(TestCase):
    def setUp(self):
        self.cmd = [
            'python',
            '/Users/denirz/Documents/Development/DOSpaces/dofiles.py',
        ]
    def test_run(self):
        res = os.system('python /Users/denirz/Documents/Development/DOSpaces/dofiles.py')
        print "res={}".format(res)
        pass
    def test_run_subprocess(self):

        cmd = [
            'python',
            '/Users/denirz/Documents/Development/DOSpaces/dofiles.py',
            '--list',
        ]
        res = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
        print res
        cmd= [
            'python',
            '/Users/denirz/Documents/Development/DOSpaces/dofiles.py',
        ]
        res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print res
        pass
    def test_download(self):
        cmd=self.cmd
        cmd.append('download')
        cmd.append('/data')
        print cmd
        res = subprocess.check_output(cmd)
        print res

    def test_help(self):
        cmd =self.cmd
        cmd.append('-h')
        print cmd
        res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.assertRegexpMatches(res,'optional arguments')
        print res