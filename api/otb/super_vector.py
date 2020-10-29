
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
        if len(self._categories) > 0:
            return self._categories.pop()
        return None

    def get_name(self):
        return self._dimension_name

    def set_name(self, name):
        self._dimension_name = name

    def get_categories(self):
        return self._categories

    def set_categories(self, categories):
        self._categories = categories

    def get_index_category(self, category_name):
        if category_name not in self._categories:
            return None
        return self._categories.index(category_name)

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
        if len(self._dimensions) > 0:
            return self._dimensions.pop()
        return None

    def get_dimensions(self):
        return self._dimensions

    def set_dimensions(self, dimensions):
        self._dimensions = dimensions

    def get_vector_name(self):
        return self._vector_name

    def set_vector_name(self, vector_name):
        self._vector_name = vector_name

    def get_index_dimension(self, dimension_name):
        for i in range(len(self._dimensions)):
            if dimension_name == self._dimensions[i].get_name():
                return i
        return None

    def get_index_category(self, dimension_name, category_name):
        idx_dim = self.get_index_dimension(dimension_name)
        if idx_dim is None:
            return None
        return [idx_dim, self._dimensions[idx_dim].get_index_category(category_name)]

    def get_shape_categories(self, categories_each_dimension):
        result = []
        if len(categories_each_dimension) > len(self._dimensions):
            return None  # If categories for each dim are smaller than  h.dimensions, we'll return the first N dim.
        for i in range(len(categories_each_dimension)):
            result.append(self.get_index_category(self._dimensions[i].get_name(),
                                                  categories_each_dimension[i])[-1])
        return tuple(result)

    def __eq__(self, other):
        if type(self) != type(other):
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
            if self_dimensions[i] != other_dimensions[i]:
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
        return self.get_header() == other.get_header()

    def get_index_dimension(self, dimension_name):
        return self._header.get_index_dimension(dimension_name)

    def get_index_category(self, dimension_name, category_name):
        return self._header.get_index_category(dimension_name, category_name)

    def get_shape_categories(self, categories_each_dimension):
        return self._header.get_shape_categories(categories_each_dimension)
