import json
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except Exception:
    genai = None

MODEL_NAME = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')


def is_configured():
    return bool(os.getenv('GEMINI_API_KEY'))


def _build_error(code, message, user_action):
    return {
        'success': False,
        'error_code': code,
        'message': message,
        'user_action': user_action,
    }


def _classify_error(error):
    message = str(error).lower()
    if 'api key' in message or 'invalid api' in message or 'unauthorized' in message:
        return 'INVALID_API_KEY', 'Gemini API key is invalid or expired.', 'Check your GEMINI_API_KEY in the .env file and restart the app.'
    if 'quota' in message or 'exceeded' in message:
        return 'QUOTA_EXCEEDED', 'The Gemini API quota has been exceeded.', 'Wait a bit and retry or review your Gemini usage limits.'
    if 'rate limit' in message or '429' in message:
        return 'RATE_LIMITED', 'Gemini rate limit reached.', 'Retry after a short delay and avoid sending too many requests at once.'
    if 'timeout' in message:
        return 'TIMEOUT', 'The Gemini request timed out.', 'Retry the request or use a lighter prompt.'
    if 'safety' in message or 'blocked' in message:
        return 'SAFETY_REJECTION', 'The AI request was blocked by safety filters.', 'Refine your content and try again with less sensitive wording.'
    if 'model' in message or 'not found' in message or 'unavailable' in message:
        return 'MODEL_UNAVAILABLE', 'The Gemini model is temporarily unavailable.', 'Try again later or switch to a supported model name.'
    if 'network' in message or 'connection' in message:
        return 'NETWORK_ERROR', 'The AI service could not be reached.', 'Check your internet connection and restart the app.'
    if 'malformed' in message or 'invalid request' in message:
        return 'INVALID_REQUEST', 'The AI request was invalid.', 'Revise the request format and retry.'
    return 'AI_ERROR', 'The AI service returned an unexpected error.', 'Retry the action or check the API configuration.'


def _safe_json_parse(raw_text):
    try:
        return json.loads(raw_text)
    except Exception:
        text = str(raw_text).strip()
        if text.startswith('```'):
            text = text.strip('`')
            if text.lower().startswith('json'):
                text = text[4:].strip()
        try:
            return json.loads(text)
        except Exception:
            return {'summary': text}


def _call_gemini(prompt):
    if not is_configured():
        return None
    if genai is None:
        raise RuntimeError('google-genai package is not installed')
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return getattr(response, 'text', None) or getattr(response, 'output_text', None) or str(response)


def generate_career_plan(profile):
    if not is_configured():
        return {
            'demo_mode': True,
            'summary': 'Demo data — connect Gemini API for live AI analysis.',
            'skill_gap_analysis': [
                {'skill': 'Python', 'current_level': 'Intermediate', 'required_level': 'Advanced', 'gap': 'Medium', 'priority': 'High'},
                {'skill': 'SQL', 'current_level': 'Beginner', 'required_level': 'Advanced', 'gap': 'High', 'priority': 'High'},
                {'skill': 'Excel', 'current_level': 'Intermediate', 'required_level': 'Advanced', 'gap': 'Medium', 'priority': 'Medium'},
            ],
            'career_readiness_score': 78,
            'roadmap': [
                {'day': 1, 'topic': 'Python fundamentals', 'what_to_learn': 'Review variables, loops, functions, APIs.', 'time': '45 mins', 'task': 'Build a mini script to automate CSV processing.', 'outcome': 'Confidence with Python basics.', 'resource': 'Python docs'}
            ],
            'radar': {'categories': ['Python', 'SQL', 'Excel', 'Statistics', 'Visualization', 'Communication'], 'current': [80, 45, 70, 50, 55, 68], 'required': [90, 85, 80, 75, 80, 80]},
            'readiness': {'Technical Skills': 76, 'Practical Experience': 62, 'Projects': 70, 'Resume Strength': 68, 'Learning Progress': 80, 'Interview Readiness': 71},
            'recommendations': ['Practice SQL joins and window functions.', 'Build one analytics portfolio project.', 'Improve resume summary with role keywords.'],
            'resources': [
                {'title': 'Python Official Docs', 'platform': 'Python', 'type': 'Documentation', 'difficulty': 'Beginner', 'estimated_time': '2 hours', 'url': 'https://docs.python.org/3/'},
                {'title': 'SQL Tutorial', 'platform': 'W3Schools', 'type': 'Tutorial', 'difficulty': 'Beginner', 'estimated_time': '1.5 hours', 'url': 'https://www.w3schools.com/sql/'},
            ],
        }

    try:
        prompt = json.dumps(profile, indent=2)
        raw = _call_gemini(f"You are an expert career coach. Return valid JSON only. Use this profile: {prompt}. Include fields: summary, skill_gap_analysis, career_readiness_score, roadmap, radar, readiness, recommendations, resources.")
        payload = _safe_json_parse(raw)
        payload['demo_mode'] = False
        return payload
    except Exception as error:
        error_code, message, user_action = _classify_error(error)
        return _build_error(error_code, message, user_action)


def generate_resume_analysis(payload):
    if not is_configured():
        return {
            'demo_mode': True,
            'summary': 'Demo data — connect Gemini API for live AI analysis.',
            'score': 82,
            'ats_breakdown': {'keyword_match': 82, 'role_alignment': 85, 'skills_match': 88, 'experience_relevance': 76, 'resume_structure': 90, 'achievement_quality': 72, 'readability': 86},
            'match_overview': {'overall_match': 82, 'matched_skills': 8, 'missing_skills': 3, 'relevant_experience': 'High', 'keyword_coverage': 76},
            'recommendations': {'keep': ['Strong Python and spreadsheet experience.', 'Clear project examples.'], 'improve': ['Add more measurable outcomes.', 'Mention SQL joins and reporting work.'], 'add': ['Data cleaning examples', 'Action verbs and metrics'], 'remove': ['Generic project wording'], 'rewrite': ['Replace vague statements with quantified technical achievements.']},
            'ats_checklist': {'contact_info': '✓ Good', 'section_headings': '✓ Good', 'target_keywords': '⚠ Needs attention', 'formatting': '✓ Good'},
            'action_plan': [
                {'step': 1, 'priority': 'High', 'reason': 'Target role keywords are missing from experience bullets.', 'suggested_action': 'Add SQL, dashboarding, and data analysis keywords where relevant.'},
                {'step': 2, 'priority': 'High', 'reason': 'Project results need stronger outcomes.', 'suggested_action': 'Rewrite project bullets with tools, tasks, and measurable impact.'},
            ],
            'interview_prep': {'technical': ['Explain your approach to cleaning messy data.', 'How do you validate a dashboard?'], 'behavioral': ['Tell me about a project challenge.', 'Describe a time you improved a process.'], 'role_specific': ['How do you prioritize KPIs?', 'How would you explain insights to non-technical teams?']},
            'job_links': [{'platform': 'LinkedIn Jobs', 'url': 'https://www.linkedin.com/jobs/'}, {'platform': 'Naukri', 'url': 'https://www.naukri.com/'}, {'platform': 'Indeed', 'url': 'https://www.indeed.com/'}, {'platform': 'Glassdoor', 'url': 'https://www.glassdoor.com/'}],
            'resources': [{'title': 'Python Official Docs', 'platform': 'Python', 'url': 'https://docs.python.org/3/'}],
        }

    try:
        prompt = json.dumps(payload, indent=2)
        raw = _call_gemini(f"You are a top ATS and resume optimization expert. Return valid JSON only. Analyze this resume and job information: {prompt}. Include keys: score, ats_breakdown, match_overview, recommendations, ats_checklist, action_plan, interview_prep, job_links, resources.")
        payload = _safe_json_parse(raw)
        payload['demo_mode'] = False
        return payload
    except Exception as error:
        error_code, message, user_action = _classify_error(error)
        return _build_error(error_code, message, user_action)


def generate_interview_prep(target_role, skill_gaps):
    if not is_configured():
        return {
            'demo_mode': True,
            'technical_questions': [
                {'question': 'How would you clean inconsistent data before analysis?', 'what_evaluates': 'Data preparation', 'suggested_preparation': 'Practice handling missing values, duplicates, and format conversions.'},
                {'question': 'What is the difference between inner and left joins?', 'what_evaluates': 'SQL reasoning', 'suggested_preparation': 'Review SQL join behavior and examples.'}
            ],
            'behavioral_questions': [
                {'question': 'Tell me about a time you solved a problem with limited information.', 'what_evaluates': 'Problem solving', 'suggested_preparation': 'Prepare a STAR story using a data challenge.'}
            ],
            'role_specific_questions': [
                {'question': 'How would you explain a KPI trend to a business stakeholder?', 'what_evaluates': 'Stakeholder communication', 'suggested_preparation': 'Practice translating technical results into business language.'}
            ]
        }

    try:
        raw = _call_gemini(f"Return valid JSON only for role {target_role}. Create 5 technical questions, 5 behavioral questions, and 5 role-specific questions. Use this skill gap list: {json.dumps(skill_gaps)}. Each question should include question, what_evaluates, suggested_preparation.")
        return _safe_json_parse(raw)
    except Exception as error:
        error_code, message, user_action = _classify_error(error)
        return _build_error(error_code, message, user_action)
