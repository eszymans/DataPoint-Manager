from flask import jsonify, request, Blueprint

from app.extensions import db
from app.models import DataPoint


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/data', methods=['GET'])
def api_get_data():
    data = DataPoint.query.all()
    return jsonify([point.to_dict() for point in data])


@api_blueprint.route('/data', methods=['POST'])
def api_add_data():
    json_data = request.get_json()

    if (not json_data or
            'weight' not in json_data or
            'height' not in json_data or
            'category' not in json_data):
        return jsonify({'error': 'Invalid data. Required: weight, '
                                 'height, category'}), 400

    try:
        new_point = DataPoint(
            weight=float(json_data['weight']),
            height=float(json_data['height']),
            category=int(json_data['category'])
        )
        db.session.add(new_point)
        db.session.commit()
        return jsonify({'id': new_point.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_blueprint.route('/data/<int:record_id>', methods=['DELETE'])
def api_delete_data(record_id):
    point = DataPoint.query.get(record_id)
    if point:
        db.session.delete(point)
        db.session.commit()
        return jsonify({'deleted_id': record_id}), 200
    else:
        return jsonify({'error': 'Record not found'}), 404
