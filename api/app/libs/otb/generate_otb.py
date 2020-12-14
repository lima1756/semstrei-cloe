import pandas as pd
import numpy as np
from otb_module import calculate_otb
from app.libs.otb.super_vector import Dimension, SuperVector, Header
import datetime
from app.libs.oracle_cx import oracle_cx

oracle_connection = oracle_cx(
    username=os.getenv('DATABASE_ORACLE_USER', 'admin'),
    password=os.getenv('DATABASE_ORACLE_PASSWORD', 'password'),
    protocol='tcps',
    host='adb.us-ashburn-1.oraclecloud.com',
    port='1522',
    service_name=os.getenv('DATABASE_ORACLE_SERVICE',
                            'key_adb_high.adb.oraclecloud.com'),
)

connection = oracle_connection.get_oracle_default_connection(oracle_connection.tns_name)

def insert(args, i):
    conn = connection
    cursor = conn.cursor()
    print("starting", i)
    cursor.execute(args)
    conn.commit()

def delete_otb_results():
    conn = connection 
    cursor = conn.cursor()
    cursor.execute('DELETE FROM OTB_RESULTS')
    conn.commit()

def get_stock_factor():
    conn = connection 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM RATE_TARGET')
    stock_factor = 1.5
    for element in cursor:
        stock_factor = float(element[1])
        break
    return stock_factor

def insert_data():
    columns = '"numberCurrentPeriodOTB", "daysLongCurrentPeriodOTB", "startDateCurrentPeriodOTB", "isFutureProjection", "daysLongProjectionPeriodOTB", "startDateProjectionPeriodOTB", UNE, SUBMARCA, CATEGORIA, MERCADO, "initialStock", "inventoryOnStores", PURCHASES, DEVOLUTION, "targetSells", "targetStock", "projectionEomStock", OTB_MINUS_CTB, PERCENTAGE_OTB'
    #delete_otb_results()
    with open(f'./files/otb_output.csv') as current_file:
        i = 0
        for line in current_file:
            if i == 0:
                i+=1
                continue
            line = line.rstrip()
            line = line.split(',')
            line[2] = f"TO_DATE('{line[2]}', 'YYYY-MM-DD')"
            line[5] = f"TO_DATE('{line[5]}', 'YYYY-MM-DD')"
            for j in range(6,10):
                line[j] = f"'{line[j]}'"
            values = ','.join(str(e) for e in line)
            sent = f'INSERT INTO OTB_RESULTS ({columns}) VALUES ({values})'
            #insert(sent, i)
            print('Not actually inserted', i)
            i+=1

def generate_data():
    #TODO: Download this tables automatically
    stock_inicial = pd.read_csv('./files/stock_inicial_otb.csv')
    plan_ventas = pd.read_csv('./files/plan_ventas_otb.csv')
    inventario_piso = pd.read_csv('./files/inventario_piso_otb.csv')
    devoluciones = pd.read_csv('./files/devoluciones_otb.csv')
    compras = pd.read_csv('./files/compras_otb.csv')
    control_category = pd.read_csv('./files/control_category_otb.csv')
    item_details = pd.read_csv('./files/item_details.csv')

    new_format = []
    for date in compras['DATE']:
        new_format.append(date[:-2] + '01')
    compras['DATE'] = new_format

    new_format = []
    for date in control_category['DATE']:
        dt = date.split('-')
        if len(dt[1]) == 1:
            dt = dt[0] + '-' + '0' + dt[1] + '-' +dt[2]
        else:
            dt = date
        new_format.append(dt[:-2] + '01')
    control_category['DATE'] = new_format

    def set_position_categories(dimension):
        cats = dimension.get_categories()
        dic = {}
        for i in range(len(cats)):
            dic[cats[i]] = i
        return dic

    #Set up Dimensions
    dimensiones = {}
    def generate_dimensions(df):
        columnas = ['UNE','SUBMARCA', 'CATEGORIA']
        for columna in columnas:
            current_dim =  Dimension(columna, list(set(df[columna].to_list())))
            positions = set_position_categories(current_dim)
            dimensiones[columna] = [current_dim, positions]
        current_year = int(datetime.datetime.now().year)
        tiempo = pd.date_range(start=f"{current_year}-12-01",end=f"{current_year+2}-5-01", freq='MS') #TODO Update so it works on the begining of the year
        tiempo_dimension = Dimension('DATE', [date_obj.strftime('%Y-%m-%d') for date_obj in tiempo])
        tiempo_positions = set_position_categories(tiempo_dimension)
        dimensiones['DATE'] = [tiempo_dimension, tiempo_positions]
        current_dim = Dimension('MERCADO', ['M1', 'M2'])
        positions = set_position_categories(current_dim)
        dimensiones['MERCADO'] = [current_dim, positions]

    generate_dimensions(control_category)

    def get_data(df):
        #get shape and positions for each dimension of the df
        columnas = df.columns.to_list()[:-1]
        posiciones = []
        shape = []
        for columna in columnas:
            posiciones_columna = dimensiones[columna][1]
            posiciones.append(posiciones_columna)
            shape.append(len(posiciones_columna))
        data = np.zeros(shape)
        valores = df.values.tolist()

        for i in range(len(valores)):
            row = valores[i] #this is an array, each element corresponds to a column
            indexes = []
            found = True
            for j in range(0, len(row)-1): #last element is target value
                current_positions = posiciones[j]
                current_val = row[j]
                if current_val not in current_positions:
                    found = False
                    break
                target_position = current_positions[current_val]
                indexes.append(target_position)
            if not found:
                continue #check
            value = row[-1]
            data.__setitem__(tuple(indexes), value)
        return data

    def get_supervector(dfotb, nombre):
        columnas = dfotb.columns.to_list()[:-1]
        dimensiones_df = []
        for columna in columnas:
            dimensiones_df.append(dimensiones[columna][0])
        header = Header(nombre,  dimensiones_df)
        data = get_data(dfotb)
        sv = SuperVector(header, data)
        return sv

    sv_stock_inicial = get_supervector(stock_inicial, 'stock_inicial')
    sv_plan_ventas = get_supervector(plan_ventas, 'plan_ventas')
    sv_inventario_piso = get_supervector(inventario_piso, 'inventario_piso')
    sv_devoluciones = get_supervector(devoluciones , 'devoluciones')
    sv_control_category = get_supervector(control_category, 'control_category')
    sv_compras = get_supervector(compras, 'compras')
    time_dimension = dimensiones['DATE'][0]
    stock_factor = get_stock_factor()

    otb_output = calculate_otb(sv_stock_inicial, sv_inventario_piso, sv_compras, sv_devoluciones, sv_plan_ventas, sv_control_category, time_dimension, stock_factor)

    sv_stock_inicial = otb_output[0]
    sv_inventario_piso = otb_output[1]
    sv_compras = otb_output[2]
    sv_devoluciones = otb_output[3]
    sv_target_venta = otb_output[4]
    sv_projection_eom_stock = otb_output[5]
    sv_target_stock = otb_output[6]
    sv_absolute_otb = otb_output[7]
    sv_percentage_otb = otb_output[8]

    startDateProjectionPeriod = None
    rows = []
    for element in sv_stock_inicial.get_header():
        row = []
        startDateCurrentPeriodOTB, UNE, SUBMARCA, MERCADO, CATEGORIA = element
        if not startDateProjectionPeriod:
            startDateProjectionPeriod = startDateCurrentPeriodOTB
        isFutureProjection = 0 if startDateCurrentPeriodOTB == startDateProjectionPeriod else 1
        row = [0, 30, startDateProjectionPeriod, isFutureProjection, 510, startDateCurrentPeriodOTB, UNE,SUBMARCA,CATEGORIA,MERCADO]
        tmp_row = []
        for i in range(9):
            current_sv = otb_output[i]
            val = current_sv.get_data().astype(np.int64)[current_sv.get_shape_categories(element)]
            
            tmp_row.append(val)
        tmp_row[5], tmp_row[6] = tmp_row[6], tmp_row[5]
        row.extend(tmp_row)
        rows.append(row)

    rows = np.array(rows)
    df = pd.DataFrame(rows)
    df.to_csv('./files/otb_output.csv', index=False)

def generate_otb():
    generate_data()
    insert_data()

generate_otb()