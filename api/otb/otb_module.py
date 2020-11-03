import numpy as np
from otb.super_vector import SuperVector, Header, Dimension
from copy import deepcopy


def join_super_vector_with_category(sv, sv_rate_control_category):
    """
    Dado dos Supervectores:
        SV1(A, B, ... T,U, . . .,C,D . . .)  --- Con distintas dimensiones, conteniendo las dimensiones T,U
        sv_rate_control_category( T,U, ... ,  Z)  --- Teniendo como primeras dimensiones T,U
    se añade la dimension Z al vector SV1, uniendo ambos supervectores filtrando segun las dimensiones T, U.
    Para Los supervectores de target ventas y devoluciones:

    ( T, U,S, M) , (T,U,C) => ( T, U,S, M, C)
    Los datos de sv  se multiplican por  sv_rate_control_category, tomando su valor, segun las Dimensiones T,U.
    """

    # Get Dimension in common from both SuperVectors:
    index_join_dimension_1_on_sv = sv.get_index_dimension(sv_rate_control_category.get_dimensions()[0])
    index_join_dimension_2_on_sv = sv.get_index_dimension(sv_rate_control_category.get_dimensions()[1])
    if index_join_dimension_1_on_sv is None or index_join_dimension_2_on_sv is None:
        raise Exception("Vectors doesn't share common Dimension for joining.")

    # Get Old Shapes
    control_shape = sv_rate_control_category.get_data().shape
    data_old_shape = sv.get_data().shape

    # Get new header with new dimension
    new_header = deepcopy(sv.get_header())
    new_header.insert_dimension(len(data_old_shape), sv_rate_control_category.get_dimensions()[-1])

    # Get new data with Category dimension
    new_data = np.zeros(data_old_shape + (control_shape[-1],))

    # Reshape Control for Make it able of multiply with the main Super Vector
    reshape_control_for_multiplication = (1,) * len(data_old_shape)
    reshape_control_for_multiplication = reshape_control_for_multiplication[:index_join_dimension_1_on_sv] \
        + (control_shape[0],) \
        + reshape_control_for_multiplication[index_join_dimension_1_on_sv+1:]\
        + (control_shape[-1],)
    reshape_control_for_multiplication = reshape_control_for_multiplication[:index_join_dimension_2_on_sv] \
        + (control_shape[1],) \
        + reshape_control_for_multiplication[index_join_dimension_2_on_sv + 1:]
    control = sv_rate_control_category.get_data().reshape(reshape_control_for_multiplication)

    # Make multiplication of SuperVector's data with control's reshaped data.
    new_data += sv.get_data().reshape(data_old_shape + (1,)) * control

    return SuperVector(new_header, new_data)


def insert_time_dimension(sv, time_dimension, new_header_name=None):
    """Dado un supervector, añade la dimension T como primera dimension.
        (U,S,C,M) --> (T,U,S,C,M)
        Los datos originales quedan en T=0
        Las demas capas de T donde T!=0, los datos=0
    """

    # Adding to header Time (T) dimension to SuperVector. (U,S,C,M) --> (T,U,S,C,M)
    header_with_extra_dimension = deepcopy(sv.get_header())
    header_with_extra_dimension.insert_dimension(0, time_dimension)  # Insert first new Dimension.
    if new_header_name is not None:
        header_with_extra_dimension.set_vector_name(new_header_name)

    # Getting new shape with dimension time added
    new_shape = (len(time_dimension.get_categories()),) + sv.get_data().shape

    # Create new data with extra dimension (T) added.
    #   For T=0 we have the original data
    #   For T>0, all data = 0
    data_with_extra_dimension = np.zeros(new_shape)
    data_with_extra_dimension[:1, ...] = sv.get_data()

    return SuperVector(header_with_extra_dimension, data_with_extra_dimension)


def get_inventario_piso_por_periodo(sv_inventario_piso, time_dimension):
    """
    Get_inventario_piso_por_periodo toma el super_vector inventario_piso (U,S,C,M) y le añade
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
    Este promedio se multiplica por un factor escalar de incremento. (En el OTB original, el factor utilizado es 1.5)
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
    """
    Get absolute otb, calcula el OTB = proyeccion_eom_stock - sv_target_stock
    Requerido: proyeccion_eom_stock y sv_target_stock sean del mismo tipo de supervector.
    """
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


def get_data_projection_eom_stock_for_period(sv_initial_stock, sv_inventario_piso, sv_compras,
                                             sv_devoluciones, sv_target_venta, period):
    """
            Get Proyection EOM stock, for given Period t
            Result: sv_stock_inicial_por_periodo +  sv_inventario_piso + sv_compras +sv_devoluciones - sv_target_venta
            Requisites: sv_stock_inicial_por_periodo, sv_inventario_piso, sv_compras, sv_devoluciones,
             sv_target_venta should be the same type of supervector.
            Returns only data for EOM Stock in given period.
        """

    if sv_initial_stock.is_same_type(sv_inventario_piso) and \
            sv_initial_stock.is_same_type(sv_compras) and \
            sv_initial_stock.is_same_type(sv_devoluciones) and \
            sv_initial_stock.is_same_type(sv_target_venta):

        # Make Calculation for given period
        projection_eom_stock_by_period_data = sv_initial_stock.get_data()[period]\
            + sv_inventario_piso.get_data()[period] + sv_compras.get_data()[period]\
            + sv_devoluciones.get_data()[period] - sv_target_venta.get_data()[period]

        return projection_eom_stock_by_period_data
    else:
        raise Exception("Super Vectors differs on type.")


# TODOC
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

    # Get devolution by category ( Basico / Moda ) given the control table by season.
    sv_devoluciones = join_super_vector_with_category(sv_devoluciones_general, sv_rate_control_moda_basico)

    # Get target_venta by category (Moda/Basico) given the control table by season.
    sv_target_venta = join_super_vector_with_category(sv_plan_ventas_general, sv_rate_control_moda_basico)

    sv_target_stock = get_target_stock(sv_target_venta, 1.5)

    sv_inventario_piso = get_inventario_piso_por_periodo(sv_inventario_piso, time_dimension)

    # Calculation of Target EOM Stock, which is also the next period Initial stock.
    ########################################################
    t_period = len(time_dimension.get_categories())

    # Transformar Stock Inicial from (U,S,M,C) -->  (T,U,S,M,C)
    sv_stock_inicial = insert_time_dimension(sv_stock_inicial, time_dimension)
    # Get new Super Vector for EOM Stock
    eom_stock_header = deepcopy(sv_stock_inicial.get_header())
    eom_stock_header.set_vector_name("Projection EOM STOCK")
    sv_projection_eom_stock = SuperVector(eom_stock_header, np.zeros(sv_stock_inicial.get_data().shape))

    # Calculate Target EOM Stock for each period.
    for t in range(t_period):
        sv_projection_eom_stock.get_data()[t, ...] += get_data_projection_eom_stock_for_period(sv_stock_inicial,
                                                                                               sv_inventario_piso,
                                                                                               sv_compras,
                                                                                               sv_devoluciones,
                                                                                               sv_target_venta, t)
        if t < t_period - 1:
            # The present Target EOM Stock, is the initial stock for the next period.
            sv_stock_inicial.get_data()[t+1, ...] += sv_projection_eom_stock.get_data()[t, ...]
    ########################################################

    # Calculate OTB
    sv_absolute_otb = get_absolute_otb(sv_projection_eom_stock, sv_target_stock)
    sv_percentage_otb = get_percentage_otb(sv_absolute_otb, sv_target_stock)

    return (sv_stock_inicial, sv_inventario_piso, sv_compras,
            sv_devoluciones, sv_target_venta, sv_projection_eom_stock,
            sv_target_stock, sv_absolute_otb, sv_percentage_otb)
