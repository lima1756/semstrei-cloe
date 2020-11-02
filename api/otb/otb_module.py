import numpy as np
from otb.super_vector import SuperVector, Header, Dimension
from copy import deepcopy


def get_vector_con_moda_basico(sv, sv_rate_control_moda_basico):
    """ Dado un supervector SV1(A, B, ... U, . . .,C,D . . .) y el supervector sv_rate_control_moda_basico( U, ... ,  Z)
    se añade la dimension Z al vector SV1, uniendo ambos supervectores segun la dimension U.
    Los datos, se multiplican, filtrandose por la dimension U.
    Para Los supervectores de target ventas y devoluciones:

     ( T, U,S, M) , (U,C) => ( T, U,S, M, C)"""

    # Get Dimension in common:
    index_join_dimension_on_sv = sv.get_index_dimension(sv_rate_control_moda_basico.get_header().get_dimensions()[0])
    if index_join_dimension_on_sv is None:
        raise Exception("Vectors doesn't share common dimension for joining.")

    # Get Old Shapes
    control_shape = sv_rate_control_moda_basico.get_data().shape
    data_old_shape = sv.get_data().shape

    # Get new header with new dimension
    new_header = deepcopy(sv.get_header())
    new_header.insert_dimension(len(data_old_shape), sv_rate_control_moda_basico.get_header().get_dimensions()[-1])

    # Get new data with Category dimension
    new_data = np.zeros(data_old_shape + (control_shape[-1],))

    reshape_control_for_mult = (1,) * len(data_old_shape)
    reshape_control_for_mult = reshape_control_for_mult[:index_join_dimension_on_sv] + (control_shape[0],) \
        + reshape_control_for_mult[index_join_dimension_on_sv+1:] + (control_shape[1],)

    control = sv_rate_control_moda_basico.get_data().reshape(reshape_control_for_mult)
    new_data += sv.get_data().reshape(data_old_shape + (1,)) * control

    return SuperVector(new_header, new_data)


def insert_time_dimension(sv, time_dimension, new_header_name=None):
    """Dado un supervector, añade la dimension T como primera dimension.
        (U,S,C,M) --> (T,U,S,C,M)
        Los datos originales quedan en T=0
        Las demas capas de T donde T!=0, los datos=0
    """

    # Adding to header Time (T) dimension to SuperVector. (U,S,C,M) --> (T,U,S,C,M)
    sv_por_periodo_header = deepcopy(sv.get_header())
    sv_por_periodo_header.insert_dimension(0, time_dimension)
    if new_header_name is not None:
        sv_por_periodo_header.set_vector_name(new_header_name)

    # Getting new shape with dimension time added
    new_shape = (len(time_dimension.get_categories()),) + sv.get_data().shape

    # Create new data with Time dimension added. for T=0 we have the original data
    # For T>0, all data = 0
    sv_por_periodo_data = np.zeros(new_shape)
    sv_por_periodo_data[:1, ...] = sv.get_data()

    return SuperVector(sv_por_periodo_header, sv_por_periodo_data)


def get_inventario_piso_por_periodo(sv_inventario_piso, time_dimension):
    """ get_inventario_piso_por_periodo toma el super_vector inventario_piso (U,S,C,M) y le añade
        una dimension extra para representar Tiempo ( cada periodo a futuro). (T,U,S,C,M)
        Los datos origniales se cuardan en T=0.
        Para T>0,  la informacion permanece en zeros.
    """
    return insert_time_dimension(sv_inventario_piso, time_dimension, "Inventario Piso por Periodo")


def get_target_stock(sv_target_venta, increment_stock_factor):
    """
    Get Target Stock calcula el stock necesario estimado para los siguientes periodos.
    Para obtener el target del periodo T = t, es necesario promediar el Target_Venta del periodo mencionado t,
    y su periodo siguiente: t + 1.
    Este promedio se multiplica por un factor escalar de incremento.
    """
    shape = sv_target_venta.get_data().shape

    # Get new objects for super vector
    target_stock_header = deepcopy(sv_target_venta.get_header())
    target_stock_header.set_vector_name("Target Stock")
    target_stock_data = np.zeros(shape)
    last_period_index = len(target_stock_header.get_dimensions()[0].get_categories())

    # Calculate  target Stock for all periods.

    # Get average from present and next period
    for t in range(last_period_index - 1):
        # Calculate average this period and next one.
        target_stock_data[t] = (sv_target_venta.get_data()[t] + sv_target_venta.get_data()[t + 1]) / 2
    target_stock_data[last_period_index - 1] = sv_target_venta.get_data()[last_period_index - 1]

    # Multiply by the increment_factor
    target_stock_data *= increment_stock_factor

    return SuperVector(target_stock_header, target_stock_data)


def get_absolute_otb(sv_projection_eom_stock, sv_target_stock):
    if sv_projection_eom_stock.is_same_type(sv_target_stock):
        absolute_otb_header = deepcopy(sv_projection_eom_stock.get_header())
        absolute_otb_header.set_vector_name("OTB / CTB")
        absolute_otb_data = sv_projection_eom_stock.get_data() - sv_target_stock.get_data()
        return SuperVector(absolute_otb_header, absolute_otb_data)
    else:
        raise Exception("Super Vectors differs on type.")


def get_percentage_otb(sv_absolute_otb, sv_target_stock):
    """
        Get percentage otb calculates
        (otb / target-stock) * 100 %
        Requisites: sv_absolute_otb sv_target_stock should be the same type of supervector
    """

    if sv_absolute_otb.is_same_type(sv_target_stock):
        # Set Header for new entity
        percentage_otb_header = deepcopy(sv_absolute_otb.get_header())
        percentage_otb_header.set_vector_name("% OTB / CTB")

        # Make division
        percentage_otb_data = sv_absolute_otb.get_data() / sv_target_stock.get_data()
        # convert to percentage
        percentage_otb_data *= 100
        # Replacing all Inf and NaN values to 0
        percentage_otb_data[percentage_otb_data == -np.inf] = 0
        percentage_otb_data[percentage_otb_data == np.inf] = 0
        percentage_otb_data = np.nan_to_num(percentage_otb_data)

        return SuperVector(percentage_otb_header, percentage_otb_data)
    else:
        raise Exception("Super Vectors differs on type.")


# TOTEST
def get_data_projection_eom_stock_for_period(sv_stock_inicial_por_periodo, sv_inventario_piso, sv_compras,
                                             sv_devoluciones, sv_target_venta, periodo):
    """
            Get Proyection EOM stock, for given Period t
            Result: sv_stock_inicial_por_periodo +  sv_inventario_piso + sv_compras +sv_devoluciones - sv_target_venta
            Requisites: sv_stock_inicial_por_periodo, sv_inventario_piso, sv_compras, sv_devoluciones,
             sv_target_venta should be the same type of supervector.
            Returns only data for EOM Stock in given period.
        """

    if sv_stock_inicial_por_periodo.is_same_type(sv_inventario_piso) and \
            sv_stock_inicial_por_periodo.is_same_type(sv_compras) and \
            sv_stock_inicial_por_periodo.is_same_type(sv_devoluciones) and \
            sv_stock_inicial_por_periodo.is_same_type(sv_target_venta):

        # Make Calculation for given period
        projection_eom_stock_for_period_data = sv_stock_inicial_por_periodo.get_data()[periodo]\
            + sv_inventario_piso.get_data()[periodo] + sv_compras.get_data()[periodo]\
            + sv_devoluciones.get_data()[periodo] - sv_target_venta.get_data()[periodo]

        return projection_eom_stock_for_period_data
    else:
        raise Exception("Super Vectors differs on type.")


def calculate_otb(sv_stock_inicial, sv_inventario_piso, sv_compras, sv_devoluciones_general,
                  sv_plan_ventas_general, sv_rate_control_moda_basico, time_dimension):
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
    time_dimension: Dimension, Dimension que indica los periodos ( Presente y futuros) del OTB.

    OUTPUT:
    Tupla con super vectores con cada variable de salida para el OTB.
                  (sv_stock_inicial, sv_inventario_piso, sv_compras, sv_devoluciones, sv_target_venta,
                  sv_projection_eom_stock, sv_target_stock, sv_absolute_otb, sv_percentage_otb)
    Cada superVector de Salida tiene dimensiones (T,U,S,M,C).
    """

    # Obtencion devoluciones por Categoria (Moda/Basico) segun la tabla de control de estacionalidad.
    sv_devoluciones = get_vector_con_moda_basico(sv_devoluciones_general, sv_rate_control_moda_basico)

    # Obtencion target_venta por Categoria (Moda/Basico) segun la tabla de control de estacionalidad.
    sv_target_venta = get_vector_con_moda_basico(sv_plan_ventas_general, sv_rate_control_moda_basico)

    sv_target_stock = get_target_stock(sv_target_venta, 1.5)

    sv_inventario_piso = get_inventario_piso_por_periodo(sv_inventario_piso, time_dimension)

    # Calculo de la proyeccion eom stock, que tambien es considerada como el stock inicial del siguiente periodo.
    ########################################################
    t_periodos = len(time_dimension.get_categories())

    # Transformar Stock Inicial from (U,S,M,C) -->  (T,U,S,M,C)
    sv_stock_inicial = insert_time_dimension(sv_stock_inicial, time_dimension)
    # Get new Super Vector for EOM Stock
    eom_stock_header = deepcopy(sv_stock_inicial.get_header())
    eom_stock_header.set_vector_name("Projection EOM STOCK")
    sv_projection_eom_stock = SuperVector(eom_stock_header, np.zeros(sv_stock_inicial.get_data().shape))

    # Calcula el EOM Stock para cada periodo.
    for t in range(t_periodos):
        sv_projection_eom_stock.get_data()[t, ...] += get_data_projection_eom_stock_for_period(sv_stock_inicial,
                                                                                               sv_inventario_piso,
                                                                                               sv_compras,
                                                                                               sv_devoluciones,
                                                                                               sv_target_venta, t)
        if t < t_periodos - 1:
            # El EOM presente, es el stock inicial del siguiente periodo.
            sv_stock_inicial.get_data()[t+1, ...] += sv_projection_eom_stock.get_data()[t, ...]
    ########################################################

    # Calcula OTB
    sv_absolute_otb = get_absolute_otb(sv_projection_eom_stock, sv_target_stock)
    sv_percentage_otb = get_percentage_otb(sv_absolute_otb, sv_target_stock)

    return (sv_stock_inicial, sv_inventario_piso, sv_compras,
            sv_devoluciones, sv_target_venta, sv_projection_eom_stock,
            sv_target_stock, sv_absolute_otb, sv_percentage_otb)
