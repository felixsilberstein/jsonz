import os
import unittest
import json_tools as jt
import json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestStringMethods(unittest.TestCase):
    def test_correctness(self):
        sample = os.path.join(THIS_DIR, 'test-data', 'sample-test.json')
        jsonz_path = jt.compress(sample)
        jsonuz_path = jt.uncompress(jsonz_path)

        with open(sample) as fa:
            a = json.load(fa)
        with open(jsonuz_path) as fb:
            b = json.load(fb)
        self.assertEqual(sorted(a.items()), sorted(b.items()))
        
    def tearDown(self):
        '''TODO: IMplement deletion of files'''
        pass

if __name__ == '__main__':
    unittest.main()