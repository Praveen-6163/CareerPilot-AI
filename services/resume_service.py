import os
import uuid
from werkzeug.utils import secure_filename

from services.ats_service import score_ats
from services.gemini_service import generate_resume_analysis
from utils.file_parser import extract_text_from_file


def parse_resume_file(file_storage, filename):
    allowed = ['.pdf', '.docx', '.txt']
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed:
        raise ValueError('Unsupported file type. Please upload PDF, DOCX, or TXT.')
    if file_storage is None:
        raise ValueError('No file uploaded. Please select a resume file.')
    if file_storage.content_length and file_storage.content_length > 10 * 1024 * 1024:
        raise ValueError('File exceeds 10 MB. Please upload a smaller file.')

    safe_name = secure_filename(filename)
    storage_path = os.path.join('uploads', safe_name)
    file_storage.save(storage_path)
    text = extract_text_from_file(storage_path, safe_name)
    if not text or not text.strip():
        raise ValueError('The uploaded resume file is empty or unreadable.')
    return {'text': text, 'path': storage_path, 'filename': safe_name, 'id': str(uuid.uuid4())}


def analyze_resume(resume_text, target_role, job_description):
    ats_result = score_ats(resume_text, target_role, job_description)
    ai = generate_resume_analysis({'resume_text': resume_text, 'target_role': target_role, 'job_description': job_description, 'ats_breakdown': ats_result})
    if isinstance(ai, dict) and ai.get('success') is False:
        return {'analysis': ats_result, 'error': ai}
    merged = {'resume_text': resume_text, 'target_role': target_role, 'job_description': job_description}
    merged.update(ats_result)
    merged.update(ai)
    return {'analysis': merged}
