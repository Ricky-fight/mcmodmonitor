import unittest

from curseforge import getPopularMods, getLastUpdatedMods


class MyTestCase(unittest.TestCase):
    def test_getPopularMods(self):
        index, pagesize = 0, 30
        mods = getPopularMods(index, pagesize)
        self.assertEqual(len(mods), pagesize)
        for mod in mods:
            print(mod.name)

    def test_getLastUpdatedMods(self):
        index, pagesize = 0, 30
        mods = getLastUpdatedMods(index, pagesize)
        self.assertEqual(len(mods), pagesize)
        for mod in mods:
            print(mod.name)


if __name__ == '__main__':
    unittest.main()