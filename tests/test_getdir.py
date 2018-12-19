#coding:utf-8
from unittest import TestCase
from do_spaces_utils import getdir,create_subdir_structure

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
        key = u'/Users/denirz/Documents/Development/DOSpaces/tests/ds/as'
        res = create_subdir_structure(key)
        print res
