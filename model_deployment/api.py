import os
os.chdir('..')

import joblib
from flask import Flask
from flask_restx import Api, Resource, fields
from model_deployment.predict_model import predict
from flask_cors import CORS

# Definición aplicación Flask
app = Flask(__name__)
CORS(app)

# Definición API Flask
api = Api(
    app, 
    version='1.0', 
    title='Used Cars Price Prediction API',
    description='Used Cars Price Prediction API')

ns = api.namespace('predict', 
     description='Used Cars Price Regressor')

# Definición argumentos o parámetros de la API
parser = api.parser()
parser.add_argument(
    'Data', 
    type=str, 
    required=True, 
    help='Data to be analyzed', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

@ns.route('/')
class UsedCarPriceApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "result": predict(args['Data'])
        }, 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
