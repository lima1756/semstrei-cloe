import unittest
from app.libs.otb.super_vector import Dimension, SuperVector, Header
import app.libs.otb.otb_module as otb_functions
import numpy as np
import numpy.testing as npt


class TestSuperVector(unittest.TestCase):

    def setUp(self):
        self._dimension_11 = Dimension(
            "WarnerBrothers", ["Yakko", "Wakko", "Dot"])
        self._dimension_12 = Dimension(
            "Colors", ("Red", "Blue", "Green", "Yellow"))
        self._dimension_13 = Dimension(
            "Fruits", ["Pear", "Orange", "Pineapple"])
        self._dimension_14 = Dimension("Temperature", ["Cold", "Hot"])

        self._header_1 = Header(
            "Kids Data",  [self._dimension_11, self._dimension_12])
        self._header_1_expanded = Header(
            "Kids Data",  [self._dimension_13, self._dimension_11, self._dimension_12])
        self._header_3 = Header(
            "Kids Data", [self._dimension_11, self._dimension_12, self._dimension_13])
        self._header_4 = Header(
            "Control 4 dim", [self._dimension_11, self._dimension_12, self._dimension_13, self._dimension_14])
        self._header_5 = Header(
            "Control 5 dim", [self._dimension_11, self._dimension_12, self._dimension_14])

        self._super_vector_1 = SuperVector(
            self._header_1, np.arange(12).reshape(3, 4))
        self._super_vector_2 = SuperVector(
            self._header_1, np.arange(12, 24).reshape(3, 4))
        self._super_vector_3 = SuperVector(self._header_1, np.array(
            [[1, 2, 4, 0], [2, 4, 8, -10], [3, 6, 12, 34]]))
        self._super_vector_4 = SuperVector(self._header_1, np.array(
            [[0, 1, 2, 0], [1, 2, 3, 0], [2, 3, 4, 10]]))
        self._super_vector_5 = SuperVector(
            self._header_3, np.arange(3 * 4 * 3).reshape((3, 4, 3,)))
        self._super_vector_6 = SuperVector(self._header_4, np.array(
            [[[0., 1.], [1., 3.],
              [.5, .5], [1., 1.]],
             [[1., 2.], [2., 6.],
              [.3, .3], [1., 2.]],
             [[2., 4.], [4., 12.],
              [.7, .7], [1., 3.]]]))
        self._super_vector_7 = SuperVector(self._header_5, np.array(
            [[[0., 1.], [1., 3.],
              [.5, .5], [1., 1.]],
             [[1., 2.], [2., 6.],
              [.3, .3], [1., 2.]],
             [[2., 4.], [4., 12.],
              [.7, .7], [1., 3.]]]))

    def test_join_super_vector_with_category(self):
        sv_con_extra_dim = otb_functions.join_super_vector_with_category(
            self._super_vector_5, self._super_vector_7, use_3rd_dim_for_join=False)
        new_header = Header(
            "", [self._dimension_11, self._dimension_12, self._dimension_13, self._dimension_14])
        self.assertEqual(new_header, sv_con_extra_dim.get_header())
        npt.assert_almost_equal(sv_con_extra_dim.get_data(), [[[[0.,   0.],
                                                                [0., 1.],
                                                                [0., 2.]],
                                                               [[3., 9.],
                                                                [4., 12.],
                                                                [5., 15.]],
                                                               [[3., 3.],
                                                                [3.5, 3.5],
                                                                [4., 4.]],
                                                               [[9., 9.],
                                                                [10., 10.],
                                                                [11., 11.]]],
                                                              [[[12., 24.],
                                                                [13., 26.],
                                                                [14., 28.]],
                                                               [[30., 90.],
                                                                [32., 96.],
                                                                [34., 102.]],
                                                               [[5.4, 5.4],
                                                                [5.7, 5.7],
                                                                [6., 6.]],
                                                               [[21., 42.],
                                                                [22., 44.],
                                                                [23., 46.]]],
                                                              [[[48., 96.],
                                                                [50., 100.],
                                                                [52., 104.]],
                                                               [[108., 324.],
                                                                [112., 336.],
                                                                [116., 348.]],
                                                               [[21., 21.],
                                                                [21.7, 21.7],
                                                                [22.4, 22.4]],
                                                               [[33., 99.],
                                                                [34., 102.],
                                                                [35., 105.]]]])

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
        sv_new_dimension = otb_functions.get_inventario_piso_por_periodo(
            self._super_vector_1, self._dimension_13)

        # Test Header was properly changed
        self.assertEqual(sv_new_dimension.get_header(),
                         self._header_1_expanded)

        # Test Data was added dimension in the proper place.
        npt.assert_almost_equal(sv_new_dimension.get_data(),
                                np.array([np.arange(12).reshape(shape),
                                          np.zeros(shape),
                                          np.zeros(shape)]))

    def test_get_percentage_otb(self):
        sv_percentage_otb = otb_functions.get_percentage_otb(
            self._super_vector_3, self._super_vector_4)
        npt.assert_almost_equal(sv_percentage_otb.get_data(), (100*np.array([[0, 2, 2, 0], [2, 2, (8/3), 0],
                                                                             [1.5, 2, 3, 3.4]])))

    def test_get_absolute_otb(self):
        shape = self._super_vector_1.get_data().shape
        sv_test_percentage_otb = otb_functions.get_absolute_otb(
            self._super_vector_2, self._super_vector_1)
        self.assertEqual(sv_test_percentage_otb.get_header(),
                         self._super_vector_2.get_header())
        npt.assert_almost_equal(
            sv_test_percentage_otb.get_data(), (-12 * np.ones(shape)))

    def test_get_target_stock(self):
        test_target_stock = otb_functions.get_target_stock(
            self._super_vector_3, 1.5)
        self.assertEqual(test_target_stock.get_header(),
                         self._super_vector_3.get_header())
        npt.assert_almost_equal(test_target_stock.get_data(), np.array([[3.75, 7.5, 15, 18],
                                                                        [4.5, 9, 18, 51],
                                                                        [4.5, 9, 18, 51]]))

    def test_get_data_projection_eom_stock_for_period(self):
        sv_stock_inicial_por_periodo = SuperVector(
            self._header_3, 2 * np.ones((3, 4, 3)))
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

    def test_with_real_data(self):
        time_dimension = Dimension("Tiempo", ["Agosto", "Septiembre", "Octubre"])
        une_dimension = Dimension("Une", ["Bolso", "Billetera", "Calzado"])
        mercado_dimension = Dimension("Mercado", ["M1", "M2"])
        categoria_dimension = Dimension("Categoria", ["Basico", "Moda"])
        tumc = [time_dimension, une_dimension, mercado_dimension, categoria_dimension]
        tuc = [time_dimension, une_dimension,categoria_dimension]
        umc = tumc[1:]
        tum = [time_dimension, une_dimension, mercado_dimension]
        tu = [time_dimension, une_dimension]
        # Header( "Header", tumc)
        sv_stock_inicial = SuperVector(
            Header("Stock Inicial", umc), np.array([[[4429, 82487], [7, 10768]],
                                                    [[3089, 31907], [910, 998]],
                                                    [[5672, 22310], [1671, 10394]]]))
        sv_inventario_piso = SuperVector(
            Header("Inventario Piso", umc), np.array([[[19, 14730], [0, 22756]],
                                                      [[89, 5065], [0, 2831]],
                                                      [[1, 6919], [0, 10678]]]))
        sv_compras = SuperVector(
                Header("Compras", tumc), np.array([[[[0, 1843], [0, 104]],
                                                    [[0, 0], [0, 0]],
                                                    [[0, 4302], [0, 135]]],

                                                   [[[0, 24392], [0, 3474]],
                                                    [[0, 5651], [0, 806]],
                                                    [[0, 6912], [0, 981]]],

                                                   [[[2216, 18104], [0, 3729]],
                                                    [[4534, 8703], [0, 691]],
                                                    [[8676, 3076], [0, 193]]]
                                                   ]))
        sv_devoluciones_general = SuperVector(
            Header("Devoluciones", tu), np.array([[2804, 423, 1218], [1082, 389, 821], [1205, 383, 716]]))
        sv_rate_control_moda_basico = SuperVector(Header("Control Basico Moda", tuc),
                                                  np.array([[[0.08, 0.92], [.2, .8], [.3, .7]],
                                                            [[0.08, 0.92], [.2, .8], [.3, .7]],
                                                            [[0.08, 0.92], [.2, .8], [.3, .7]]]))

        sv_plan_ventas_general = SuperVector(
            Header("Plan Ventas", tum), np.array([[[17847, 4885], [4736, 1031], [5123, 1392]],
                                                  [[30227, 5330], [8575, 1009], [7895, 1169]],
                                                  [[35288, 5463], [10314, 1112], [9967, 1494]]]))
        # pdb.set_trace()
        otb_output = otb_functions.calculate_otb(sv_stock_inicial, sv_inventario_piso, sv_compras,
                                                 sv_devoluciones_general, sv_plan_ventas_general,
                                                 sv_rate_control_moda_basico, time_dimension, 1.5,
                                                 use_submarca_for_real_cases=False)
        sv_stock_inicial = otb_output[0]
        sv_inventario_piso = otb_output[1]
        sv_compras = otb_output[2]
        sv_devoluciones = otb_output[3]
        sv_target_venta = otb_output[4]
        sv_projection_eom_stock = otb_output[5]
        sv_target_stock = otb_output[6]
        sv_absolute_otb = otb_output[7]
        sv_percentage_otb = otb_output[8]

        npt.assert_almost_equal(sv_inventario_piso.get_data().astype(np.int64),
                                np.array([[[[19, 14730], [0, 22756]],
                                           [[89, 5065], [0, 2831]],
                                           [[1, 6919], [0, 10678]]],
                                          [[[0, 0], [0, 0]],
                                           [[0, 0], [0, 0]],
                                           [[0, 0], [0, 0]]],
                                          [[[0, 0], [0, 0]],
                                           [[0, 0], [0, 0]],
                                           [[0, 0], [0, 0]]]]))

        npt.assert_almost_equal(sv_devoluciones.get_data().astype(np.int64), np.array([[[[0,    0],
                                                                                         [224, 2579]],
                                                                                        [[0,    0],
                                                                                         [84,  338]],
                                                                                        [[0,    0],
                                                                                         [365,  852]]],
                                                                                       [[[0,    0],
                                                                                         [86,  995]],
                                                                                        [[0,    0],
                                                                                         [77,  311]],
                                                                                        [[0,    0],
                                                                                         [246,  574]]],
                                                                                       [[[0,    0],
                                                                                         [96, 1108]],
                                                                                        [[0,    0],
                                                                                         [76,  306]],
                                                                                        [[0,    0],
                                                                                         [214,  501]]]]))

        npt.assert_almost_equal(sv_target_venta.get_data().astype(np.int64), np.array([[[[1427, 16419],
                                                                                         [0,  4885]],
                                                                                        [[947,  3788],
                                                                                         [0,  1031]],
                                                                                        [[1536,  3586],
                                                                                         [0,  1392]]],
                                                                                       [[[2418, 27808],
                                                                                         [0,  5330]],
                                                                                        [[1715,  6860],
                                                                                         [0, 1009]],
                                                                                        [[2368,  5526],
                                                                                         [0,  1169]]],
                                                                                       [[[2823, 32464],
                                                                                         [0,  5463]],
                                                                                        [[2062,  8251],
                                                                                         [0,      1112]],
                                                                                        [[2990,  6976],
                                                                                         [0,  1494]]]]))

        npt.assert_almost_equal(sv_compras.get_data().astype(np.int64), np.array([[[[0, 1843], [0, 104]],
                                                                                   [[0, 0], [0, 0]],
                                                                                   [[0, 4302], [0, 135]]],
                                                                                  [[[0, 24392], [0, 3474]],
                                                                                   [[0, 5651], [0, 806]],
                                                                                   [[0, 6912], [0, 981]]],
                                                                                  [[[2216, 18104], [0, 3729]],
                                                                                   [[4534, 8703], [0, 691]],
                                                                                   [[8676, 3076], [0, 193]]]]))

        npt.assert_almost_equal(sv_projection_eom_stock.get_data().astype(np.int64)[:1, ...],
                                np.array([[[[3020, 82640],
                                            [231, 31322]],
                                           [[2230, 33183],
                                            [994, 3136]],
                                           [[4136, 29944],
                                            [2036, 20667]]]]))

        npt.assert_almost_equal(sv_stock_inicial.get_data().astype(np.int64)[:2, ...], np.array([[[[4429, 82487],
                                                                                                   [7, 10768]],
                                                                                                  [[3089, 31907],
                                                                                                   [910, 998]],
                                                                                                  [[5672, 22310],
                                                                                                   [1671, 10394]]],
                                                                                                 [[[3020, 82640],
                                                                                                   [231, 31322]],
                                                                                                  [[2230, 33183],
                                                                                                   [994, 3136]],
                                                                                                  [[4136, 29944],
                                                                                                   [2036, 20667]]]]))

        npt.assert_almost_equal(sv_absolute_otb.get_data().astype(np.int64)[:1, ...], np.array([[[[910, -37435],
                                                                                                  [-231, -23227]],
                                                                                                 [[602, -21849],
                                                                                                  [-994, -1545]],
                                                                                                 [[-117, -20567],
                                                                                                  [-2036, -18670]]]]
                                                                                               ))

        npt.assert_almost_equal(sv_target_stock.get_data().astype(np.int64)[:1, ...], np.array([[[[3930, 45205],
                                                                                                  [0, 8094]],
                                                                                                 [[2833, 11333],
                                                                                                  [0, 1590]],
                                                                                                 [[4018, 9377],
                                                                                                  [0, 1997]]]]))

        npt.assert_almost_equal(sv_percentage_otb.get_data().astype(np.int64)[:1, ...], np.array([[[[23,  -82],
                                                                                                    [0, -286]],
                                                                                                   [[21, -192],
                                                                                                    [0, -97]],
                                                                                                   [[-2, -219],
                                                                                                    [0, -934]]]]))


if __name__ == '__main__':
    unittest.main()
