from flask import Flask, jsonify, request, Response
from flask.views import MethodView
from models import Advertisement, Session
from errors import HttpError
from sqlalchemy.exc import IntegrityError
from schema import CreateAdvertisement, UpdateAdvertisement, validate_json

app = Flask("app")

class AdvertisementView(MethodView):
    def get(self, ad_id: int):
        session = Session()
        ad = session.query(Advertisement).get(ad_id)
        if ad is None:
            raise HttpError(404, "Advertisement not found")
        return jsonify({
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'date_created': ad.date_created,
            'owner': ad.owner
        })

    def post(self):
        json_data = validate_json(CreateAdvertisement, request.json)
        ad = Advertisement(
            title=json_data["title"],
            description=json_data["description"],
            owner=json_data["owner"]
        )
        session = Session()
        session.add(ad)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HttpError(400, "Advertisement with this title already exists")
        return jsonify({'id': ad.id})

    def delete(self, ad_id: int):
        session = Session()
        ad = session.query(Advertisement).get(ad_id)
        if ad is None:
            raise HttpError(404, "Advertisement not found")
        session.delete(ad)
        session.commit()
        return jsonify({"status": "success"})

advertisement_view = AdvertisementView.as_view("advertisement_view")

app.add_url_rule("/api/v1/advertisement", view_func=advertisement_view, methods=["POST"])
app.add_url_rule(
    "/api/v1/advertisement/<int:ad_id>",
    view_func=advertisement_view,
    methods=["GET", "DELETE"]
)

if __name__ == '__main__':
    app.run()