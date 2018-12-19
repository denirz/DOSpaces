#coding:utf-8
from unittest import TestCase
from do_spaces_utils import getdir,create_subdir_structure
import os
import re
import shutil


class TestGetdir(TestCase):
    def test_getdir(self):
        key = '/Users/denirz/Documents/Development/DOSpaces/spaces/bin/python'
        res = getdir(key)
        self.assertEqual(res,'/Users/denirz/Documents/Development/DOSpaces/spaces/bin')

        key = '/Users/denirz/Documents/Development/DOSpaces/spaces/bins/'
        res = getdir(key)
        self.assertEqual(res, '/Users/denirz/Documents/Development/DOSpaces/spaces')

        key = '/Users/denirz/D2/Documents/Development/DOSpaces/spaces/bins/'
        res = getdir(key)
        self.assertEqual(res, '/Users/denirz')

        key = '/Users/denirz/BitTorrent Sync/iMedia/Финансовые требования/Проект/Final DocSet/4-9_ДопМатериалы/_9_ДопМатериалы_Документооборот/8_Документооборот_образцы документов/'
        res = getdir(key)
        self.assertEqual(res, key.rstrip('/'))

        key = '/Users/denirz/BitTorrent Sync/iMedia/Финансовые требования/Проект/Final DocSet/4-9_ДопМатериалы/_9_ДопМатериалы_Документооборот/8_Документооборот_образцы документов/asdasd'
        res = getdir(key)
        self.assertEqual(res,
                        '/Users/denirz/BitTorrent Sync/iMedia/Финансовые требования/Проект/Final DocSet/4-9_ДопМатериалы/_9_ДопМатериалы_Документооборот/8_Документооборот_образцы документов'
                         )

        key = u'/Users/denirz/BitTorrent Sync/iMedia/Финансовые требования/Проект/Final DocSet/4-9_ДопМатериалы/_9_ДопМатериалы_Документооборот/8_Документооборот_образцы документов/asdasd'
        res = getdir(key)
        self.assertEqual(res,
                         u'/Users/denirz/BitTorrent Sync/iMedia/Финансовые требования/Проект/Final DocSet/4-9_ДопМатериалы/_9_ДопМатериалы_Документооборот/8_Документооборот_образцы документов'
                         )

        key = u'/Users/denirz/BitTorrent Sync/PMedia/Финансовые требования/Проект/Final DocSet/4-9_ДопМатериалы/_9_ДопМатериалы_Документооборот/8_Документооборот_образцы документов/asdasd'
        res = getdir(key)
        self.assertEqual(res,
                         u'/Users/denirz/BitTorrent Sync'
                         )
        key = u'dsdsdsd'
        res = getdir(key)
        self.assertEqual(res,
                         u'/'
                         )


class TestCreateSreuct(TestCase):
    def test_create_subdir_structure(self):
        key = u'/Users/denirz/Documents/Development/DOSpaces/tests/dd/ase/se'
        dest = getdir(key)
        print dest
        res = create_subdir_structure(key)
        if res:
            self.assertTrue(os.path.isdir(res))
            pattern = re.compile(dest + '/(.*)')
            created  = pattern.search(res).group(1).split('/')[0]
            print "to delete {}".format(dest+'/'+created)
            shutil.rmtree(dest+'/'+created)
        print res
