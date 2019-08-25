# Adopted from: https://gist.github.com/jwcarr/626cbc80e0006b526688
import unittest
from math import log
from vi import variation_of_information, normalized_variation_of_information, normalized_information_distance

class TestVI(unittest.TestCase):
    def test_variation_of_information(self):
        # Identical partitions
        X1 = [ [1,2,3,4,5], [6,7,8,9,10] ]
        Y1 = [ [1,2,3,4,5], [6,7,8,9,10] ]
        vi1 = variation_of_information(X1, Y1)
        nvi1 = normalized_variation_of_information(X1, Y1)
        nid1 = normalized_information_distance(X1, Y1)
        self.assertEqual(vi1, 0)

        # Similar partitions
        X2 = [ [1,2,3,4], [5,6,7,8,9,10] ]
        Y2 = [ [1,2,3,4,5,6], [7,8,9,10] ]
        vi2 = variation_of_information(X2, Y2)
        nvi2 = normalized_variation_of_information(X2, Y2)
        nid2 = normalized_information_distance(X2, Y2)
        self.assertTrue(abs(vi2 - 1.102) < 0.0001)

        # Dissimilar partitions
        X3 = [ [1,2], [3,4,5], [6,7,8], [9,10] ]
        Y3 = [ [10,2,3], [4,5,6,7], [8,9,1] ]
        vi3 = variation_of_information(X3, Y3)
        nvi3 = normalized_variation_of_information(X3, Y3)
        nid3 = normalized_information_distance(X3, Y3)
        self.assertTrue(abs(vi3 - 2.302) < 0.0001)

        # Totally different partitions
        X4 = [ [1,2,3,4,5,6,7,8,9,10] ]
        Y4 = [ [1], [2], [3], [4], [5], [6], [7], [8], [9], [10] ]
        vi4 = variation_of_information(X4, Y4)
        nvi4 = normalized_variation_of_information(X4, Y4)
        nid4 = normalized_information_distance(X4, Y4)
        self.assertTrue(abs(vi4 - log(10, 2)) < 0.0001)

        self.assertEqual(nvi1, 0)
        self.assertTrue(nvi1 < nvi2)
        self.assertTrue(nvi2 < nvi3)
        self.assertTrue(nvi3 < nvi4)
        self.assertEqual(nvi4, 1)

        self.assertEqual(nid1, 0)
        self.assertTrue(nid1 < nid2)
        self.assertTrue(nid2 < nid3)
        self.assertTrue(nid3 < nid4)
        self.assertEqual(nid4, 1)


if __name__ == '__main__':
    unittest.main()
