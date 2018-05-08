import unittest

import numpy as np

from objloader import Obj


class TestCase(unittest.TestCase):

    def test_1(self):
        model = Obj.fromstring('''
            v 1.0 2.0 3.0
            v 1.0 1.0 1.0
            v 3.0 2.0 1.0

            vn 4.0 5.0 6.0
            vn 1.0 1.0 1.0
            vn 4.0 3.0 2.0

            vt 7.0 8.0 9.0
            vt 1.0 1.0 1.0
            vt 5.0 4.0 3.0

            f 1/1/1 2/2/2 3/3/3
        ''')

        arr = model.to_array()
        np.testing.assert_almost_equal(arr, [
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [3.0, 2.0, 1.0, 4.0, 3.0, 2.0, 5.0, 4.0, 3.0],
        ])


if __name__ == '__main__':
    unittest.main()
