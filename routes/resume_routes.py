from flask import Blueprint, jsonify, request

from services.json_storage import read_json, write_json
from services.resume_service import analyze_resume, parse_resume_file

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error_code': 'FILE_REQUIRED', 'message': 'Please upload a resume file.'}), 400

    uploaded = request.files['file']
    if uploaded.filename == '':
        return jsonify({'success': False, 'error_code': 'FILE_REQUIRED', 'message': 'Please select a resume file.'}), 400

    try:
        parsed = parse_resume_file(uploaded, uploaded.filename)
        history = read_json('history.json', [])
        history.append({'id': parsed['id'], 'filename': parsed['filename'], 'status': 'uploaded', 'path': parsed['path']})
        write_json('history.json', history)
        return jsonify({'success': True, 'data': {'id': parsed['id'], 'filename': parsed['filename'], 'source_path': parsed['path']}})
    except ValueError as exc:
        return jsonify({'success': False, 'error_code': 'INVALID_FILE', 'message': str(exc)}), 400


@resume_bp.route('/api/resume/analyze', methods=['POST'])
def analyze_resume_route():
    payload = request.get_json(silent=True) or {}
    resume_text = (payload.get('resume_text') or '').strip()
    target_role = (payload.get('target_role') or '').strip()
    job_description = (payload.get('job_description') or '').strip()

    if not target_role:
        return jsonify({'success': False, 'error_code': 'VALIDATION_ERROR', 'message': 'Target role is required.'}), 400
    if not job_description:
        return jsonify({'success': False, 'error_code': 'VALIDATION_ERROR', 'message': 'Job description is required.'}), 400
    if not resume_text:
        return jsonify({'success': False, 'error_code': 'VALIDATION_ERROR', 'message': 'Resume text is required for analysis.'}), 400

    result = analyze_resume(resume_text, target_role, job_description)
    if 'error' in result:
        return jsonify(result['error']), 400

    analysis = result['analysis']
    items = read_json('resume_analysis.json', [])
    analysis_record = {'id': len(items) + 1, 'target_role': target_role, 'job_description': job_description, 'analysis': analysis}
    items.append(analysis_record)
    write_json('resume_analysis.json', items)

    return jsonify({'success': True, 'data': analysis_record})


@resume_bp.route('/api/resume/history', methods=['GET'])
def resume_history():
    return jsonify({'success': True, 'data': read_json('history.json', [])})


@resume_bp.route('/api/resume/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    items = read_json('resume_analysis.json', [])
    for item in items:
        if str(item.get('id')) == str(analysis_id):
            return jsonify({'success': True, 'data': item})
    return jsonify({'success': False, 'error_code': 'NOT_FOUND', 'message': 'Resume analysis not found.'}), 404
