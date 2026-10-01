import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

from routes.api_routes import api_bp
from routes.career_routes import career_bp
from routes.job_routes import job_bp
from routes.resume_routes import resume_bp

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(api_bp)
app.register_blueprint(career_bp)
app.register_blueprint(job_bp)
app.register_blueprint(resume_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/career-guide')
def career_guide():
    return render_template('career.html')

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/resume-analyzer')
def resume_analyzer():
    return render_template('resume.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.errorhandler(400)
def bad_request(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error_code': 'BAD_REQUEST', 'message': 'The request data is invalid.'}), 400
    return render_template('index.html', error='Request could not be processed.'), 400

@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error_code': 'NOT_FOUND', 'message': 'The requested endpoint was not found.'}), 404
    return render_template('index.html', error='Page not found.'), 404

@app.errorhandler(413)
def too_large(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error_code': 'FILE_TOO_LARGE', 'message': 'Uploaded file exceeds the 10 MB size limit.'}), 413
    return render_template('index.html', error='Uploaded file is too large.'), 413

@app.errorhandler(429)
def rate_limited(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error_code': 'RATE_LIMITED', 'message': 'The AI service is rate limited right now. Please wait a moment and retry.'}), 429
    return render_template('index.html', error='Too many requests. Please try again later.'), 429

@app.errorhandler(500)
def server_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error_code': 'SERVER_ERROR', 'message': 'Something went wrong on the server. Please try again.'}), 500
    return render_template('index.html', error='A server issue occurred. Please try again.'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
