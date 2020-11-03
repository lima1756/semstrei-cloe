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
        self._dimension_14 = Dimension("Temperature", ["Cold", "Hot"])

        self._header_1 = Header("Kids Data",  [self._dimension_11, self._dimension_12])
        self._header_1_expanded = Header("Kids Data",  [self._dimension_13, self._dimension_11, self._dimension_12])
        self._header_3 = Header("Kids Data", [self._dimension_11, self._dimension_12, self._dimension_13])
        self._header_4 = Header("Control 4 dim", [self._dimension_11, self._dimension_12, self._dimension_14])

        self._super_vector_1 = SuperVector(self._header_1, np.arange(12).reshape(3, 4))
        self._super_vector_2 = SuperVector(self._header_1, np.arange(12, 24).reshape(3, 4))
        self._super_vector_3 = SuperVector(self._header_1, np.array([[1, 2, 4, 0], [2, 4, 8, -10], [3, 6, 12, 34]]))
        self._super_vector_4 = SuperVector(self._header_1, np.array([[0, 1, 2, 0], [1, 2, 3, 0], [2, 3, 4, 10]]))
        self._super_vector_5 = SuperVector(self._header_3, np.arange(3 * 4 * 3).reshape(3, 4, 3))
        self._super_vector_6 = SuperVector(self._header_4, np.array(
            [[[0, 1], [1, 3], [.5, .5], [1, 1]],
             [[1, 2], [2, 6], [.3, .3], [1, 2]],
             [[2, 4], [4, 12], [.7, .7], [1, 3]]]))

    def test_join_super_vector_with_category(self):
        sv_con_extra_dim = otb_functions.join_super_vector_with_category(self._super_vector_5, self._super_vector_6)
        new_header = Header("", [self._dimension_11, self._dimension_12, self._dimension_13, self._dimension_14])
        self.assertEqual(new_header, sv_con_extra_dim.get_header())
        print(sv_con_extra_dim.get_data())
        npt.assert_almost_equal(sv_con_extra_dim.get_data(), [[[[0, 0],     [0, 1],      [0, 2]],
                                                               [[3, 9],     [4, 12],     [5, 15]],
                                                               [[3, 3],     [3.5, 3.5],  [4, 4]],
                                                               [[9, 9],     [10, 10],    [11,   11]]],
                                                              [[[12, 24],   [13, 26],    [14, 28]],
                                                               [[30, 90],   [32, 96],    [34, 102]],
                                                               [[5.4, 5.4], [5.7, 5.7],  [6,  6]],
                                                               [[21, 42],   [22., 44],   [23, 46]]],
                                                              [[[48, 96],   [50., 100],  [52, 104]],
                                                               [[108, 324], [112., 336], [116, 348]],
                                                               [[21, 21], [21.7,  21.7], [22.4,  22.4]],
                                                               [[33.,   99], [34.,  102], [35.,  105]]]])

    def test_insert_time_dimension(self):
        sv_con_time = otb_functions.insert_time_dimension(self._super_vector_1, self._dimension_14,
                                                          new_header_name="Temp, Bros, & Colors.")
        self.assertEqual(sv_con_time.get_header(), Header("Temp, Bros, & Colors.",
                                                          [self._dimension_14, self._dimension_11, self._dimension_12]))
        npt.assert_almost_equal(sv_con_time.get_data(),
                                np.array([[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]],
                                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]))

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
        npt.assert_almost_equal(sv_percentage_otb.get_data(), (100*np.array([[0, 2, 2, 0], [2, 2, (8/3), 0],
                                                                             [1.5, 2, 3, 3.4]])))

    def test_get_absolute_otb(self):
        shape = self._super_vector_1.get_data().shape
        sv_test_percentage_otb = otb_functions.get_absolute_otb(self._super_vector_2, self._super_vector_1)
        self.assertEqual(sv_test_percentage_otb.get_header(), self._super_vector_2.get_header())
        npt.assert_almost_equal(sv_test_percentage_otb.get_data(), (12 * np.ones(shape)))

    def test_get_target_stock(self):
        test_target_stock = otb_functions.get_target_stock(self._super_vector_3, 1.5)
        self.assertEqual(test_target_stock.get_header(), self._super_vector_3.get_header())
        npt.assert_almost_equal(test_target_stock.get_data(), np.array([[2.25, 4.5, 9, -7.5],
                                                                        [3.75, 7.5, 15, 18], [4.5, 9, 18, 51]]))

    def test_get_data_projection_eom_stock_for_period(self):
        sv_stock_inicial_por_periodo = SuperVector(self._header_3, 2 * np.ones((3, 4, 3)))
        sv_inventario_piso = SuperVector(self._header_3, np.ones((3, 4, 3)))
        sv_compras = SuperVector(self._header_3, np.ones((3, 4, 3)))
        sv_devoluciones = SuperVector(self._header_3, np.ones((3, 4, 3)))
        test_target_venta = np.zeros((3, 4, 3,))
        test_target_venta[0] += 3 * np.ones((4, 3,))
        test_target_venta[1] += 5 * np.ones((4, 3,))
        test_target_venta[2] += 6 * np.ones((4, 3,))

        sv_target_venta = SuperVector(self._header_3, test_target_venta)
        eom0 = otb_functions.get_data_projection_eom_stock_for_period(sv_stock_inicial_por_periodo, sv_inventario_piso,
                                                                      sv_compras, sv_devoluciones, sv_target_venta, 0)
        eom1 = otb_functions.get_data_projection_eom_stock_for_period(sv_stock_inicial_por_periodo, sv_inventario_piso,
                                                                      sv_compras, sv_devoluciones, sv_target_venta, 1)
        eom2 = otb_functions.get_data_projection_eom_stock_for_period(sv_stock_inicial_por_periodo, sv_inventario_piso,
                                                                      sv_compras, sv_devoluciones, sv_target_venta, 2)
        npt.assert_almost_equal(eom0, 2 * np.ones((4, 3,)))
        npt.assert_almost_equal(eom1, np.zeros((4, 3,)))
        npt.assert_almost_equal(eom2, -1 * np.ones((4, 3,)))

    def test_calculate_otb(self):
        time_dimension = Dimension("Tiempo", ["Hoy", "Prox Semana"])
        une_dimension = Dimension("Une", ["Bolsas", "Monederos"])
        submarca_dimension = Dimension("Submarca", ["Mujer", "Hombre", "Niños"])
        mercado_dimension = Dimension("Mercado", ["M1", "M2"])
        categoria_dimension = Dimension("Categoria", ["Moda", "Basico"])
        tusmc = [time_dimension, une_dimension, submarca_dimension, mercado_dimension, categoria_dimension]
        tuc = [time_dimension, une_dimension, categoria_dimension]
        usmc = tusmc[1:]
        tusm = [time_dimension, une_dimension, submarca_dimension, mercado_dimension]
        # Header( "Header", tusmc)
        sv_stock_inicial = SuperVector(Header("Stock Inicial", usmc), np.arange(24).reshape(2, 3, 2, 2))
        sv_inventario_piso = SuperVector(Header("Inventario Piso", usmc),  2 * np.ones((2, 3, 2, 2,)))
        sv_compras = SuperVector(Header("Compras", tusmc),   np.ones((2, 3, 2, 2,)))
        sv_devoluciones_general = SuperVector(Header("Devoluciones", tusm), np.ones((2, 2, 3, 2,)))
        sv_plan_ventas_general = SuperVector(Header("Plan Ventas", tusm), 7 * np.ones((2, 2, 3, 2,)))
        sv_rate_control_moda_basico = SuperVector(Header("Control Moda Basico", tuc),
                                                  np.array([[[0.2, 0.8], [0.6, 0.4]], [[0.1, 0.9], [0.7, 0.3]]]))
        otb_output = otb_functions.calculate_otb(sv_stock_inicial, sv_inventario_piso, sv_compras,
                                                 sv_devoluciones_general, sv_plan_ventas_general,
                                                 sv_rate_control_moda_basico, time_dimension)
        sv_stock_inicial = otb_output[0]
        sv_inventario_piso = otb_output[1]
        sv_compras = otb_output[2]
        sv_devoluciones = otb_output[3]
        sv_target_venta = otb_output[4]
        sv_projection_eom_stock = otb_output[5]
        sv_target_stock = otb_output[6]
        sv_absolute_otb = otb_output[7]
        sv_percentage_otb = otb_output[8]

        npt.assert_almost_equal(sv_stock_inicial.get_data(), np.array([[[[[0,  1], [2., 3.]],
                                                                         [[4, 5], [6., 7.]],
                                                                         [[8, 9], [10., 11.]]],
                                                                        [[[12, 13], [14., 15.]],
                                                                         [[16, 17], [18., 19.]],
                                                                         [[20, 21], [22., 23.]]]],
                                                                       [[[[1.8, -0.8], [3.8,  1.2]],
                                                                         [[5.8,  3.2], [7.8,  5.2]],
                                                                         [[9.8,  7.2], [11.8,  9.2]]],
                                                                        [[[11.4, 13.6], [13.4, 15.6]],
                                                                         [[15.4, 17.6], [17.4, 19.6]],
                                                                         [[19.4, 21.6], [21.4, 23.6]]]]]))
        npt.assert_almost_equal(sv_inventario_piso.get_data(), np.array([[[[[2., 2.], [2., 2.]],
                                                                           [[2., 2.], [2., 2.]],
                                                                           [[2., 2.], [2., 2.]]],
                                                                          [[[2., 2.], [2., 2.]],
                                                                           [[2., 2.], [2., 2.]],
                                                                           [[2., 2.], [2., 2.]]]],
                                                                         [[[[0., 0.], [0., 0.]],
                                                                           [[0., 0.], [0., 0.]],
                                                                           [[0., 0.], [0., 0.]]],
                                                                          [[[0., 0.], [0., 0.]],
                                                                           [[0., 0.], [0., 0.]],
                                                                           [[0., 0.], [0., 0.]]]]]))
        npt.assert_almost_equal(sv_compras.get_data(), np.array([[[[1., 1.], [1., 1.]],
                                                                  [[1., 1.], [1., 1.]],
                                                                  [[1., 1.], [1., 1.]]],
                                                                 [[[1., 1.], [1., 1.]],
                                                                  [[1., 1.], [1., 1.]],
                                                                  [[1., 1.], [1., 1.]]]]))
        npt.assert_almost_equal(sv_devoluciones.get_data(), np.array([[[[[0.2, 0.8], [0.2, 0.8]],
                                                                        [[0.2, 0.8], [0.2, 0.8]],
                                                                        [[0.2, 0.8], [0.2, 0.8]]],
                                                                       [[[0.6, 0.4], [0.6, 0.4]],
                                                                        [[0.6, 0.4], [0.6, 0.4]],
                                                                        [[0.6, 0.4], [0.6, 0.4]]]],
                                                                      [[[[0.1, 0.9], [0.1, 0.9]],
                                                                        [[0.1, 0.9], [0.1, 0.9]],
                                                                        [[0.1, 0.9], [0.1, 0.9]]],
                                                                       [[[0.7, 0.3], [0.7, 0.3]],
                                                                        [[0.7, 0.3], [0.7, 0.3]],
                                                                        [[0.7, 0.3], [0.7, 0.3]]]]]))
        npt.assert_almost_equal(sv_target_venta.get_data(), np.array([[[[[1.4, 5.6], [1.4, 5.6]],
                                                                        [[1.4, 5.6], [1.4, 5.6]],
                                                                        [[1.4, 5.6], [1.4, 5.6]]],
                                                                       [[[4.2, 2.8], [4.2, 2.8]],
                                                                        [[4.2, 2.8], [4.2, 2.8]],
                                                                        [[4.2, 2.8], [4.2, 2.8]]]],
                                                                      [[[[0.7, 6.3], [0.7, 6.3]],
                                                                        [[0.7, 6.3], [0.7, 6.3]],
                                                                        [[0.7, 6.3], [0.7, 6.3]]],
                                                                       [[[4.9, 2.1], [4.9, 2.1]],
                                                                        [[4.9, 2.1], [4.9, 2.1]],
                                                                        [[4.9, 2.1], [4.9, 2.1]]]]]))
        npt.assert_almost_equal(sv_projection_eom_stock.get_data(), np.array([[[[[1.8, -0.8], [3.8,  1.2]],
                                                                                [[5.8,  3.2], [7.8,  5.2]],
                                                                                [[9.8,  7.2], [11.8,  9.2]]],
                                                                               [[[11.4, 13.6], [13.4, 15.6]],
                                                                                [[15.4, 17.6], [17.4, 19.6]],
                                                                                [[19.4, 21.6], [21.4, 23.6]]]],
                                                                              [[[[2.2, -5.2], [4.2, -3.2]],
                                                                                [[6.2, -1.2], [8.2,  0.8]],
                                                                                [[10.2,  2.8], [12.2,  4.8]]],
                                                                               [[[8.2, 12.8], [10.2, 14.8]],
                                                                                [[12.2, 16.8], [14.2, 18.8]],
                                                                                [[16.2, 20.8], [18.2, 22.8]]]]]))
        npt.assert_almost_equal(sv_target_stock.get_data(), np.array([[[[[1.575, 8.925], [1.575, 8.925]],
                                                                        [[1.575, 8.925], [1.575, 8.925]],
                                                                        [[1.575, 8.925], [1.575, 8.925]]],
                                                                       [[[6.825, 3.675], [6.825, 3.675]],
                                                                        [[6.825, 3.675], [6.825, 3.675]],
                                                                        [[6.825, 3.675], [6.825, 3.675]]]],
                                                                      [[[[1.05,  9.45], [1.05,  9.45]],
                                                                        [[1.05,  9.45], [1.05,  9.45]],
                                                                        [[1.05,  9.45], [1.05,  9.45]]],
                                                                       [[[7.35,  3.15], [7.35,  3.15]],
                                                                        [[7.35,  3.15], [7.35,  3.15]],
                                                                        [[7.35,  3.15], [7.35,  3.15]]]]]
                                                                     ))
        npt.assert_almost_equal(sv_absolute_otb.get_data(), np.array([[[[[0.225,  -9.725], [2.225,  -7.725]],
                                                                        [[4.225,  -5.725], [6.225,  -3.725]],
                                                                        [[8.225,  -1.725], [10.225,   0.275]]],
                                                                       [[[4.575,   9.925], [6.575,  11.925]],
                                                                        [[8.575,  13.925], [10.575,  15.925]],
                                                                        [[12.575,  17.925], [14.575,  19.925]]]],
                                                                      [[[[1.15,  -14.65], [3.15,  -12.65]],
                                                                        [[5.15,  -10.65], [7.15,   -8.65]],
                                                                        [[9.15,   -6.65], [11.15,   -4.65]]],
                                                                       [[[0.85,    9.65], [2.85,   11.65]],
                                                                        [[4.85,   13.65], [6.85,   15.65]],
                                                                        [[8.85,   17.65], [10.85,   19.65]]]]]))

        npt.assert_almost_equal(sv_percentage_otb.get_data(), np.array([[[[[14.28571429, -108.96358543],
                                                                           [141.26984127,  -86.55462185]],
                                                                          [[268.25396825,  -64.14565826],
                                                                           [395.23809524,  -41.73669468]],
                                                                          [[522.22222222,  -19.32773109],
                                                                           [649.20634921,    3.08123249]]],
                                                                         [[[67.03296703,  270.06802721],
                                                                           [96.33699634,  324.48979592]],
                                                                          [[125.64102564,  378.91156463],
                                                                           [154.94505495,  433.33333333]],
                                                                          [[184.24908425,  487.75510204],
                                                                           [213.55311355,  542.17687075]]]],
                                                                        [[[[109.52380952, -155.02645503],
                                                                           [300,         -133.86243386]],
                                                                          [[490.47619048, -112.6984127],
                                                                           [680.95238095,  -91.53439153]],
                                                                          [[871.42857143,  -70.37037037],
                                                                           [1061.9047619,   -49.20634921]]],
                                                                         [[[11.56462585,  306.34920635],
                                                                           [38.7755102,  369.84126984]],
                                                                          [[65.98639456,  433.33333333],
                                                                           [93.19727891,  496.82539683]],
                                                                          [[120.40816327,  560.31746032],
                                                                           [147.61904762,  623.80952381]]]]]))


if __name__ == '__main__':
    unittest.main()
