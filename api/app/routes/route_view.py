from flask.views import MethodView
from flask import make_response, jsonify


class RouteView(MethodView):

    def return_response(self, status, data, number):
        responseObject = {
            'status': status
        }
        if data is not None:
            responseObject = {
                **responseObject,
                **data
            }
        return make_response(jsonify(responseObject)), number

    def return_success(self, data = None):
        return self.return_response('success', data, 200)

    def return_success_201(self, data = None):
        return self.return_response('success', data, 201)

    def return_not_found(self, data = None):
        return self.return_response('fail', data, 404)

    def return_data_not_valid(self, validation):
        return self.return_response('fail', {
            'errors': validation.get_error()
        }, 424)

    def return_server_error(self, message='Some error occurred. Please try again.'):
        return self.return_response('fail', {
            'message': message
        }, 500)
