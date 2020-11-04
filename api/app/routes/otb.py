from flask import Blueprint, request, make_response, jsonify, render_template

otb = Blueprint('otb', __name__)


class OTB(MethodView):
    def get(self):
        pass


otb_view = OTB.as_view('otb')
