import unittest
from otb.super_vector import Dimension, SuperVector, Header
import numpy as np


class TestSuperVector(unittest.TestCase):

    def setUp(self):
        self._dimension_11 = Dimension("WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_12 = Dimension("Colors", ("Red", "Blue", "Green", "Yellow"))
        self._dimension_13 = Dimension("Fruits", ["Pear", "Orange", "Pineapple"])

        self._dimension_21 = Dimension("WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_22 = Dimension("Colors", ("Red", "Blue", "Green", "Yellow"))

        self._header_1 = Header("Kids Data",  [self._dimension_11, self._dimension_12])
        self._header_2 = Header("Kids Data", [self._dimension_21, self._dimension_22])
        self._header_3 = Header("Other Data", [self._dimension_11, self._dimension_12, self._dimension_13])

        self._super_vector_1 = SuperVector(self._header_1, np.arange(12).reshape(3, 4))
        self._super_vector_2 = SuperVector(self._header_2, np.arange(12, 24).reshape(3, 4))

    def test_get_dimension_name(self):
        self.assertEqual(self._dimension_13.get_name(), "Fruits")

    def test_set_dimension_name(self):
        _a_name = "Frutas"
        self._dimension_13.set_name(_a_name)
        self.assertEqual(self._dimension_13.get_name(), _a_name)
        self._dimension_13.set_name("Fruits")

    def test_add_remove_category_to_dimension(self):
        self._dimension_13.add_category("Apple")
        self.assertEqual(self._dimension_13.get_categories(), ["Pear", "Orange", "Pineapple", "Apple"])
        self._dimension_13.remove_category()
        self.assertEqual(self._dimension_13.get_categories(), ["Pear", "Orange", "Pineapple"])

    def test_get_categories_to_dimension(self):
        self.assertEqual(self._dimension_11.get_categories(), ["Yakko", "Wakko", "Dot"] )

    def test_set_categories_to_dimension(self):
        self._dimension_13.set_categories(["Pera", "Naranja", "Annana"])
        self.assertEqual(self._dimension_13.get_categories(), ["Pera", "Naranja", "Annana"])
        self._dimension_13.set_categories(["Pear", "Orange", "Pineapple"])

    def test_eq_dimension(self):
        self.assertEqual(self._dimension_11, self._dimension_21)
        self.assertNotEqual(self._dimension_11, self._dimension_13)

    def test_add_remove_dimension_to_header(self):
        self._header_1.add_dimension(self._dimension_13)
        self.assertEqual(self._header_1.get_dimensions(), [self._dimension_11, self._dimension_12, self._dimension_13])
        self._header_1.remove_dimension()
        self.assertEqual(self._header_1.get_dimensions(), [self._dimension_11, self._dimension_12])


    def test_get_dimensions_to_header(self):
        self.assertEqual(self._header_1.get_dimensions(),  [self._dimension_11, self._dimension_12])

    def test_set_dimensions_to_header(self):
        self._header_1.set_dimensions([self._dimension_13, self._dimension_21])
        self.assertEqual(self._header_1.get_dimensions(), [self._dimension_13, self._dimension_21])
        self._header_1.set_dimensions([self._dimension_11, self._dimension_12])

    def test_eq_headers(self):
        self.assertEqual(self._header_1, self._header_2)
        self.assertNotEqual(self._header_1, self._header_3)

    def test_vector_get_header(self):
        self.assertEqual(self._super_vector_1.get_header(), self._header_1)


    def test_vector_set_header(self):
        self._super_vector_1.set_header(self._header_3)
        self.assertEqual(self._super_vector_1.get_header(), self._header_3)
        self._super_vector_1.set_header(self._header_1)



    def test_headers_are_same(self):
        self.assertEqual(self._header_1, self._header_2)
        self.assertNotEqual(self._header_1, self._header_3)

    def test_super_vector_are_same_type(self):
        self.assertTrue(self._super_vector_1.are_same_type(self._super_vector_2))

if __name__ == '__main__':
    unittest.main()
