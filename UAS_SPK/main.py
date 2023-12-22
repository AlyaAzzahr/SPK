from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import tbl_cushion as cushionModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'reputasi_brand': 3, 'kandungan_spf': 3, 'ketahanan': 2, 'isi_kemasan': 2, 'harga': 1}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(cushionModel.brand_cushion, cushionModel.reputasi_brand, cushionModel.kandungan_spf, cushionModel.ketahanan, cushionModel.isi_kemasan, cushionModel.harga)
        result = session.execute(query).fetchall()
        print(result)
        return [{'brand_cushion': tbl_cushion.brand_cushion, 'reputasi_brand': tbl_cushion.reputasi_brand, 'kandungan_spf': tbl_cushion.kandungan_spf, 'ketahanan': tbl_cushion.ketahanan, 'isi_kemasan': tbl_cushion.isi_kemasan, 'harga': tbl_cushion.harga} for tbl_cushion in result]

    @property
    def normalized_data(self):
        reputasi_brand_values = []
        kandungan_spf_values = []
        ketahanan_values = []
        isi_kemasan_values = []
        harga_values = []

        for data in self.data:
            reputasi_brand_values.append(data['reputasi_brand'])
            kandungan_spf_values.append(data['kandungan_spf'])
            ketahanan_values.append(data['ketahanan'])
            isi_kemasan_values.append(data['isi_kemasan'])
            harga_values.append(data['harga'])

        return [
            {'brand_cushion': data['brand_cushion'],
             'reputasi_brand': min(reputasi_brand_values) / data['reputasi_brand'],
             'kandungan_spf': data['kandungan_spf'] / max(kandungan_spf_values),
             'ketahanan': data['ketahanan'] / max(ketahanan_values),
             'isi_kemasan': data['isi_kemasan'] / max(isi_kemasan_values),
             'harga': data['harga'] / max(harga_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
                row['reputasi_brand'] ** self.raw_weight['reputasi_brand'] *
                row['kandungan_spf'] ** self.raw_weight['kandungan_spf'] *
                row['ketahanan'] ** self.raw_weight['ketahanan'] *
                row['isi_kemasan'] ** self.raw_weight['isi_kemasan'] *
                row['harga'] ** self.raw_weight['harga']
            )

            produk.append({
                'brand_cushion': row['brand_cushion'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'brand_cushion': product['brand_cushion'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['brand_cushion']:
                  round(row['reputasi_brand'] * weight['reputasi_brand'] +
                        row['kandungan_spf'] * weight['kandungan_spf'] +
                        row['ketahanan'] * weight['ketahanan'] +
                        row['isi_kemasan'] * weight['isi_kemasan'] +
                        row['harga'] * weight['harga'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class tbl_cushion(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(cushionModel)
        data = [{'brand_cushion': tbl_cushion.brand_cushion, 'reputasi_brand': tbl_cushion.reputasi_brand, 'kandungan_spf': tbl_cushion.kandungan_spf, 'ketahanan': tbl_cushion.ketahanan, 'isi_kemasan': tbl_cushion.isi_kemasan, 'harga': tbl_cushion.harga} for tbl_cushion in session.scalars(query)]
        return self.get_paginated_result('tbl_cushion/', data, request.args), HTTPStatus.OK.value


api.add_resource(tbl_cushion, '/tbl_cushion')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)