#coding:utf-8
from unittest import TestCase
import unittest
import os
import sys
import copy
import re
import subprocess
import do_spaces_utils
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
        cmd.append('/asdasd/data')
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

    def test_list(self):
        cmd =self.cmd
        cmd.append('-l')
        print cmd
        res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        # self.assertRegexpMatches(res,'optional arguments')
        print res

    def test_list_k(self):
        key = u'/Users/denirz/Documents/Ideas/GlobalTelecom/Учет времени/Июнь 2014/ А'
        cmd = self.cmd
        cmd.append('-l')
        cmd.append('-k')
        cmd.append(key)
        print cmd
        res = subprocess.check_output(cmd,)
        self.assertRegexpMatches(res,"GlobalTelecom/Учет")
        print res

    def test_list_k_depth(self):
        key = u'/Users/denirz/Documents/Ideas/GlobalTelecom/'
        cmd = self.cmd
        cmd.append('-l')
        cmd.append('-k')
        cmd.append(key)
        cmd.append('--depth')
        cmd.append('3')
        print cmd
        res = subprocess.check_output(cmd,)
        self.assertRegexpMatches(res,"GlobalTelecom/Учет")
        print res


    def test_upload_file(self):
        cmd=self.cmd
        cmd.append('-u')
        cmd.append(u'/Users/denirz/Documents/CV/выход  из сумасшествия.pages')
        print cmd
        res = subprocess.check_output(cmd)
        self.assertRegexpMatches(res,'NEWKey=')
        print res

    @unittest.skip("not inplemented yet ")
    def test_upload_key(self):
        cmd=self.cmd
        cmd.append('-u')
        cmd.append(u'/Users/denirz/Documents/CV/выход  из сумасшествия.pages')
        cmd.append('-k')
        cmd.append('somestupid Key')
        print cmd
        res = subprocess.check_output(cmd)
        print res
        self.assertRegexpMatches(res,'Uploading')

    def test_upload_catalog(self):
        cmd=self.cmd
        cmd.append('-u')
        cmd.append(u'/Users/denirz/Dropbox/ТТК/')
        print cmd
        res = subprocess.check_output(cmd)
        print res
        self.assertRegexpMatches(res,'Uploading')



    def test_subparser(self):
        cmd = self.cmd
        cmd.append('-u')
        cmd.append('source')
        print cmd
        res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        # self.assertRegexpMatches(res, 'optional arguments')
        print res

        cmd.append('-k')
        print cmd
        with self.assertRaises(subprocess.CalledProcessError):
            res = subprocess.check_output(cmd)

        # self.assertRegexpMatches(res, 'optional arguments')
        print res

        cmd.append(u'asdasdkjhda')
        print cmd
        res = subprocess.check_output(cmd)
        # self.assertRegexpMatches(res, 'optional arguments')
        print res

    def test_download(self):
        """
        просто загружаем  указывая только ключ
        :return:
        """
        cmd = self.cmd
        cmd.append('-d')
        # cmd.append('-k')
        # cmd.append('samplekey')
        print cmd
        # with self.assertRaises(subprocess.CalledProcessError):
        res = subprocess.check_output(cmd)
        print res
        self.assertRegexpMatches(res,'provide key')
        cmd.append('-k')
        print cmd
        with self.assertRaises(subprocess.CalledProcessError):
            res = subprocess.check_output(cmd)
        print res
        cmd.append('somekey')
        print " ".join(cmd)
        res = subprocess.check_output(cmd)


        cmd.pop()
        samplekey = 'd/ddddsds.jpg'
        cmd.append(samplekey)
        print " ".join(cmd)
        res = subprocess.check_output(cmd)
        print res
        fname = re.findall(".*\"(.*)\"", res)
        print "FNAME{}".format(fname)
        filename =  os.path.abspath(fname[1])
        print filename
        print os.path.isfile(filename)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)

        # self.assertRegexpMatches(res, 'optional arguments')

        # cmd = self.cmd
        # cmd=cmd[:-1]
        # cmd.append('-u')
        # cmd.append('source')
        # print cmd
        # res = subprocess.check_output(cmd)
        # self.assertRegexpMatches(res, 'optional arguments')
        # print res

    def test_delete(self):
        filename = '/Users/denirz/outfile.txt'
        upload = copy.deepcopy(self.cmd)
        upload.append('-u')
        upload.append(filename)
        print " ".join(upload)
        res = subprocess.check_output(upload)
        print res
        listfiles = do_spaces_utils.MyBucket().list_key_prefix(filename)
        self.assertIn(filename,listfiles)

        delete = copy.deepcopy(self.cmd)
        delete.append('--delete')
        delete.append('-k')
        delete.append(filename)
        print " ".join(delete)
        res = subprocess.check_output(delete)
        print res
        listfiles = do_spaces_utils.MyBucket().list_key_prefix(filename)
        self.assertNotIn(filename,listfiles)


    def test_keys_with_spaces(self):
        key = '/Users/denirz/BitTorrent Sync/iMedia/'
        self.cmd.append('-l')
        self.cmd.append('-k')
        self.cmd.append(key)
        print " ".join(self.cmd)
        res = subprocess.check_output(self.cmd)
        # print res
        for line in res.split("\n"):
            # print line
            if line.startswith("/"):
                self.assertRegexpMatches(line,'^'+key)



    def test_get_url(self):
        # key = '/Users/denirz/BitTorrent Sync/iMedia/'
        key = 'd.d/ddddsds.jpg'
        self.cmd.append('-k')
        self.cmd.append(key)
        self.cmd.append('--link')
        self.cmd.append('2')
        print " ".join(self.cmd)
        res = subprocess.check_output(self.cmd)
        print res

        key = '/Users/denirz/BitTorrent Sync/iMedia/'
        cmdwrongkey = ['python',
                            '/Users/denirz/Documents/Development/DOSpaces/dofiles.py',
                            '-k',key,'--link','2']
        res = subprocess.check_output(cmdwrongkey)
        print res
        self.assertRegexpMatches(res,key)
        self.assertRegexpMatches(res,'not found')
