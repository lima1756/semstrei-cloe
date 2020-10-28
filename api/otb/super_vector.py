
class Dimension:
    """
    Una dimension denota el encabezado de una columna  y las categorias que esta categoria posee.
    Cada super vector debe poseer un conjunto de dimensiones ( encabezado ) para de esta forma describir los datos
    del super vector.
    Ejemplo: dimension_fruta = ["manzana", "pera"]
    La dimension fruta nos da una relacion entre sus categorias y el index que le pertenece a cada uno.
    En este caso, manzana --> 0, pera --> 1
    """

    _dimension_name = ""     # Nombre de la dimension
    _categories = []        # Relacion nombres tipos/categorias de una dimension vs el index asignado en esa dimension
                            # el index de la {categoria} debe coincidir con el indice de su vector numerico.

    def __init__(self, name, categories):
        self._dimension_name = name
        self._categories = categories

    def add_category(self, category):
        self._categories.append(category)

    def remove_category(self):
        if len(self.categories) > 0:
            return self.categories.pop()
        return None

    def get_name(self):
        return self._dimension_name

    def set_name(self, name):
        self._dimension_name = name

    def get_categories(self):
        return self._categories

    def set_categories(self, categories):
        self._categories = categories

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.get_name() != other.get_name():
            return False

        self_categ = self.get_categories()
        other_categ = other.get_categories()

        if (self_categ is None) != (other_categ is None):
            return False
        if self_categ is None:  # Both are None due last conditional
            return True
        if len(self_categ) != len(other_categ):
            return False

        for i in range(len(self_categ)):
            if self_categ[i] != other_categ[i]:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


class Header:
    """
    Un Header ( encabezado ) nos indicara las dimensiones y orden de dimensiones que posee nuestro vector de datos.
    Ejemplo:
    Sea (Frutas, Color) nuestro encabezado. Los datos nos indicaran cantidad["frutas"]["color"] hemos comprado.
    cantidad = [[ 1, 3, 2] , [0, 2, 3]]
    Si tenemos un encabezado de la forma: (Frutas --> [manzana, pera], Color --> [rojo, amarillo, verde])
    Esto implica que nuestro vector cantidad puede ser interpretado como:

             |  rojo   | amarillo  |   verde
    ---------------------------------------------
    manzana  |   1     |     3     |     2
    ---------------------------------------------
    pera     |   0     |     2     |     3

    El encabezado contiene las dimensiones (Frutas, Color), por lo que nos indica la forma en la cual estan
    organizados los datos en nuestro vector.
    """

    _dimensions = []
    _vector_name = ""

    def __init__(self, name, dimensions):
        self._dimensions = dimensions
        self._vector_name = name

    def add_dimension(self, dimension):
        self._dimensions.append(dimension)

    def remove_dimension(self):
        if len(self.dimensions) > 0:
            return self.dimensions.pop()
        return None

    def get_dimensions(self):
        return self._dimensions

    def set_dimensions(self, dimensions):
        self._dimensions = dimensions

    def get_vector_name(self):
        return self._vector_name

    def set_vector_name(self, vector_name):
        self._vector_name = vector_name

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.get_vector_name() != other.get_vector_name():
            return False

        self_dimensions = self.get_dimensions()
        other_dimensions = other.get_dimensions()

        if (self_dimensions is None) != (other_dimensions is None):
            return False
        if self_dimensions is None:  # Both are None due last conditional
            return True
        if len(self_dimensions) != len(other_dimensions):
            return False

        for i in range(len(self_dimensions)):
            if not self_dimensions[i] == other_dimensions[i]:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


class SuperVector:
    """
    Un SuperVector contiene los datos de nuestra entidad,
    asi como el encabezado que  describe a los datos.

    Sea:
    datos = [[ 1, 3, 2] , [0, 2, 3]]
    encabezado = (Frutas --> [manzana, pera], Color --> [rojo, amarillo, verde])
    Esto implica que nuestro vector cantidad puede ser interpretado como:

             |  rojo   | amarillo  |   verde
    ---------------------------------------------
    manzana  |   1     |     3     |     2
    ---------------------------------------------
    pera     |   0     |     2     |     3

    """

    _data = None  # vector np de datos
    _header = None

    def __init__(self, header, data):
        self._data = data
        self._header = header

    def get_data(self):
        return self._data

    def get_header(self):
        return self._header

    def set_data(self, data):
        self._data = data

    def set_header(self, header):
        self._header = header

    def are_same_type(self, other):
        return self.get_header() != other.get_header()
