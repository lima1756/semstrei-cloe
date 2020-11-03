from flask import Blueprint, request, make_response, jsonify, render_template

password_recovery_blueprint = Blueprint('passsword_recovery', __name__)


class OTB(MethodView):
    def get(self):
        pass


otb = OTB.as_view('otb')
