import unittest
from cache import FingerPrintCache


class MyTestCase(unittest.TestCase):
    def test_cache(self):
        filename = "test.cache"
        cache = FingerPrintCache(filename)
        cache.data = {"modslug1":{1,2,3,4,5},"modslug2":{1,2,3,4,5}}
        cache.save()
        retrivedData = FingerPrintCache(filename).data
        self.assertEqual(cache.data, retrivedData)  # add assertion here


if __name__ == '__main__':
    unittest.main()
