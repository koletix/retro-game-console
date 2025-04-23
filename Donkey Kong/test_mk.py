import unittest
import game_mk

ladders, platforms = game_mk.import_level(1) 

class TestMK(unittest.TestCase):
    def test_ladders_none(self):
        self.assertTrue(ladders != None)

    def test_platforms_none(self):        
        self.assertTrue(platforms != None)        

    def test_ladders_count(self):        
        self.assertTrue(len(ladders) > 0)

    def test_platforms_count(self):        
        self.assertTrue(len(platforms) > 0)

    def test_ladders_info(self):        
        for ladder in ladders:
            self.assertTrue("row" in ladder)
            self.assertTrue("col" in ladder)
            self.assertTrue("slope_mult" in ladder)
            self.assertTrue("length" in ladder)

    def test_platforms_info(self):        
        for platform in platforms:
            self.assertTrue("row" in platform)
            self.assertTrue("col" in platform)
            self.assertTrue("slope_mult" in platform)
            self.assertTrue("length" in platform)

if __name__ == '__main__':
    unittest.main()