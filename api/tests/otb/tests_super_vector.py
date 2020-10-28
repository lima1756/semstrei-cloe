import unittest
from otb.super_vector import Dimension, SuperVector, Header


class TestSuperVector(unittest.TestCase):

    def setUp(self):
        self._dimension_11 = Dimension("WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_12 = Dimension("Colors", ("Red", "Blue", "Green", "Yellow"))
        self.fruits = ("Fruits", ["Pear", "Orange", "Pineapple"])
        self._dimension_13 = Dimension(fruits)

        self._dimension_21 = Dimension("WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_22 = Dimension("Colors", ("Red", "Blue", "Green", "Yellow"))

        self._header_1 = Header("Kids Data",  [_dimension_11, _dimension_12])
        self._header_2 = Header("Kids Data", [_dimension_21, _dimension_22])
        self._header_3 = Header("Other Data", [_dimension_11, _dimension_12, _dimension_13])

        self._super_vector_1 = SuperVector(_header_1, np.arange(12).reshape(3, 4))
        self._super_vector_2 = SuperVector(_header_2, np.arange(12, 24).reshape(3, 4))

    def test_super_vector_are_same_type(self):
        self.assertTrue(self._super_vector_1.are_same_type(self._super_vector_2))


if __name__ == '__main__':
    unittest.main()
