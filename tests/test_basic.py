import logging
import struct
import sys
import unittest

from objloader import Obj


class TestCase(unittest.TestCase):

    def test_1(self):
        model = Obj.fromstring('''
            v 1.0 2.0 3.0
            v 4.0 5.0 6.0
            v 7.0 8.0 9.0
            f 1 2 3
        ''')

        ax, ay, az = struct.unpack('3f', model.pack('vx'))
        self.assertAlmostEqual(ax, 1.0)
        self.assertAlmostEqual(ay, 4.0)
        self.assertAlmostEqual(az, 7.0)

    def test_2(self):
        model = Obj.fromstring('''
            v 1.0 2.0 3.0
            v 4.0 5.0 6.0
            v 7.0 8.0 9.0
            f 1 2 3
        ''')

        ax, ay, az, bx, by, bz, cx, cy, cz = struct.unpack('9f', model.pack('vx vy vz'))
        self.assertAlmostEqual(ax, 1.0)
        self.assertAlmostEqual(ay, 2.0)
        self.assertAlmostEqual(az, 3.0)
        self.assertAlmostEqual(bx, 4.0)
        self.assertAlmostEqual(by, 5.0)
        self.assertAlmostEqual(bz, 6.0)
        self.assertAlmostEqual(cx, 7.0)
        self.assertAlmostEqual(cy, 8.0)
        self.assertAlmostEqual(cz, 9.0)

    def test_3(self):
        model = Obj.fromstring('''
            v 1.0 2.0 3.0
            v 4.0 5.0 6.0
            v 7.0 8.0 9.0
            f 1 2 3
        ''')

        ax, anx, bx, bnx, cx, cnx = struct.unpack('6f', model.pack('vx nx'))
        self.assertAlmostEqual(ax, 1.0)
        self.assertAlmostEqual(anx, 0.0)
        self.assertAlmostEqual(bx, 4.0)
        self.assertAlmostEqual(bnx, 0.0)
        self.assertAlmostEqual(cx, 7.0)
        self.assertAlmostEqual(cnx, 0.0)

    def test_4(self):
        model = Obj.fromstring('''
            v 1.0 2.0 3.0
            vt 3.0 4.0 5.0
            vn 7.0 8.0 9.0
            f 1/1/1 1/1/1 1/1/1
        ''')

        vx, ty, nz = struct.unpack('3f', model.pack('vx ty nz')[:12])
        self.assertAlmostEqual(vx, 1.0)
        self.assertAlmostEqual(ty, 4.0)
        self.assertAlmostEqual(nz, 9.0)


if __name__ == '__main__':
    unittest.main()
