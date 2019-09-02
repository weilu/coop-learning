import unittest
from distance_measures import to_label_array


class TestDistanceMeasures(unittest.TestCase):

    def test_to_label_array(self):
        x = [ [0,1,2,3,4], [5,6,7,8,9] ]
        xl = to_label_array(x)
        self.assertEqual(xl, [0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

        x = [ [0,1,2,3], [4,5,6,7,8,9] ]
        xl = to_label_array(x)
        self.assertEqual(xl, [0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

        x = [ [0,1,2,3,4,5], [6,7,8,9] ]
        xl = to_label_array(x)
        self.assertEqual(xl, [0, 0, 0, 0, 0, 0, 1, 1, 1, 1])

        x = [ [0,1], [2,3,4], [5,6,7], [8,9] ]
        xl = to_label_array(x)
        self.assertEqual(xl, [0, 0, 1, 1, 1, 2, 2, 2, 3, 3])

        x = [ [9,1,2], [3,4,5,6], [7,8,0] ]
        xl = to_label_array(x)
        self.assertEqual(xl, [2, 0, 0, 1, 1, 1, 1, 2, 2, 0])

        x = [ [0,1,2,3,4,5,6,7,8,9] ]
        xl = to_label_array(x)
        self.assertEqual(xl, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        x = [ [0], [1], [2], [3], [4], [5], [6], [7], [8], [9] ]
        xl = to_label_array(x)
        self.assertEqual(xl, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


if __name__ == '__main__':
    unittest.main()
