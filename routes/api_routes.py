import os

from flask import Blueprint, jsonify, request

from services.resource_service import get_resources_by_category, load_resource_catalog
from services.json_storage import read_json
from services.gemini_service import is_configured

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/health', methods=['GET'])
def health_check():
    gemini_status = 'Connected' if is_configured() else 'Not Configured'
    return jsonify({
        'success': True,
        'backend': 'Connected',
        'gemini': gemini_status,
        'storage': 'Ready',
        'dependencies': 'Ready',
        'model': os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    })


@api_bp.route('/api/resources', methods=['GET'])
def get_resources():
    return jsonify({'success': True, 'data': load_resource_catalog()})


@api_bp.route('/api/resources/<category>', methods=['GET'])
def get_resources_by_name(category):
    return jsonify({'success': True, 'data': get_resources_by_category(category)})
