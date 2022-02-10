from flask_restful import Resource
from flask import request
from src.backend import api
from src.backend.recommender import recommend
import json


@api.resource('/recommendation')
class RecommendationResource(Resource):
    def post(self):
        data = json.loads(request.data)
        books = recommend(data['title'].lower(), data['author'].lower())
        return json.dumps(books)
