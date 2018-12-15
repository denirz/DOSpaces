#coding:utf-8
from unittest import TestCase
import unittest
from do_spaces_utils import auth, MyBucket
import do_spaces_utils
import random
import os
import boto3

class TestMyBucket(TestCase):
    def test_auth(self):
        bt=auth()
        self.assertGreater(bt.objects.iterator().__sizeof__(),2)
        pass

    def test_listfiles(self):
        # bt=auth()
        bucket = MyBucket()
        listfiles = bucket.listfiles()
        print "listfiles: {}".format(listfiles)
        self.assertIsInstance(listfiles,list)
        print listfiles

    def  test_getinitialpath(self):
        key=u'Services_Irz_4.pdf'
        key2 = u'\u0447\u0442\u043e-\u0442\u043e'
        kee3 = u'\u041e\u0446\u0435\u043d\u043a\u0430_\u0440\u0430\u0431\u043e\u0442.docx'
        keywrong='test'
        # bt = auth()
        bucket = MyBucket()
        # print type(bucket.getinitialpath(kee3))
        self.assertEqual(bucket.getinitialpath(key),'') ## должен возвращать пустую строку если  путь не указан
        self.assertEqual(bucket.getinitialpath(key),'') ## должен возвращать пустую строку если  путь не указан
        self.assertEqual(bucket.getinitialpath(keywrong),'-1')

    def test_putfile(self):
        filename = u'/Users/denirz/BitTorrent Sync/iMedia/Интернет проекты/Grazia/Оценка_работ.docx'
        key = u'хорошевка электричество ноябрь 2015'
        bucket = MyBucket()
        res = bucket.putfile(filename,key)
        self.assertIsInstance(res,unicode)
        self.assertEqual(bucket.getinitialpath(key),filename)

        filename=u'/Users/denirz/BitTorrent Sync/iMedia/Интернет проекты/Grazia/GRAZIA iPhone 8 Plus.jpg'
        key = u'что-то от грации'
        res = bucket.putfile(filename, key)
        self.assertIsInstance(res, unicode)
        self.assertEqual(bucket.getinitialpath(key), filename)

        filename = u'/Users/denirz/BitTorrent Sync/iMedia/Интернет проекты/Grazia/GRAZIA iPhone 8 Plu.jpg'
        key = u'что-то от грации'
        # если файл не найден то надо поднять Assertion Eror:
        self.assertRaises(AssertionError,bucket.putfile,filename, key)

        # если ключа нет, то в качестве ключа берем имя файла
        filename = u'/Users/denirz/BitTorrent Sync/iMedia/Интернет проекты/Grazia/GRAZIA iPhone 8 Plus.jpg'
        # key = u''
        key= bucket.putfile(filename)
        print u"Key submitted:{}".format(key)
        self.assertEqual(key,filename)
        # self.assertRaises(AssertionError, bucket.putfile, filename, key)

        # если файла нет, то надо поднять тоже какуюто ошибку AssertionError
        filename = u''
        key = u'ыццу'
        self.assertRaises(AssertionError, bucket.putfile, filename, key)
        #todo
        # Если ключ уже существуюет то... по хорошему надо сделать новый  но  с признаком  следующего...
        # filename=u'/Users/denirz/Documents/Development/DOSpaces/tests/v21.782.368-russ-01.tif'
        # key = bucket.putfile(filename)
        # print u"Key submitted:{}".format(key)
        # self.assertEqual(key, filename)

    def test_listinitialpath(self):
        bucket =MyBucket()
        l,k=bucket.list_initialpath()
        self.assertEqual(len(l),len(k))
        self.assertGreater(len(l),1)
        print "{:=^40}:{:=^40}".format("key","path")
        for i in zip(k,l):
            print u"{:>40}:{:<40}".format(i[0][-39:],i[1][-39:])



    def test_putdir(self):
        dirname=u'/Users/denirz/Downloads/russ-18/'
        # dirname=u'/Users/denirz/Downloads/Telegram Desktop/'
        # dirname=u'/Users/denirz/Documents/Ideas/SkolTech/'
        bucket=MyBucket()
        self.assertRaises(AssertionError,bucket.putdir,'/sds')
        self.assertRaises(AssertionError,bucket.putdir,u'/sds')
        res = bucket.putdir(dirname)
        print res
        self.test_listinitialpath()

    def test_find_object_by_string(self):
        bucket=MyBucket()
        instr='asda'
        self.assertRaises(AssertionError,bucket.find_object_by_string,instr)
        instr=u"щ"
        print "__result:__"
        self.assertGreater(len(bucket.find_object_by_string(instr)),1)
        instr = u"\."
        self.assertGreater(len(bucket.find_object_by_string(instr)), 1)
        instr = u"asdasdaasdasdassdas"
        self.assertEqual(len(bucket.find_object_by_string(instr)), 0)


    def test_downloadfile(self):
        bucket=MyBucket()
        self.assertRaises(bucket.downloadfile)

        keylist = bucket.listfiles()

        samplekey = random.sample(keylist,1)[0]
        # print u"Sample Key:{}".format(samplekey)
        res= bucket.downloadfile(key=samplekey,targetdir='.')
        # print u"saved to {}".format(res)
        self.assertTrue(os.path.isfile(res))
        os.remove(res)

        samplekey = random.sample(keylist, 1)[0]
        # print u"Sample Key:{}".format(samplekey)
        tempdir= '/Users/denirz'
        assert  os.path.isdir(tempdir),"{} is not a directory".format(tempdir)
        res = bucket.downloadfile(key=samplekey, targetdir=tempdir)
        # print u"saved to {}".format(res)
        self.assertTrue(os.path.isfile(res))
        os.remove(res)

        samplekey = random.choice(keylist)
        # print u"Sample Key:{}".format(samplekey)
        # no target_dir:
        res= bucket.downloadfile(key=samplekey) #  no taargetdir
        # print u"saved to {}".format(res)
        self.assertTrue(os.path.isfile(res))
        os.remove(res)


        with self.assertRaises(AssertionError):
            res = bucket.downloadfile(key=samplekey,targetdir="/home/ds")  # no taargetdir

    def test_downloadfile_wrongKey(self):
        """
        попытка запустить в неверным ключом должна приводить к Exception наверно ...
        :return:
        """
        key="awdasdasdasda"
        bucket=MyBucket()
        with self.assertRaises(Exception):
            res = bucket.downloadfile(key=key)
            print res

    def test_deletfile(self):
        bucket=MyBucket()
        keylist=bucket.listfiles()
        key = random.choice(keylist)
        print u"Selected {}".format(key)
        bakfile = bucket.downloadfile(key=key)
        res = bucket.deletefile(key=key)
        self.assertEqual(res,0) # 0 возвращается если код ответа 200 +/-
        with self.assertRaises(Exception):
            bucket.deletefile(key=key)
        bucket.putfile(filepath=bakfile,key=key)

    @unittest.skip("нужен только для отладки")
    def test_debug(self):
        b = MyBucket()
        pass
