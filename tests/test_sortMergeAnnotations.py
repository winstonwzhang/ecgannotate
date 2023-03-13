import unittest

from bin.sortMergeAnnotations import sortMergeAnnotations

class test(unittest.TestCase):
    def testsortMergeAnnotations(self):
        inputList = [{'start': 45, 'end': 75, 'type': 'AF'},
                     {'start': 23, 'end': 48, 'type': 'AB'},
                     {'start': 45, 'end': 75, 'type': 'AF'},
                     {'start': 23, 'end': 48, 'type': 'AF'},
                     {'start': 100, 'end': 101, 'type': 'AF'}]
        validateList = [{'start': 23, 'end': 75, 'type': 'AF'},
                        {'start': 23, 'end': 48, 'type': 'AB'},
                        {'start': 100, 'end': 101, 'type': 'AF'}]
        self.assertEqual(sortMergeAnnotations(inputList), validateList)

if __name__ == "__main__":
    unittest.main()