import os
from datetime import datetime

from services.gemini_service import generate_career_plan
from services.resource_service import get_resources_for_topic

ROOT = os.path.dirname(os.path.dirname(__file__))
CAREER_PATH = os.path.join(ROOT, 'data', 'career_profiles.json')
ROADMAP_PATH = os.path.join(ROOT, 'data', 'roadmaps.json')


def build_roadmap(data):
    role = data.get('target_role', 'Career Goal')
    time_per_day = data.get('time_per_day', '1 hour')
    skill_list = data.get('skills', [])
    skills_text = ', '.join(skill_list[:5]) if skill_list else 'core skills'

    roadmap = []
    weekly_topics = [
        ('Week 1: Foundation', 'Build foundational understanding of your target role and core technical concepts.', 'Python and role basics'),
        ('Week 2: Core Skills', 'Deepen technical confidence through targeted skill-building exercises.', 'SQL, Excel, analytics workflows'),
        ('Week 3: Practical Application', 'Apply your learning with mini-projects and exercises.', 'Project implementation and dashboarding'),
        ('Week 4: Projects + Interview Prep', 'Polish portfolio and prepare for interviews.', 'Interview practice and portfolio evidence'),
    ]
    days = 1
    for week_name, week_desc, focus in weekly_topics:
        for _ in range(7):
            topic = focus
            if 'Foundation' in week_name:
                topic = 'Role foundation: ' + skills_text
            elif 'Core Skills' in week_name:
                topic = 'Core skill sprint for ' + role
            elif 'Practical Application' in week_name:
                topic = 'Practice application for ' + role
            else:
                topic = 'Portfolio and interview readiness for ' + role
            roadmap.append({
                'day': days,
                'week': week_name,
                'topic': topic,
                'what_to_learn': week_desc,
                'estimated_time': time_per_day,
                'practical_task': 'Complete a focused task using ' + topic.lower(),
                'expected_outcome': 'Improved role readiness and confidence.',
                'learning_resource': 'Search resource',
                'status': 'Not Started'
            })
            days += 1
    return roadmap


def analyze_career(profile):
    career_plan = generate_career_plan(profile)
    if isinstance(career_plan, dict) and career_plan.get('success') is False:
        return career_plan
    role = profile.get('target_role', 'Career Goal')
    roadmap = career_plan.get('roadmap') or build_roadmap(profile)
    skill_gap_analysis = career_plan.get('skill_gap_analysis', [])
    readiness = career_plan.get('readiness', {'Technical Skills': 72, 'Practical Experience': 65, 'Projects': 68, 'Resume Strength': 70, 'Learning Progress': 80, 'Interview Readiness': 74})
    resources = career_plan.get('resources', [])
    if not resources:
        resources = get_resources_for_topic(role)
    if isinstance(resources, list) and not resources:
        resources.append({'title': 'Search resource', 'platform': 'Search', 'type': 'Resource', 'difficulty': 'Varied', 'estimated_time': 'Varied', 'url': '#'})

    result = {
        'career_summary': career_plan.get('summary', f'You are currently developing toward a {role} role. Focus on the skill gaps most relevant to the role and track steady progress. '),
        'skill_gap_analysis': skill_gap_analysis,
        'career_readiness_score': career_plan.get('career_readiness_score', 78),
        'roadmap': roadmap,
        'radar': career_plan.get('radar', {'categories': ['Python', 'SQL', 'Excel', 'Statistics', 'Visualization', 'Communication'], 'current': [80, 45, 70, 50, 55, 68], 'required': [90, 85, 80, 75, 80, 80]}),
        'readiness': readiness,
        'recommendations': career_plan.get('recommendations', ['Practice role-specific SQL tasks', 'Build one portfolio project', 'Refresh your resume with measurable outcomes']),
        'resources': resources,
        'target_role': role,
        'profile': profile,
        'generated_at': datetime.utcnow().isoformat()
    }
    return result
