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
        self._header_2 = Header("Kids Data",  [self._dimension_11, self._dimension_12])

        self._header_3 = Header("Kids Data", [self._dimension_11, self._dimension_12, self._dimension_13])
        self._header_4 = Header("Control 4 dim",  [self._dimension_11, self._dimension_14])
        self._header_5 = Header("Kids Data", [self._dimension_12, self._dimension_11])

        self._header_1_expanded = Header("Kids Data",  [self._dimension_13, self._dimension_11, self._dimension_12])

        self._super_vector_1 = SuperVector(self._header_1, np.arange(12).reshape(3, 4))
        self._super_vector_2 = SuperVector(self._header_2, np.arange(12, 24).reshape(3, 4))

        self._super_vector_3 = SuperVector(self._header_1, np.array([[1, 2, 4, 0], [2, 4, 8, -10], [3, 6, 12, 34]]))
        self._super_vector_4 = SuperVector(self._header_2, np.array([[0, 1, 2, 0], [1, 2, 3, 0], [2, 3, 4, 10]]))

        self._super_vector_5 = SuperVector(self._header_2, np.arange(3 * 4).reshape(3, 4))
        self._super_vector_6 = SuperVector(self._header_4, np.array([[2,  3], [4, 6], [8,  9]]))
        self._super_vector_7 = SuperVector(self._header_5, np.arange(3 * 4).reshape(4, 3))

    def test_get_vector_con_moda_basico(self):
        sv_con_extra_dim = otb_functions.get_vector_con_moda_basico(self._super_vector_5, self._super_vector_6)
        new_header = Header("", [self._dimension_11, self._dimension_12, self._dimension_14])
        self.assertEqual(new_header, sv_con_extra_dim.get_header())
        npt.assert_almost_equal(sv_con_extra_dim.get_data(), [[[0, 0], [2, 3], [4, 6], [6, 9]],
                                                              [[16, 24], [20, 30], [24, 36], [28, 42]],
                                                              [[64, 72], [72, 81], [80, 90], [88, 99]]])

        sv_con_extra_dim_2 = otb_functions.get_vector_con_moda_basico(self._super_vector_7, self._super_vector_6)
        new_header_2 = Header("", [self._dimension_12, self._dimension_11,  self._dimension_14])
        self.assertEqual(new_header_2, sv_con_extra_dim_2.get_header())
        npt.assert_almost_equal(sv_con_extra_dim_2.get_data(), [[[0, 0], [4, 6], [16, 18]],
                                                                [[6, 9], [16, 24], [40, 45]],
                                                                [[12, 18], [28, 42], [64, 72]],
                                                                [[18, 27], [40, 60], [88, 99]]])

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
        """
        calculate_otb(sv_stock_inicial, sv_inventario_piso, sv_compras, sv_devoluciones_general,
                      sv_plan_ventas_general, sv_rate_control_moda_basico, time_dimension) :
                      (sv_stock_inicial, sv_inventario_piso, sv_compras, sv_devoluciones, sv_target_venta,
                      sv_projection_eom_stock, sv_target_stock, sv_absolute_otb, sv_percentage_otb)

        Es la funcion principal, que calcula todas las variables necesarias para el OTB.
        Inputs:
        sv_stock_inicial: SuperVector, Stock Inicial, (U,S,M,C)
        sv_inventario_piso: SuperVector, Inventario Piso, (U,S,M,C)
        sv_compras: SuperVector, Compras, (T,U,S,M,C)
        sv_devoluciones_general: SuperVector, Devoluciones ( Moda + Basico), (T,U,S,M)
        sv_plan_ventas_general: SuperVector, Plan_Ventas (Moda + Basico), (T,U,S,M)
        sv_rate_control_moda_basico: SuperVector, Tabla de Control Moda Basico por Une, (U,C)

        OUTPUT:
        Tupla con super vectores con cada variable de salida para el OTB.
                      (sv_stock_inicial, sv_inventario_piso, sv_compras, sv_devoluciones, sv_target_venta,
                      sv_projection_eom_stock, sv_target_stock, sv_absolute_otb, sv_percentage_otb)
        Cada superVector de Salida tiene dimensiones (T,U,S,M,C).
        """
        time_dimension = Dimension("Tiempo", ["Hoy", "Prox Semana"])
        une_dimension = Dimension("Une", ["Bolsas", "Monederos"])
        submarca_dimension = Dimension("Submarca", ["Mujer", "Hombre", "Niños"])
        mercado_dimension = Dimension("Mercado", ["M1", "M2"])
        categoria_dimension = Dimension("Categoria", ["Moda", "Basico"])
        tusmc = [time_dimension, une_dimension, submarca_dimension, mercado_dimension, categoria_dimension]
        uc = [une_dimension, categoria_dimension]
        usmc = tusmc[1:]
        tusm = [time_dimension, une_dimension, submarca_dimension, mercado_dimension]
        # Header( "Header", tusmc)
        sv_stock_inicial = SuperVector(Header("Stock Inicial", usmc), np.arange(24).reshape(2, 3, 2, 2))
        sv_inventario_piso = SuperVector(Header("Inventario Piso", usmc),  2 * np.ones((2, 3, 2, 2,)))
        sv_compras = SuperVector(Header("Compras", tusmc),   np.ones((2, 3, 2, 2,)))
        sv_devoluciones_general = SuperVector(Header("Devoluciones", tusm), np.ones((2, 2, 3, 2,)))
        sv_plan_ventas_general = SuperVector(Header("Plan Ventas", tusm), 7 * np.ones((2, 2, 3, 2,)))
        sv_rate_control_moda_basico = SuperVector(Header("Control Moda Basico", uc),
                                                  np.array([[0.1, 0.9], [0.7, 0.3]]))
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
                                                           [[[[2.4, -1.4], [4.4, 0.6]],
                                                             [[6.4,  2.6], [8.4, 4.6]],
                                                             [[10.4,  6.6], [12.4, 8.6]]],
                                                            [[[10.8, 14.2], [12.8, 16.2]],
                                                             [[14.8, 18.2], [16.8, 20.2]],
                                                             [[18.8, 22.2], [20.8, 24.2]]]]]))
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
        npt.assert_almost_equal(sv_devoluciones.get_data(), np.array([[[[[0.1, 0.9], [0.1, 0.9]],
                                                            [[0.1, 0.9], [0.1, 0.9]],
                                                            [[0.1, 0.9], [0.1, 0.9]]],
                                                           [[[0.7, 0.3], [0.7, 0.3]],
                                                            [[0.7, 0.3], [0.7, 0.3]],
                                                            [[0.7, 0.3], [0.7, 0.3]]]],
                                                          [[[[0.1, 0.9], [0.1, 0.9]],
                                                            [[0.1, 0.9], [0.1, 0.9]],
                                                            [[0.1, 0.9], [0.1, 0.9]]],
                                                           [[[0.7, 0.3], [0.7, 0.3]],
                                                            [[0.7, 0.3], [0.7, 0.3]],
                                                            [[0.7, 0.3], [0.7, 0.3]]]]]))
        npt.assert_almost_equal(sv_target_venta.get_data(), np.array([[[[[0.7, 6.3], [0.7, 6.3]],
                                                            [[0.7, 6.3], [0.7, 6.3]],
                                                            [[0.7, 6.3], [0.7, 6.3]]],
                                                           [[[4.9, 2.1], [4.9, 2.1]],
                                                            [[4.9, 2.1], [4.9,  2.1]],
                                                            [[4.9, 2.1], [4.9, 2.1]]]],
                                                          [[[[0.7, 6.3], [0.7, 6.3]],
                                                            [[0.7, 6.3], [0.7, 6.3]],
                                                            [[0.7, 6.3], [0.7, 6.3]]],
                                                           [[[4.9, 2.1], [4.9, 2.1]],
                                                            [[4.9, 2.1], [4.9,  2.1]],
                                                            [[4.9, 2.1], [4.9, 2.1]]]]]))
        npt.assert_almost_equal(sv_projection_eom_stock.get_data(), np.array(
            [[[[[2.4, -1.4], [4.4,  0.6]],
               [[6.4,  2.6], [8.4,  4.6]],
               [[10.4,  6.6], [12.4,   8.6]]],
              [[[10.8, 14.2], [12.8, 16.2]],
               [[14.8, 18.2], [16.8, 20.2]],
               [[18.8, 22.2], [20.8, 24.2]]]],
             [[[[2.8, -5.8], [4.8, -3.8]],
               [[6.8, - 1.8], [8.8,  0.2]],
               [[10.8,  2.2], [12.8, 4.2]]],
              [[[7.6, 13.4], [9.6, 15.4]],
               [[11.6, 17.4], [13.6, 19.4]],
               [[15.6, 21.4], [17.6, 23.4]]]]]))
        npt.assert_almost_equal(sv_target_stock.get_data(), np.array([[[[[1.05, 9.45], [1.05, 9.45]],
                                                            [[1.05, 9.45], [1.05, 9.45]],
                                                            [[1.05, 9.45], [1.05, 9.45]]],
                                                           [[[7.35, 3.15], [7.35, 3.15]],
                                                            [[7.35, 3.15], [7.35, 3.15]],
                                                            [[7.35, 3.15], [7.35, 3.15]]]],
                                                          [[[[1.05, 9.45], [1.05, 9.45]],
                                                            [[1.05, 9.45], [1.05, 9.45]],
                                                            [[1.05, 9.45], [1.05, 9.45]]],
                                                           [[[7.35, 3.15], [7.35, 3.15]],
                                                            [[7.35, 3.15], [7.35, 3.15]],
                                                            [[7.35, 3.15], [7.35, 3.15]]]]]))
        npt.assert_almost_equal(sv_absolute_otb.get_data(), np.array([[[[[1.35, -10.85], [3.35, -8.85]],
                                                            [[5.35, -6.85], [7.35, -4.85]],
                                                            [[9.35, -2.85], [11.35, -0.85]]],
                                                           [[[3.45, 11.05], [5.45, 13.05]],
                                                            [[7.45, 15.05], [9.45, 17.05]],
                                                            [[11.45, 19.05], [13.45, 21.05]]]],
                                                          [[[[1.75, -15.25], [3.75, -13.25]],
                                                            [[5.75, -11.25], [7.75, -9.25]],
                                                            [[9.75, -7.25], [11.75, -5.25]]],
                                                           [[[0.25,  10.25], [2.25,  12.25]],
                                                            [[4.25,  14.25], [6.25,  16.25]],
                                                            [[8.25,  18.25], [10.25,  20.25]]]]]))
        npt.assert_almost_equal(sv_percentage_otb.get_data(), np.array(
            [[[[[128.57142857, - 114.81481481], [319.04761905, - 93.65079365]],
               [[509.52380952, - 72.48677249], [700., - 51.32275132]],
               [[890.47619048, - 30.15873016], [1080.95238095, - 8.99470899]]],
              [[[46.93877551,  350.79365079], [74.14965986,  414.28571429]],
               [[101.36054422,  477.77777778], [128.57142857,  541.26984127]],
               [[155.78231293, 604.76190476], [182.99319728, 668.25396825]]]],
             [[[[166.66666667, -161.37566138], [357.14285714, -140.21164021]],
               [[547.61904762, -119.04761905], [738.0952381, -97.88359788]],
               [[928.57142857, -76.71957672], [1119.04761905, -55.55555556]]],
              [[[3.40136054,  325.3968254], [30.6122449,   388.88888889]],
               [[57.82312925, 452.38095238], [85.03401361,  515.87301587]],
               [[112.24489796, 579.36507937], [139.45578231, 642.85714286]]]]]))


if __name__ == '__main__':
    unittest.main()
