# Adopted from: https://gist.github.com/jwcarr/626cbc80e0006b526688
import unittest
from math import log
from vi import variation_of_information

class TestVI(unittest.TestCase):
    def test_variation_of_information(self):
        # Identical partitions
        X1 = [ [1,2,3,4,5], [6,7,8,9,10] ]
        Y1 = [ [1,2,3,4,5], [6,7,8,9,10] ]
        vi = variation_of_information(X1, Y1)
        self.assertEqual(vi, 0)

        # Similar partitions
        X2 = [ [1,2,3,4], [5,6,7,8,9,10] ]
        Y2 = [ [1,2,3,4,5,6], [7,8,9,10] ]
        vi = variation_of_information(X2, Y2)
        self.assertTrue(vi - 1.102 < 0.0001)

        # Dissimilar partitions
        X3 = [ [1,2], [3,4,5], [6,7,8], [9,10] ]
        Y3 = [ [10,2,3], [4,5,6,7], [8,9,1] ]
        vi = variation_of_information(X3, Y3)
        self.assertTrue(vi - 2.302 < 0.0001)

        # Totally different partitions
        X4 = [ [1,2,3,4,5,6,7,8,9,10] ]
        Y4 = [ [1], [2], [3], [4], [5], [6], [7], [8], [9], [10] ]
        vi = variation_of_information(X4, Y4)
        self.assertTrue(vi - log(10, 2) < 0.0001)


if __name__ == '__main__':
    unittest.main()
