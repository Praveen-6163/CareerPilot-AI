import os
from datetime import datetime

from flask import Blueprint, jsonify, request

from services.career_service import analyze_career, build_roadmap
from services.json_storage import read_json, write_json

career_bp = Blueprint('career', __name__)


@career_bp.route('/api/career/analyze', methods=['POST'])
def analyze_route():
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    role = (payload.get('target_role') or '').strip()
    skills = payload.get('skills') or []
    if not name or not role or not skills or not payload.get('time_per_day'):
        return jsonify({'success': False, 'error_code': 'VALIDATION_ERROR', 'message': 'Name, target role, skills, and available time are required.'}), 400

    result = analyze_career(payload)
    if isinstance(result, dict) and result.get('success') is False:
        return jsonify(result), 400

    profiles = read_json('career_profiles.json', [])
    profiles.append({**payload, 'id': len(profiles) + 1, 'created_at': datetime.utcnow().isoformat()})
    write_json('career_profiles.json', profiles)

    roadmap = result.get('roadmap', build_roadmap(payload))
    roadmaps = read_json('roadmaps.json', [])
    roadmaps.append({'id': len(roadmaps) + 1, 'target_role': role, 'roadmap': roadmap, 'created_at': datetime.utcnow().isoformat()})
    write_json('roadmaps.json', roadmaps)

    return jsonify({'success': True, 'data': result})


@career_bp.route('/api/career/profile', methods=['GET'])
def get_profile():
    profiles = read_json('career_profiles.json', [])
    return jsonify({'success': True, 'data': profiles[-1] if profiles else {}})


@career_bp.route('/api/career/profile', methods=['PUT'])
def update_profile():
    payload = request.get_json(silent=True) or {}
    profiles = read_json('career_profiles.json', [])
    if profiles:
        profiles[-1].update(payload)
        write_json('career_profiles.json', profiles)
        return jsonify({'success': True, 'data': profiles[-1]})
    return jsonify({'success': False, 'error_code': 'PROFILE_NOT_FOUND', 'message': 'No career profile exists yet.'}), 404


@career_bp.route('/api/career/roadmap', methods=['GET'])
def get_roadmap():
    roadmaps = read_json('roadmaps.json', [])
    return jsonify({'success': True, 'data': roadmaps[-1] if roadmaps else {'roadmap': []}})


@career_bp.route('/api/career/roadmap/progress', methods=['PUT'])
def update_progress():
    payload = request.get_json(silent=True) or {}
    day = payload.get('day')
    status = payload.get('status')
    if day is None or not status:
        return jsonify({'success': False, 'error_code': 'VALIDATION_ERROR', 'message': 'Day and status are required.'}), 400

    roadmaps = read_json('roadmaps.json', [])
    if not roadmaps:
        return jsonify({'success': False, 'error_code': 'ROADMAP_NOT_FOUND', 'message': 'No roadmap exists yet.'}), 404
    roadmap = roadmaps[-1].get('roadmap', [])
    for item in roadmap:
        if item.get('day') == day:
            item['status'] = status
            break
    roadmaps[-1]['roadmap'] = roadmap
    write_json('roadmaps.json', roadmaps)
    return jsonify({'success': True, 'data': roadmaps[-1]})
