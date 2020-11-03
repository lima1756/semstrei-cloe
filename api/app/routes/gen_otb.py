from flask import Blueprint, request, make_response, jsonify, render_template

password_recovery_blueprint = Blueprint('passsword_recovery', __name__)


class GenOTB(MethodView):
    def get(self):
        pass


gen_otb = GenOTB.as_view('gen_otb')
