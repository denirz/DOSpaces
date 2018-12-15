from unittest import TestCase
from do_spaces_utils import checkfilename

class TestCheckfilename(TestCase):
    def test_checkfilename(self):

        self.assertTrue(checkfilename(u'asdd.doc'),"Unicode name _asdd.doc shoule be True")
        self.assertTrue(checkfilename(u'asdd.do')," 2 letters extention is ok ")
        self.assertTrue(checkfilename(u'asdd.d')," 1 letters extention is ok ")
        self.assertTrue(checkfilename(u'asdd.docs')," 4 letters extention is ok ")
        self.assertFalse(checkfilename(u'asdd.')," empty extension is not ok even with comma")
        self.assertFalse(checkfilename(u'asdd')," empty extension is not ok ")

        self.assertTrue(checkfilename(u'/s/asdd.doc')," empty extension is not ok ")
        self.assertTrue(checkfilename('asdd.doc'), "non-unicode name should be true")
        self.assertTrue(checkfilename('asdd.do'), " 2 letters extention is ok ")
        self.assertTrue(checkfilename('asdd.d'), " 1 letters extention is ok ")
        self.assertTrue(checkfilename('asdd.docs'), " 4 letters extention is ok ")
        self.assertFalse(checkfilename('asdd.'), " empty extension is not ok even with comma")
        self.assertFalse(checkfilename('asdd'), " empty extension is not ok ")
        self.assertTrue(checkfilename('/s/asdd.doc'), " empty extension is not ok ")
        self.assertTrue(checkfilename('.DS_Store'), ".DS_Store is OK  ")
        self.assertTrue(checkfilename(u'.DS_Store'), "unicode .DS_Store is OK  ")
