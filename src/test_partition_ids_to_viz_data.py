import unittest
from partition_ids_to_viz_data import partition_str_to_list


class TestPartitionIdsToVizData(unittest.TestCase):

    def test_partition_str_to_list(self):
        part_str = '{frozenset({86}), frozenset({0, 73})}\n'
        partition = partition_str_to_list(part_str)
        self.assertEqual(len(partition), 2)
        unique_members = set()
        for coal in partition:
            unique_members |= set(coal)
        self.assertEqual(len(unique_members), 3)


if __name__ == '__main__':
    unittest.main()
