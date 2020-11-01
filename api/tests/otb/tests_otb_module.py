import unittest
from otb.super_vector import Dimension, SuperVector, Header
import otb.otb_module as otb_functions
import numpy as np
import numpy.testing as npt
from copy import deepcopy


class TestSuperVector(unittest.TestCase):

    def setUp(self):
        self._dimension_11 = Dimension("WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_12 = Dimension("Colors", ("Red", "Blue", "Green", "Yellow"))
        self._dimension_13 = Dimension("Fruits", ["Pear", "Orange", "Pineapple"])

        self._dimension_21 = Dimension("WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_22 = Dimension("Colors", ("Red", "Blue", "Green", "Yellow"))

        self._header_1 = Header("Kids Data",  [self._dimension_11, self._dimension_12])
        self._header_2 = Header("Kids Data",  [self._dimension_11, self._dimension_12])
        self._header_1_expanded = Header("Kids Data",  [self._dimension_13, self._dimension_11, self._dimension_12])

        self._super_vector_1 = SuperVector(self._header_1, np.arange(12).reshape(3, 4))
        self._super_vector_2 = SuperVector(self._header_2, np.arange(12, 24).reshape(3, 4))

        self._super_vector_3 = SuperVector(self._header_1, np.array([[1, 2, 4], [2, 4, 8], [3, 6, 12]]))
        self._super_vector_4 = SuperVector(self._header_2, np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]]))

    def test_insert_dimension_to_shape(self):
        self.assertEqual(otb_functions.insert_dimension_to_shape((1, 2), 0, 3), (3, 1, 2))
        self.assertEqual(otb_functions.insert_dimension_to_shape((3, 4), 1, 7), (3, 7, 4))
        self.assertEqual(otb_functions.insert_dimension_to_shape((1, 2), 3, 3), (1, 2, 3))
        self.assertEqual(otb_functions.insert_dimension_to_shape((1, 2), 1.5, 3), None)
        self.assertEqual(otb_functions.insert_dimension_to_shape((1, 2), 7, 3), (1, 2, 3))
        self.assertEqual(otb_functions.insert_dimension_to_shape((1, 2), -7, 3), (3, 1, 2))

    def test_get_inventario_piso_por_periodo(self):
        shape = self._super_vector_1.get_data().shape
        sv_new_dimension = otb_functions.get_inventario_piso_por_periodo(self._super_vector_1, self._dimension_13)

        # Test Header was properly changed
        self.assertEqual(sv_new_dimension.get_header(), self._header_1_expanded)

        # Test Data was added dimension in the proper place.
        npt.assert_almost_equal(sv_new_dimension.get_data(),
                                np.array([np.arange(12).reshape(shape),
                                          np.zeros(shape),
                                          np.zeros(shape)]))

    def test_get_percentage_otb(self):
        sv_percentage_otb = otb_functions.get_percentage_otb(self._super_vector_3, self._super_vector_4)
        npt.assert_almost_equal(sv_percentage_otb.get_data(), (100*np.array([[0, 2, 2], [2, 2, (8/3)], [1.5, 2, 3]])))

    def test_get_absolute_otb(self):
        shape = self._super_vector_1.get_data().shape
        sv_test_percentage_otb = otb_functions.get_absolute_otb(self._super_vector_2, self._super_vector_1)
        self.assertEqual(sv_test_percentage_otb.get_header(), self._super_vector_2.get_header())
        npt.assert_almost_equal(sv_test_percentage_otb.get_data(), (12 * np.ones(shape)))

    def test_get_target_stock(self):
        test_target_stock = otb_functions.get_target_stock(self._super_vector_3, 1.5)
        self.assertEqual(test_target_stock.get_header(), self._super_vector_3.get_header())
        npt.assert_almost_equal(test_target_stock.get_data(), np.array([[2.25, 4.5, 9], [3.75, 7.5, 15], [4.5, 9, 18]]))


if __name__ == '__main__':
    unittest.main()
