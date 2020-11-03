from flask import Blueprint, request, make_response, jsonify, render_template

password_recovery_blueprint = Blueprint('passsword_recovery', __name__)


class GenOTB(MethodView):
    def get(self):
        #TODO:
        # - query de la bdd para obtener la nueva info
        # - llamar codigo de Alex para calcular el OTB
        # - hacer uso de modelos creado por Alex y guardar los nuevos datos
        pass


gen_otb = GenOTB.as_view('gen_otb')
