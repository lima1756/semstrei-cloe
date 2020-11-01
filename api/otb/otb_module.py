import numpy as np
from otb.super_vector import SuperVector, Header, Dimension
from copy import deepcopy


def insert_dimension_to_shape(old_shape, index, dimension_shape):
    """Dada una tupla (shape) inserta un escalar en la tupla, para definir una nueva shape"""
    if type(index) is not int:
        return None
    if index > len(old_shape):  # If index is larger add last
        return old_shape + (dimension_shape,)
    if index < 0:  # If index is neg add first
        return (dimension_shape,) + old_shape
    return old_shape[:index] + (dimension_shape,) + old_shape[index:]


# TODO TOTEST TODOC
def get_vector_con_moda_basico(sv, sv_rate_control_moda_basico):
    """ (U,C) -- ( T, U,S, M) => ( T, U,S, C, M)
    control_shape = sv_rate_control_moda_basico.get_date().shape
    old_shape = sv.get_data().shape
    new_shape = insert_dimension_to_shape(old_shape, 3, control_shape[-1])
    # . . ."""
    pass


def get_inventario_piso_por_periodo(sv_inventario_piso, time_dimension):
    """ get_inventario_piso_por_periodo toma el super_vector inventario_piso (U,S,C,M) y le añade
        una dimension extra para representar Tiempo ( cada periodo a futuro). (T,U,S,C,M)
        Los datos origniales se cuardan en T=0.
        Para T>0,  la informacion permanece en zeros.
    """

    # Adding to header Time (T) dimension. (U,S,C,M) --> (T,U,S,C,M)
    inventario_piso_por_periodo_header = deepcopy(sv_inventario_piso.get_header())
    inventario_piso_por_periodo_header.insert_dimension(0, time_dimension)
    inventario_piso_por_periodo_header.set_vector_name("Inventario Piso por Periodo")

    # Getting new shape with dimension time added
    new_shape = insert_dimension_to_shape(sv_inventario_piso.get_data().shape, 0, len(time_dimension.get_categories()))

    # Create new data with Time dimension added. for T=0 we have the original data
    # For T>0, all data = 0
    inventario_piso_por_periodo_data = np.zeros(new_shape)
    inventario_piso_por_periodo_data[:1, :, :] = sv_inventario_piso.get_data()

    return SuperVector(inventario_piso_por_periodo_header, inventario_piso_por_periodo_data)


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

        # Make division, avoiding 0 in denominator
        percentage_otb_data = sv_absolute_otb.get_data() / sv_target_stock.get_data()
        percentage_otb_data *= 100
        percentage_otb_data = np.where(percentage_otb_data == np.inf, 0, percentage_otb_data)
        percentage_otb_data = np.where(percentage_otb_data == np.nan, 0, percentage_otb_data)

        return SuperVector(percentage_otb_header, percentage_otb_data)
    else:
        raise Exception("Super Vectors differs on type.")


# TODO TOTEST TODOC
"""
def calculate_otb(sv_stock_inicial, sv_inventario_piso, sv_compras, sv_devoluciones_general,
                  sv_plan_ventas_general, rate_control_moda_basico, time_dimension):
    sv_devoluciones = get_vector_con_moda_basico(sv_devoluciones_general, rate_control_moda_basico)

    sv_target_venta  = get_vector_con_moda_basico(sv_plan_ventas_general, rate_control_moda_basico)
    sv_target_stock = get_target_stock(sv_target_venta, 1.5)

    sv_inventario_piso = get_inventario_piso_por_periodo(sv_inventario_piso, time_dimension)

    ##############################################
    sv_stock_inicial_por_periodo = []
    sv_projection_eom_stock = get_projection_eom_stock(sv_stock_inicial_por_periodo, sv_inventario_piso,
                                                       sv_compras, sv_devoluciones, sv_target_venta)
    ############################################

    sv_absolute_otb = get_absolute_otb(sv_projection_eom_stock, sv_target_stock)
    sv_percentage_otb = get_percentage_otb(sv_absolute_otb, sv_target_stock)
"""
