import unittest
from app.libs.otb.super_vector import Dimension, SuperVector, Header
import numpy.testing as npt
import numpy as np
from copy import deepcopy
from ...base_test_app import BaseTestApp


class TestSuperVector(BaseTestApp):

    def setUp(self):
        self._dimension_11 = Dimension(
            "WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_12 = Dimension(
            "Colors", ("Red", "Blue", "Green", "Yellow"))
        self._dimension_13 = Dimension(
            "Fruits", ["Pear", "Orange", "Pineapple"])

        self._dimension_21 = Dimension(
            "WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_22 = Dimension(
            "Colors", ("Red", "Blue", "Green", "Yellow"))

        self._header_1 = Header(
            "Kids Data",  [self._dimension_11, self._dimension_12])
        self._header_2 = Header(
            "Kids Data", [self._dimension_21, self._dimension_22])
        self._header_3 = Header(
            "Other Data", [self._dimension_11, self._dimension_12, self._dimension_13])

        self._super_vector_1 = SuperVector(
            self._header_1, np.arange(12).reshape(3, 4))
        self._super_vector_2 = SuperVector(
            self._header_2, np.arange(12, 24).reshape(3, 4))

    def tearDown(self):
        pass  # doesn't use any of the app set up

    def test_get_dimension_name(self):
        self.assertEqual(self._dimension_13.get_name(), "Fruits")

    def test_set_dimension_name(self):
        _a_name = "Frutas"
        self._dimension_13.set_name(_a_name)
        self.assertEqual(self._dimension_13.get_name(), _a_name)
        self._dimension_13.set_name("Fruits")

    def test_add_remove_category_to_dimension(self):
        self._dimension_13.add_category("Apple")
        self.assertEqual(self._dimension_13.get_categories(), [
                         "Pear", "Orange", "Pineapple", "Apple"])
        self._dimension_13.remove_category()
        self.assertEqual(self._dimension_13.get_categories(),
                         ["Pear", "Orange", "Pineapple"])

    def test_get_categories_to_dimension(self):
        self.assertEqual(self._dimension_11.get_categories(),
                         ["Yakko", "Wakko", "Dot"])

    def test_set_categories_to_dimension(self):
        self._dimension_13.set_categories(["Pera", "Naranja", "Annana"])
        self.assertEqual(self._dimension_13.get_categories(),
                         ["Pera", "Naranja", "Annana"])
        self._dimension_13.set_categories(["Pear", "Orange", "Pineapple"])

    def test_get_index_category(self):
        self.assertEqual(self._dimension_11.get_index_category("Yakko"), 0)

    def test_get_copy_dimension(self):
        dim_copy = deepcopy(self._dimension_11)
        self.assertEqual(self._dimension_11, dim_copy)
        self.assertFalse(self._dimension_11 is dim_copy)

    def test_eq_dimension(self):
        self.assertEqual(self._dimension_11, self._dimension_21)
        self.assertNotEqual(self._dimension_11, self._dimension_13)

    def test_add_remove_dimension_to_header(self):
        self._header_1.add_dimension_last(self._dimension_13)
        self.assertEqual(self._header_1.get_dimensions(), [
                         self._dimension_11, self._dimension_12, self._dimension_13])
        self._header_1.remove_last_dimension()
        self.assertEqual(self._header_1.get_dimensions(), [
                         self._dimension_11, self._dimension_12])

    def test_get_dimensions_to_header(self):
        self.assertEqual(self._header_1.get_dimensions(),  [
                         self._dimension_11, self._dimension_12])

    def test_set_dimensions_to_header(self):
        self._header_1.set_dimensions([self._dimension_13, self._dimension_21])
        self.assertEqual(self._header_1.get_dimensions(), [
                         self._dimension_13, self._dimension_21])
        self._header_1.set_dimensions([self._dimension_11, self._dimension_12])

    def test_get_category_from_header(self):
        self.assertEqual(self._header_2.get_index_category(
            "WarnerBrothers", "Wakko"), [0, 1])
        self.assertEqual(self._header_2.get_index_category(
            "Colors", "Green"), [1, 2])
        self.assertEqual(self._header_2.get_index_category(
            "Sabores", "Dulce"), None)

    def test_eq_headers(self):
        self.assertEqual(self._header_1, self._header_2)
        self.assertNotEqual(self._header_1, self._header_3)

    def test_get_copy_header(self):
        header_copy = deepcopy(self._header_1)
        self.assertEqual(self._header_1, header_copy)
        self.assertFalse(self._header_1 is header_copy)

    def test_vector_get_header(self):
        self.assertEqual(self._super_vector_1.get_header(), self._header_1)

    def test_vector_set_header(self):
        self._super_vector_1.set_header(self._header_3)
        self.assertEqual(self._super_vector_1.get_header(), self._header_3)
        self._super_vector_1.set_header(self._header_1)

    def test_get_shape_from_header(self):
        self.assertEqual(self._header_1.get_shape_categories(
            ["Dot", "Blue"]), (2, 1))
        self.assertEqual(self._header_3.get_shape_categories(
            ["Wakko", "Red", "Orange"]), (1, 0, 1))
        self.assertEqual(self._header_3.get_shape_categories(
            ["Wakko", "Purple", "Banana"]), (1, None, None))

    def test_headers_are_same(self):
        self.assertEqual(self._header_1, self._header_2)
        self.assertNotEqual(self._header_1, self._header_3)

    def test_super_vector_are_same_type(self):
        self.assertTrue(
            self._super_vector_1.is_same_type(self._super_vector_2))

    def test_get_dimension_from_header(self):
        self.assertEqual(
            self._super_vector_1.get_index_dimension(self._dimension_11), 0)
        self.assertEqual(
            self._super_vector_1.get_index_dimension(self._dimension_12), 1)
        self.assertEqual(self._super_vector_1.get_index_dimension(
            Dimension("Seasons", [])), None)

    def test_get_dimension_by_name_from_header(self):
        self.assertEqual(
            self._super_vector_1.get_index_dimension_by_name("WarnerBrothers"), 0)
        self.assertEqual(
            self._super_vector_1.get_index_dimension_by_name("Colors"), 1)
        self.assertEqual(
            self._super_vector_1.get_index_dimension_by_name("Sabores"), None)

    def test_get_shape_from_super_vector(self):
        self.assertEqual(self._super_vector_1.get_shape_categories(
            ["Dot", "Blue"]), (2, 1))
        self.assertEqual(self._super_vector_1.get_shape_categories(
            ["Wakko", "Purple"]), (1, None))
        self.assertEqual(
            self._super_vector_1.get_shape_categories(["Yakko"]), (0,))

    def test_super_vector_addition(self):
        x1 = self._super_vector_1.get_index_category("WarnerBrothers", "Yakko")
        y1 = self._super_vector_1.get_index_category("WarnerBrothers", "Dot")
        x2 = self._super_vector_2.get_index_category("Colors", "Red")
        y2 = self._super_vector_2.get_index_category("Colors", "Green")
        npt.assert_almost_equal(self._super_vector_1.get_data() + self._super_vector_2.get_data(),
                                np.arange(12, 36, 2).reshape(3, 4))
        npt.assert_almost_equal(self._super_vector_1.get_data()[x1[-1]:y1[-1], x2[-1]:y2[-1]] +
                                self._super_vector_2.get_data(
        )[x1[-1]:y1[-1], x2[-1]:y2[-1]],
            np.arange(12, 36, 2).reshape(3, 4)[x1[-1]:y1[-1], x2[-1]:y2[-1]])


if __name__ == '__main__':
    unittest.main()
