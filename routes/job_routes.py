from flask import Blueprint, jsonify, request

job_bp = Blueprint('jobs', __name__)

JOB_PORTALS = {
    'Data Analyst': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst'), ('Naukri', 'https://www.naukri.com/data-analyst-jobs'), ('Indeed', 'https://in.indeed.com/jobs?q=Data+Analyst'), ('Glassdoor', 'https://www.glassdoor.com/Job/data-analyst-jobs-SRCH_KO0,12.htm'), ('Wellfound', 'https://wellfound.com/jobs?query=Data%20Analyst')],
    'Data Scientist': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist'), ('Naukri', 'https://www.naukri.com/data-scientist-jobs'), ('Indeed', 'https://in.indeed.com/jobs?q=Data+Scientist'), ('Glassdoor', 'https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,16.htm'), ('Wellfound', 'https://wellfound.com/jobs?query=Data%20Scientist')],
    'Machine Learning Engineer': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Machine%20Learning%20Engineer'), ('Indeed', 'https://in.indeed.com/jobs?q=Machine+Learning+Engineer'), ('Wellfound', 'https://wellfound.com/jobs?query=Machine%20Learning%20Engineer')],
    'Software Developer': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Software%20Developer'), ('Naukri', 'https://www.naukri.com/software-developer-jobs'), ('Indeed', 'https://in.indeed.com/jobs?q=Software+Developer'), ('Glassdoor', 'https://www.glassdoor.com/Job/software-developer-jobs-SRCH_KO0,18.htm')],
    'Web Developer': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Web%20Developer'), ('Indeed', 'https://in.indeed.com/jobs?q=Web+Developer'), ('Naukri', 'https://www.naukri.com/web-developer-jobs')],
    'Python Developer': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Python%20Developer'), ('Indeed', 'https://in.indeed.com/jobs?q=Python+Developer'), ('Naukri', 'https://www.naukri.com/python-developer-jobs')],
    'AI Engineer': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=AI%20Engineer'), ('Indeed', 'https://in.indeed.com/jobs?q=AI+Engineer'), ('Wellfound', 'https://wellfound.com/jobs?query=AI%20Engineer')],
    'Business Analyst': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Business%20Analyst'), ('Naukri', 'https://www.naukri.com/business-analyst-jobs'), ('Indeed', 'https://in.indeed.com/jobs?q=Business+Analyst'), ('Glassdoor', 'https://www.glassdoor.com/Job/business-analyst-jobs-SRCH_KO0,18.htm')],
    'Cloud Engineer': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Cloud%20Engineer'), ('Indeed', 'https://in.indeed.com/jobs?q=Cloud+Engineer'), ('Naukri', 'https://www.naukri.com/cloud-engineer-jobs')],
    'Cybersecurity Analyst': [('LinkedIn Jobs', 'https://www.linkedin.com/jobs/search/?keywords=Cybersecurity%20Analyst'), ('Indeed', 'https://in.indeed.com/jobs?q=Cybersecurity+Analyst'), ('Naukri', 'https://www.naukri.com/cyber-security-jobs')],
}


@job_bp.route('/api/jobs/search-links', methods=['GET'])
def job_search_links():
    role = request.args.get('role', 'Data Analyst')
    if not role:
        role = 'Data Analyst'
    portals = JOB_PORTALS.get(role, JOB_PORTALS['Data Analyst'])
    return jsonify({'success': True, 'data': {'role': role, 'links': [{'platform': name, 'url': url} for name, url in portals]}})
