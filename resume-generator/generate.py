#!/usr/bin/env python3
"""
Resume Generator Script
Converts resume text files to styled HTML resumes and PDFs
Supports multiple people: matt, max, alison
"""

import re
import subprocess
import sys
import os
import shutil
import argparse
from typing import List, Dict, Any

# Person-specific configurations
PERSON_CONFIGS = {
    'matt': {
        'input_file': 'matt_resume.txt',
        'profile_image': 'matt-profile-image.jpeg',
        'linkedin_url': 'https://linkedin.com/in/mreider',
        'output_dir': 'matt',
        'resume_type': 'professional',  # professional resume with skills grid
        'show_skills_grid': False,
        'show_certifications': True,
        'show_personal': True,
    },
    'max': {
        'input_file': 'max_resume.txt',
        'profile_image': 'max-profile-image.jpeg',
        'linkedin_url': None,  # No LinkedIn for Max
        'output_dir': 'max',
        'resume_type': 'student_twocol',  # two-column student resume format
        'show_skills_grid': False,
        'show_certifications': False,
        'show_personal': False,
    },
    'alison': {
        'input_file': 'alison_resume.txt',
        'profile_image': 'alison.jpeg',
        'linkedin_url': 'https://www.linkedin.com/in/alison-cohen-4229681a7',
        'output_dir': 'alison',
        'resume_type': 'professional',  # professional resume
        'show_skills_grid': False,
        'show_certifications': False,
        'show_personal': False,
    },
}


def parse_resume_data(filename: str) -> Dict[str, Any]:
    """Parse the resume data from text file"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {}

    # Parse basic info
    data['name'] = re.search(r'NAME: (.+)', content).group(1)
    data['phone'] = re.search(r'PHONE: (.+)', content).group(1)
    data['email'] = re.search(r'EMAIL: (.+)', content).group(1)
    data['location'] = re.search(r'LOCATION: (.+)', content).group(1)

    # Parse summary
    summary_match = re.search(r'SUMMARY:\n(.+?)(?=\n\n|\nJOB TITLE|\nEDUCATION|\nLEADERSHIP)', content, re.DOTALL)
    data['summary'] = summary_match.group(1).strip() if summary_match else ""

    # Parse jobs
    data['jobs'] = []

    # Pattern for jobs with bullets
    job_with_bullets_pattern = r'JOB TITLE: (.+?)\nCOMPANY: (.+?)\nDATES: (.+?)\n((?:- .+\n?)+)'
    for match in re.finditer(job_with_bullets_pattern, content):
        title, company, dates, bullets = match.groups()
        bullet_list = [line.strip('- ').strip() for line in bullets.split('\n') if line.strip().startswith('-')]
        data['jobs'].append({
            'title': title,
            'company': company,
            'dates': dates,
            'bullets': bullet_list
        })

    # Pattern for jobs without bullets
    job_without_bullets_pattern = r'JOB TITLE: (.+?)\nCOMPANY: (.*?)\nDATES: (.+?)(?=\n\n|\nJOB TITLE|\nEDUCATION|\nACTIVITIES|\nSKILLS|\nLANGUAGES|$)'
    for match in re.finditer(job_without_bullets_pattern, content):
        title, company, dates = match.groups()
        # Skip if this job was already found with bullets
        already_exists = any(job['title'] == title.strip() and job['company'] == company.strip() for job in data['jobs'])
        if not already_exists:
            data['jobs'].append({
                'title': title.strip(),
                'company': company.strip(),
                'dates': dates.strip(),
                'bullets': []
            })

    # Parse education
    data['education'] = []
    edu_match = re.search(r'EDUCATION:\n\n(.+?)(?=\nLICENSES|\nLEADERSHIP|\nACTIVITIES|\nSKILLS|\nPERSONAL|$)', content, re.DOTALL)
    if edu_match:
        edu_text = edu_match.group(1).strip()
        lines = edu_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line and not line.startswith('Graduated') and not line.startswith('Pupil Personnel') and not line.startswith('High Level') and not line.startswith('An interdisciplinary'):
                degree = line
                school = ""
                date = ""
                details = ""

                # Get school from next line
                if i + 1 < len(lines):
                    school = lines[i + 1].strip()

                # Get graduation date from next line
                if i + 2 < len(lines):
                    next_line = lines[i + 2].strip()
                    if next_line.startswith('Graduated'):
                        date = next_line.replace('Graduated ', '')
                        i += 1
                    elif re.match(r'^[A-Z][a-z]+ \d{4}', next_line):
                        # Date format like "September 2025 - Present"
                        date = next_line
                        i += 1

                # Check for additional details
                if i + 2 < len(lines):
                    detail_line = lines[i + 2].strip()
                    if detail_line and not re.match(r'^[A-Z][a-z]+ of|^Bachelor|^Master|^International', detail_line):
                        details = detail_line
                        i += 1

                data['education'].append({
                    'degree': degree,
                    'school': school,
                    'date': date,
                    'details': details if details else None
                })
                i += 2
            else:
                i += 1

    # Parse leadership training (for Max's resume)
    data['leadership'] = []
    leadership_match = re.search(r'LEADERSHIP TRAINING:\n\n(.+?)(?=\nACTIVITIES|$)', content, re.DOTALL)
    if leadership_match:
        # Use the job parser for leadership section too
        leadership_content = leadership_match.group(1)
        job_pattern = r'JOB TITLE: (.+?)\nCOMPANY: (.+?)\nDATES: (.+?)\n((?:- .+\n?)+)'
        for match in re.finditer(job_pattern, leadership_content):
            title, company, dates, bullets = match.groups()
            bullet_list = [line.strip('- ').strip() for line in bullets.split('\n') if line.strip().startswith('-')]
            data['leadership'].append({
                'title': title,
                'company': company,
                'dates': dates,
                'bullets': bullet_list
            })

    # Parse activities (for Max's resume)
    data['activities'] = []
    activities_match = re.search(r'ACTIVITIES:\n\n(.+?)(?=\nWORK EXPERIENCE|\nSKILLS|$)', content, re.DOTALL)
    if activities_match:
        activities_text = activities_match.group(1).strip()
        # Split by double newlines or activity headers
        blocks = re.split(r'\n\n+', activities_text)
        for block in blocks:
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            if lines:
                activity_name = lines[0]
                activity_bullets = [l.strip('- ').strip() for l in lines[1:] if l.strip().startswith('-')]
                data['activities'].append({
                    'name': activity_name,
                    'bullets': activity_bullets
                })

    # Parse work experience (for student resumes)
    data['work_experience'] = []
    work_match = re.search(r'WORK EXPERIENCE:\n\n(.+?)(?=\nSKILLS|$)', content, re.DOTALL)
    if work_match:
        work_content = work_match.group(1)
        job_pattern = r'JOB TITLE: (.+?)\nCOMPANY: (.+?)\nDATES: (.+?)\n((?:- .+\n?)*)'
        for match in re.finditer(job_pattern, work_content):
            title, company, dates, bullets = match.groups()
            bullet_list = [line.strip('- ').strip() for line in bullets.split('\n') if line.strip().startswith('-')]
            data['work_experience'].append({
                'title': title,
                'company': company,
                'dates': dates,
                'bullets': bullet_list
            })

    # Parse skills (simple list for Max)
    data['skills'] = []
    skills_match = re.search(r'SKILLS:\n((?:- .+\n?)+)', content)
    if skills_match:
        skills_text = skills_match.group(1)
        data['skills'] = [line.strip('- ').strip() for line in skills_text.split('\n') if line.strip().startswith('-')]

    # Parse languages
    languages_match = re.search(r'LANGUAGES:\n(.+?)(?=\n\n|$)', content, re.DOTALL)
    data['languages'] = languages_match.group(1).strip() if languages_match else ""

    # Parse interests
    interests_match = re.search(r'INTERESTS:\n(.+?)(?=\n\n|$)', content, re.DOTALL)
    data['interests'] = interests_match.group(1).strip() if interests_match else ""

    # Parse references
    references_match = re.search(r'REFERENCES:\n(.+?)(?=\n\n|$)', content, re.DOTALL)
    data['references'] = references_match.group(1).strip() if references_match else ""

    # Parse competencies (for Matt's resume)
    comp_match = re.search(r'CORE COMPETENCIES:\n(.+?)(?=\nEDUCATION)', content, re.DOTALL)
    if comp_match:
        comp_text = comp_match.group(1).strip()
        data['competencies'] = [line.strip('• ').strip() for line in comp_text.split('\n') if line.strip().startswith('•')]
    else:
        data['competencies'] = []

    # Parse licenses & certifications
    data['certifications'] = []
    cert_match = re.search(r'LICENSES & CERTIFICATIONS:\n\n(.+?)(?=\nPERSONAL|$)', content, re.DOTALL)
    if cert_match:
        cert_text = cert_match.group(1).strip()
        lines = cert_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line and not line.startswith('Issued'):
                cert_name = line
                organization = ""
                date = ""

                if i + 1 < len(lines):
                    organization = lines[i + 1].strip()

                if i + 2 < len(lines) and lines[i + 2].strip().startswith('Issued'):
                    date = lines[i + 2].strip().replace('Issued ', '')

                data['certifications'].append({
                    'name': cert_name,
                    'organization': organization,
                    'date': date
                })
                i += 3
            else:
                i += 1

    # Parse personal
    personal_match = re.search(r'PERSONAL:\n(.+)', content, re.DOTALL)
    data['personal'] = personal_match.group(1).strip() if personal_match else ""

    return data


def generate_student_twocol_html(data: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Generate two-column HTML for student resume - Awesome-CV inspired styling"""

    # Build skills as comma-separated text
    skills_text = ", ".join(data.get('skills', []))

    # Build education HTML for left column
    edu_html = ""
    for edu in data['education']:
        details = edu.get('details', '')
        if details:
            details_html = f'<p class="edu-description">{details}</p>'
        else:
            details_html = ''
        edu_html += f"""
                <div class="edu-item">
                    <div class="edu-school">{edu['school']}</div>
                    <div class="edu-degree">{edu['degree']}</div>
                    <div class="edu-date">{edu['date']}</div>
                    {details_html}
                </div>"""

    # Build leadership HTML
    leadership_html = ""
    if data.get('leadership'):
        for item in data['leadership']:
            bullets_text = " ".join(item['bullets'])
            leadership_html += f"""
                <div class="leadership-item">
                    <div class="leadership-org">{item['company']}</div>
                    <div class="leadership-title">{item['title']}</div>
                    <div class="leadership-date">{item['dates']}</div>
                    <p class="leadership-description">{bullets_text}</p>
                </div>"""

    # Build activities HTML
    activities_html = ""
    if data.get('activities'):
        for activity in data['activities']:
            if activity['bullets']:
                desc = " ".join(activity['bullets'])
            else:
                desc = ""
            activities_html += f"""
                <div class="activity-item">
                    <div class="activity-name">{activity['name']}</div>
                    <p class="activity-description">{desc}</p>
                </div>"""

    # Build work experience HTML
    work_html = ""
    if data.get('work_experience'):
        for job in data['work_experience']:
            bullets_text = " ".join(job['bullets']) if job['bullets'] else ""
            work_html += f"""
                <div class="work-item">
                    <div class="work-title">{job['title']}</div>
                    <div class="work-company">{job['company']}</div>
                    <div class="work-date">{job['dates']}</div>
                    <p class="work-description">{bullets_text}</p>
                </div>"""

    # Action icons
    action_icons_html = """
        <div class="action-icons">
            <a href="resume.pdf" title="Download PDF" target="_blank">
                <img src="acrobat-logo.png" alt="Download PDF">
            </a>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']} - Resume</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

        :root {{
            --accent-color: #00A388;
            --accent-dark: #008872;
            --text-primary: #212121;
            --text-secondary: #666666;
            --text-light: #999999;
            --border-color: #e0e0e0;
            --bg-light: #f5f5f5;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @page {{
            size: letter;
            margin: 0;
        }}

        body {{
            font-family: 'Source Sans Pro', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 9pt;
            line-height: 1.4;
            color: var(--text-primary);
            background: #fff;
            width: 8.5in;
            min-height: 11in;
            max-height: 11in;
            margin: 0 auto;
            padding: 0.4in;
            overflow: hidden;
        }}

        .container {{
            display: grid;
            grid-template-columns: 1fr 200px;
            gap: 25px;
            height: 100%;
            position: relative;
        }}

        .action-icons {{
            position: absolute;
            top: 0;
            right: 0;
            display: flex;
            gap: 8px;
            z-index: 1000;
        }}

        .action-icons a {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            background: #fff;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 5px;
            transition: all 0.2s ease;
        }}

        .action-icons a:hover {{
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }}

        .action-icons img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}

        /* Left Column */
        .left-column {{
            display: flex;
            flex-direction: column;
        }}

        /* Header */
        .header {{
            margin-bottom: 14px;
            padding-bottom: 12px;
            border-bottom: 2pt solid var(--accent-color);
        }}

        .header h1 {{
            font-family: 'Roboto', sans-serif;
            font-size: 26pt;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: 2pt;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .header .tagline {{
            font-size: 9pt;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        /* Section Titles */
        .section-title {{
            font-family: 'Roboto', sans-serif;
            font-size: 11pt;
            font-weight: 700;
            color: var(--accent-color);
            text-transform: uppercase;
            letter-spacing: 1pt;
            margin-bottom: 8px;
            margin-top: 12px;
            padding-bottom: 3pt;
            border-bottom: 1pt solid var(--border-color);
        }}

        .section-title:first-of-type {{
            margin-top: 0;
        }}

        /* Education */
        .edu-item {{
            margin-bottom: 10px;
            padding-left: 10px;
            border-left: 2pt solid var(--accent-color);
        }}

        .edu-school {{
            font-family: 'Roboto', sans-serif;
            font-size: 10pt;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .edu-degree {{
            font-size: 9pt;
            font-weight: 600;
            color: var(--accent-color);
        }}

        .edu-date {{
            font-size: 8pt;
            color: var(--text-light);
            font-style: italic;
            margin-bottom: 3px;
        }}

        .edu-description {{
            font-size: 8pt;
            color: var(--text-secondary);
            line-height: 1.4;
        }}

        /* Leadership */
        .leadership-item {{
            margin-bottom: 8px;
            padding-left: 10px;
            border-left: 2pt solid var(--accent-color);
        }}

        .leadership-org {{
            font-family: 'Roboto', sans-serif;
            font-size: 9.5pt;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .leadership-title {{
            font-size: 8.5pt;
            font-weight: 600;
            color: var(--accent-color);
        }}

        .leadership-date {{
            font-size: 8pt;
            color: var(--text-light);
            font-style: italic;
            margin-bottom: 2px;
        }}

        .leadership-description {{
            font-size: 8pt;
            color: var(--text-secondary);
            line-height: 1.4;
        }}

        /* Activities */
        .activity-item {{
            margin-bottom: 8px;
            padding-left: 10px;
            border-left: 2pt solid var(--accent-color);
        }}

        .activity-name {{
            font-family: 'Roboto', sans-serif;
            font-size: 9.5pt;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 2px;
        }}

        .activity-description {{
            font-size: 8pt;
            color: var(--text-secondary);
            line-height: 1.4;
        }}

        /* Work Experience */
        .work-item {{
            margin-bottom: 8px;
            padding-left: 10px;
            border-left: 2pt solid var(--accent-color);
        }}

        .work-title {{
            font-family: 'Roboto', sans-serif;
            font-size: 9.5pt;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .work-company {{
            font-size: 8.5pt;
            font-weight: 600;
            color: var(--accent-color);
        }}

        .work-date {{
            font-size: 8pt;
            color: var(--text-light);
            font-style: italic;
            margin-bottom: 2px;
        }}

        .work-description {{
            font-size: 8pt;
            color: var(--text-secondary);
            line-height: 1.4;
        }}

        /* Right Column */
        .right-column {{
            background: var(--bg-light);
            padding: 12px;
            border-radius: 6px;
            border-top: 3pt solid var(--accent-color);
        }}

        .profile-image {{
            width: 100%;
            max-width: 160px;
            border-radius: 50%;
            margin: 0 auto 12px auto;
            display: block;
            border: 3pt solid var(--accent-color);
        }}

        .contact-block {{
            margin-bottom: 14px;
            text-align: center;
        }}

        .contact-item {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            font-size: 8pt;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }}

        .contact-item i {{
            color: var(--accent-color);
            font-size: 9pt;
            width: 12pt;
        }}

        .right-section {{
            margin-bottom: 12px;
        }}

        .right-section-title {{
            font-family: 'Roboto', sans-serif;
            font-size: 9pt;
            font-weight: 700;
            color: var(--accent-color);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
            padding-bottom: 3pt;
            border-bottom: 1pt solid var(--border-color);
        }}

        .right-section p {{
            font-size: 8pt;
            color: var(--text-secondary);
            line-height: 1.4;
        }}

        @media print {{
            body {{
                padding: 0.4in;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            .action-icons {{
                display: none !important;
            }}
        }}

        @media screen and (max-width: 768px) {{
            body {{
                width: 100%;
                min-height: auto;
                max-height: none;
                padding: 20px;
            }}
            .container {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            .right-column {{
                order: -1;
            }}
            .profile-image {{
                max-width: 120px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {action_icons_html}

        <!-- Left Column: Main Content -->
        <div class="left-column">
            <div class="header">
                <h1>{data['name']}</h1>
                <p class="tagline">{data['summary']}</p>
            </div>

            <h2 class="section-title">Education</h2>
            {edu_html}

            <h2 class="section-title">Leadership Training</h2>
            {leadership_html}

            <h2 class="section-title">Activities</h2>
            {activities_html}

            <h2 class="section-title">Work Experience</h2>
            {work_html}
        </div>

        <!-- Right Column: Contact & Skills -->
        <div class="right-column">
            <img src="{config.get('profile_image', '')}" alt="{data['name']}" class="profile-image">

            <div class="contact-block">
                <div class="contact-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>{data['location'].replace(' | ', '</span></div><div class="contact-item"><i class="fas fa-map-marker-alt"></i><span>')}</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-phone"></i>
                    <span>{data['phone']}</span>
                </div>
                <div class="contact-item">
                    <i class="fas fa-envelope"></i>
                    <span>{data['email']}</span>
                </div>
            </div>

            <div class="right-section">
                <h3 class="right-section-title">Objective</h3>
                <p>{data['summary']}</p>
            </div>

            <div class="right-section">
                <h3 class="right-section-title">Skills</h3>
                <p>{skills_text}</p>
            </div>

            <div class="right-section">
                <h3 class="right-section-title">Languages</h3>
                <p>{data.get('languages', '')}</p>
            </div>

            <div class="right-section">
                <h3 class="right-section-title">Interests</h3>
                <p>{data.get('interests', '')}</p>
            </div>

            <div class="right-section">
                <h3 class="right-section-title">References</h3>
                <p>{data.get('references', '')}</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    return html


def generate_html(data: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Generate HTML from parsed data - Awesome-CV inspired styling"""

    # Generate jobs HTML
    jobs_html = ""
    for job in data['jobs']:
        bullets_html = ""
        if job['bullets']:
            for bullet in job['bullets']:
                bullets_html += f"                    <li>{bullet}</li>\n"
            bullets_section = f"""                <ul class="job-achievements">
{bullets_html}                </ul>"""
        else:
            bullets_section = ""

        company_html = f'<span class="job-company">{job["company"]}</span>' if job['company'] else ""

        jobs_html += f"""            <div class="job">
                <div class="job-header">
                    <div class="job-title-company">
                        <span class="job-title">{job['title']}</span>
                        {company_html}
                    </div>
                    <span class="job-duration">{job['dates']}</span>
                </div>
{bullets_section}
            </div>

"""

    # Generate education HTML - Awesome-CV style
    edu_html = ""
    for edu in data['education']:
        details_html = ""
        if edu.get('details'):
            details_html = f'<div class="edu-details">{edu["details"]}</div>'

        edu_html += f"""            <div class="education-item">
                <div class="education-info">
                    <div class="degree">{edu['degree']}</div>
                    <div class="school">{edu['school']}</div>
                    {details_html}
                </div>
                <div class="edu-date">{edu['date']}</div>
            </div>
"""

    # Generate leadership HTML (for Max)
    leadership_html = ""
    if data.get('leadership'):
        for item in data['leadership']:
            bullets_html = ""
            for bullet in item['bullets']:
                bullets_html += f"                        <li>{bullet}</li>\n"
            leadership_html += f"""            <div class="job">
                <div class="job-header">
                    <div>
                        <span class="job-title">{item['title']}</span>
                        <span class="company">{item['company']}</span>
                    </div>
                    <span class="job-duration">{item['dates']}</span>
                </div>
                    <ul class="achievements">
{bullets_html}                    </ul>
            </div>

"""

    # Generate activities HTML (for Max)
    activities_html = ""
    if data.get('activities'):
        for activity in data['activities']:
            bullets_html = ""
            for bullet in activity['bullets']:
                bullets_html += f"                        <li>{bullet}</li>\n"
            if bullets_html:
                activities_html += f"""            <div class="activity">
                <div class="activity-name">{activity['name']}</div>
                    <ul class="achievements">
{bullets_html}                    </ul>
            </div>

"""
            else:
                activities_html += f"""            <div class="activity">
                <div class="activity-name">{activity['name']}</div>
            </div>

"""

    # Generate skills HTML (simple list for Max, grid for Matt)
    skills_html = ""
    if config.get('show_skills_grid') and data.get('competencies'):
        # Matt's skills grid
        skills_categories = {
            "Product Management": ["Roadmap development", "Requirement gathering", "KPI definition", "Competitive analysis", "Go-to-market strategy"],
            "Platform Experience": ["Multi-tenant SaaS platforms", "API strategy", "Developer ecosystems", "Enterprise integrations"],
            "Leadership": ["Engineering collaboration", "UX partnership", "Stakeholder management", "Executive communication"],
            "Technical Skills": ["Jira, Aha!, Confluence", "API design", "AWS, GCP, Azure", "SQL & data analytics"]
        }
        for category, skills in skills_categories.items():
            skills_list = ""
            for skill in skills:
                skills_list += f"                            <li>{skill}</li>\n"
            skills_html += f"""                    <div class="skill-category">
                        <h4>{category}</h4>
                        <ul>
{skills_list}                        </ul>
                    </div>
"""
    elif data.get('skills'):
        # Max's simple skills list
        for skill in data['skills']:
            skills_html += f"                <li>{skill}</li>\n"

    # Generate certifications HTML - Awesome-CV style
    cert_html = ""
    if config.get('show_certifications') and data.get('certifications'):
        for cert in data['certifications']:
            cert_html += f"""            <div class="cert-item">
                <div class="cert-info">
                    <div class="cert-name">{cert['name']}</div>
                    <div class="cert-org">{cert['organization']}</div>
                </div>
                <div class="cert-date">{cert['date']}</div>
            </div>
"""

    # Generate personal section
    personal_html = ""
    if config.get('show_personal') and data.get('personal'):
        personal_html = data['personal'].replace('\n', '<br>\n                    ')

    # Build header with optional profile image - Awesome-CV style with dual locations/phones
    # Parse locations and phones (support | separator for dual values)
    locations = [loc.strip() for loc in data['location'].split('|')]
    phones = [ph.strip() for ph in data['phone'].split('|')]

    # Build contact items
    # Build location column
    location_items = ""
    for loc in locations:
        location_items += f"""                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>{loc}</span>
                    </div>
"""

    # Build phone column
    phone_items = ""
    for phone in phones:
        phone_items += f"""                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <span>{phone}</span>
                    </div>
"""

    # Build links column
    link_items = f"""                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <a href="mailto:{data['email']}">{data['email']}</a>
                    </div>
"""
    if config.get('linkedin_url'):
        linkedin_short = config['linkedin_url'].replace('https://', '').replace('http://', '').replace('www.', '')
        link_items += f"""                    <div class="contact-item">
                        <i class="fab fa-linkedin"></i>
                        <a href="{config['linkedin_url']}" target="_blank">{linkedin_short}</a>
                    </div>
"""

    # Combine into columns
    contact_items = f"""                <div class="contact-column">
{location_items}                </div>
                <div class="contact-column">
{phone_items}                </div>
                <div class="contact-column">
{link_items}                </div>
"""

    if config.get('profile_image'):
        header_content = f"""            <div class="header-top">
                <img src="{config['profile_image']}" alt="{data['name']}" class="profile-photo">
                <div>
                    <h1>{data['name']}</h1>
                    <div class="subtitle">Principal Product Manager</div>
                </div>
            </div>
            <div class="contact-info">
{contact_items}            </div>"""
    else:
        header_content = f"""            <div class="header-top">
                <div>
                    <h1>{data['name']}</h1>
                    <div class="subtitle">Product Manager</div>
                </div>
            </div>
            <div class="contact-info">
{contact_items}            </div>"""

    # Build action icons
    action_icons = ""
    icons_list = []
    icons_list.append("""            <a href="resume.pdf" title="Download PDF" target="_blank">
                <img src="acrobat-logo.png" alt="Download PDF">
            </a>""")
    if config.get('linkedin_url'):
        icons_list.append(f"""            <a href="{config['linkedin_url']}" title="LinkedIn Profile" target="_blank">
                <img src="linkedin-logo.png" alt="LinkedIn">
            </a>""")
    action_icons = "\n".join(icons_list)

    # Build sections based on resume type
    sections_html = ""

    # Summary section (all resumes) - Awesome-CV style
    if data.get('summary'):
        sections_html += f"""        <section class="section summary">
            <h2 class="section-title">Summary</h2>
            <p>{data['summary']}</p>
        </section>

"""

    # Education section (student resumes show this prominently)
    if config['resume_type'] == 'student':
        sections_html += f"""            <section class="education-section">
                <h2 class="section-title">Education</h2>
{edu_html}            </section>

"""

    # Leadership Training (for Max)
    if data.get('leadership'):
        sections_html += f"""            <section class="leadership-section">
                <h2 class="section-title">Leadership Training</h2>
{leadership_html}            </section>

"""

    # Work Experience (professional resumes) - Awesome-CV style
    if data.get('jobs') and config['resume_type'] == 'professional':
        sections_html += f"""        <section class="section">
            <h2 class="section-title">Experience</h2>
{jobs_html}        </section>

"""

    # Skills section - Awesome-CV style
    if config.get('show_skills_grid') and skills_html:
        sections_html += f"""        <section class="section">
            <h2 class="section-title">Core Competencies</h2>
            <div class="skills-grid">
{skills_html}            </div>
        </section>

"""
    elif data.get('skills'):
        sections_html += f"""        <section class="section">
            <h2 class="section-title">Skills</h2>
            <ul class="skills-list">
{skills_html}            </ul>
        </section>

"""

    # Activities (for Max)
    if data.get('activities'):
        sections_html += f"""            <section class="activities-section">
                <h2 class="section-title">Activities</h2>
{activities_html}            </section>

"""

    # Languages (for Max)
    if data.get('languages'):
        sections_html += f"""            <section class="languages-section">
                <h2 class="section-title">Languages</h2>
                <p>{data['languages']}</p>
            </section>

"""

    # Education & Certifications (professional resumes) - Awesome-CV style
    if config['resume_type'] == 'professional':
        sections_html += f"""        <section class="section">
            <h2 class="section-title">Education</h2>
{edu_html}        </section>

"""
        if cert_html:
            sections_html += f"""        <section class="section">
            <h2 class="section-title">Certifications</h2>
{cert_html}        </section>

"""

    # Personal section
    if personal_html:
        sections_html += f"""            <section>
                <div class="personal">
                    {personal_html}
                </div>
            </section>
"""

    # Complete HTML template - Awesome-CV inspired styling
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']} - Resume</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

        :root {{
            --accent-color: #00A388;
            --accent-dark: #008872;
            --text-primary: #212121;
            --text-secondary: #666666;
            --text-light: #999999;
            --border-color: #e0e0e0;
            --bg-light: #f5f5f5;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Source Sans Pro', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.5;
            color: var(--text-primary);
            font-weight: 400;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.35in;
            background: #ffffff;
            font-size: 10pt;
        }}

        .container {{
            position: relative;
        }}

        .action-icons {{
            position: absolute;
            top: 0;
            right: 0;
            display: flex;
            gap: 10px;
            z-index: 1000;
        }}

        .action-icons a {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            transition: all 0.2s ease;
            text-decoration: none;
            padding: 6px;
        }}

        .action-icons a:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            border-color: var(--accent-color);
        }}

        .action-icons img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}

        .header {{
            text-align: center;
            padding-bottom: 12pt;
            margin-bottom: 10pt;
            border-bottom: 2pt solid var(--accent-color);
            page-break-inside: avoid;
            page-break-after: avoid;
        }}

        .header-top {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20pt;
            margin-bottom: 12pt;
        }}

        .profile-photo {{
            width: 75pt;
            height: 75pt;
            border-radius: 50%;
            object-fit: cover;
            border: 3pt solid var(--accent-color);
        }}

        .header h1 {{
            font-family: 'Roboto', sans-serif;
            font-size: 28pt;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: 2pt;
            text-transform: uppercase;
            margin-bottom: 4pt;
        }}

        .header .subtitle {{
            font-size: 12pt;
            font-weight: 400;
            color: var(--accent-color);
            letter-spacing: 1pt;
            text-transform: uppercase;
            margin-bottom: 14pt;
        }}

        .contact-info {{
            display: flex;
            justify-content: center;
            gap: 0;
        }}

        .contact-column {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 0 16pt;
            border-right: 1pt solid var(--border-color);
        }}

        .contact-column:last-child {{
            border-right: none;
        }}

        .contact-item {{
            display: flex;
            align-items: center;
            gap: 6pt;
            color: var(--text-secondary);
            font-size: 9pt;
            font-weight: 400;
            margin-bottom: 2pt;
        }}

        .contact-item:last-child {{
            margin-bottom: 0;
        }}

        .contact-item i {{
            color: var(--accent-color);
            font-size: 9pt;
            width: 12pt;
            text-align: center;
        }}

        .contact-item a {{
            color: var(--text-secondary);
            text-decoration: none;
        }}

        .contact-item a:hover {{
            color: var(--accent-color);
        }}

        .section {{
            margin-bottom: 14pt;
        }}

        .section-title {{
            font-family: 'Roboto', sans-serif;
            font-size: 12pt;
            font-weight: 700;
            color: var(--accent-color);
            text-transform: uppercase;
            letter-spacing: 1.5pt;
            margin-bottom: 10pt;
            padding-bottom: 4pt;
            border-bottom: 1pt solid var(--border-color);
        }}

        .summary {{
            margin-bottom: 12pt;
            page-break-after: avoid;
        }}

        .summary p {{
            font-size: 10pt;
            line-height: 1.5;
            color: var(--text-secondary);
            text-align: justify;
            padding: 6pt 0;
        }}

        .job {{
            margin-bottom: 10pt;
            page-break-inside: avoid;
        }}

        .job:last-child {{
            margin-bottom: 0;
        }}

        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            margin-bottom: 4pt;
        }}

        .job-title-company {{
            display: flex;
            align-items: baseline;
            gap: 8pt;
            flex-wrap: wrap;
        }}

        .job-title {{
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            font-size: 11pt;
            color: var(--text-primary);
        }}

        .job-company {{
            font-weight: 600;
            font-size: 10pt;
            color: var(--accent-color);
        }}

        .job-duration {{
            font-size: 9pt;
            font-weight: 400;
            color: var(--text-light);
            font-style: italic;
        }}

        .job-achievements {{
            margin: 6pt 0 0 0;
            padding-left: 16pt;
            list-style: none;
        }}

        .job-achievements li {{
            position: relative;
            margin-bottom: 4pt;
            font-size: 9.5pt;
            line-height: 1.5;
            color: var(--text-secondary);
        }}

        .job-achievements li::before {{
            content: "\\f054";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 6pt;
            color: var(--accent-color);
            position: absolute;
            left: -14pt;
            top: 4pt;
        }}

        .skills-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8pt;
            list-style: none;
        }}

        .skills-list li {{
            background: var(--bg-light);
            border: 1pt solid var(--border-color);
            border-left: 3pt solid var(--accent-color);
            padding: 5pt 12pt;
            font-size: 9pt;
            font-weight: 500;
            color: var(--text-secondary);
            border-radius: 0 4pt 4pt 0;
        }}

        .education-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 8pt;
            padding: 8pt 12pt;
            background: var(--bg-light);
            border-left: 3pt solid var(--accent-color);
        }}

        .education-info {{
            flex: 1;
        }}

        .degree {{
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            font-size: 10.5pt;
            color: var(--text-primary);
        }}

        .school {{
            font-size: 9.5pt;
            font-weight: 600;
            color: var(--accent-color);
            margin-top: 2pt;
        }}

        .edu-date {{
            font-size: 9pt;
            font-weight: 400;
            color: var(--text-light);
            font-style: italic;
        }}

        .edu-details {{
            font-size: 9pt;
            color: var(--text-secondary);
            margin-top: 4pt;
            font-style: italic;
        }}

        .cert-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 8pt;
            padding: 8pt 12pt;
            background: var(--bg-light);
            border-left: 3pt solid var(--accent-color);
        }}

        .cert-info {{
            flex: 1;
        }}

        .cert-name {{
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            font-size: 10.5pt;
            color: var(--text-primary);
        }}

        .cert-org {{
            font-size: 9.5pt;
            font-weight: 600;
            color: var(--accent-color);
            margin-top: 2pt;
        }}

        .cert-date {{
            font-size: 9pt;
            font-weight: 400;
            color: var(--text-light);
            font-style: italic;
        }}

        .personal {{
            background: var(--bg-light);
            padding: 12pt 14pt;
            border-left: 3pt solid var(--accent-color);
            font-style: italic;
            color: var(--text-secondary);
            font-size: 10pt;
            line-height: 1.6;
        }}

        @media print {{
            body {{
                padding: 0;
                background: white;
            }}
            .action-icons {{
                display: none !important;
            }}
            .section {{
                page-break-inside: avoid;
            }}
        }}

        @media screen and (max-width: 768px) {{
            body {{
                padding: 20px;
                font-size: 9pt;
            }}
            .header h1 {{
                font-size: 24pt;
                letter-spacing: 1pt;
            }}
            .header .subtitle {{
                font-size: 10pt;
            }}
            .header-top {{
                flex-direction: column;
                gap: 12pt;
            }}
            .profile-photo {{
                width: 70pt;
                height: 70pt;
            }}
            .contact-info {{
                flex-direction: column;
                gap: 8pt;
            }}
            .contact-column {{
                border-right: none;
                border-bottom: 1pt solid var(--border-color);
                padding: 6pt 0;
            }}
            .contact-column:last-child {{
                border-bottom: none;
            }}
            .job-header {{
                flex-direction: column;
                gap: 4pt;
            }}
            .education-item, .cert-item {{
                flex-direction: column;
                gap: 4pt;
            }}
        }}

        @media screen and (max-width: 480px) {{
            body {{
                padding: 15px;
                font-size: 8.5pt;
            }}
            .header h1 {{
                font-size: 20pt;
            }}
            .section-title {{
                font-size: 11pt;
            }}
            .skills-list {{
                gap: 6pt;
            }}
            .skills-list li {{
                padding: 4pt 8pt;
                font-size: 8pt;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="action-icons">
{action_icons}
        </div>
        <header class="header">
{header_content}
        </header>

        <div class="content">
{sections_html}        </div>
    </div>
</body>
</html>"""

    return html_template


def generate_pdf(output_dir: str):
    """Generate PDF from HTML using Chrome headless"""
    html_path = os.path.join(output_dir, 'index.html')
    pdf_path = os.path.join(output_dir, 'resume.pdf')

    methods = [
        ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless', '--disable-gpu', f'--print-to-pdf={pdf_path}', '--no-margins', '--no-pdf-header-footer', html_path],
        ['google-chrome', '--headless', '--disable-gpu', f'--print-to-pdf={pdf_path}', '--no-margins', '--no-pdf-header-footer', html_path],
        ['chromium-browser', '--headless', '--disable-gpu', f'--print-to-pdf={pdf_path}', '--no-margins', '--no-pdf-header-footer', html_path],
    ]

    for method in methods:
        try:
            result = subprocess.run(method, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  PDF generated using {method[0]}")
                return True
        except FileNotFoundError:
            continue

    print(f"  Could not generate PDF automatically for {output_dir}")
    return False


def generate_index_page(script_dir: str, hugo_static_resume: str):
    """Generate the main index page for /resume/"""
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reider Family Resumes</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600&display=swap');

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #000000;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #ffffff;
        }

        h1 {
            font-family: 'Crimson Text', serif;
            font-size: 28pt;
            font-weight: 700;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #000000;
            letter-spacing: -0.5pt;
        }

        .resume-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .resume-item {
            margin-bottom: 20px;
            padding: 20px 25px;
            background: #f7f7f7;
            border: 1px solid #cccccc;
            border-left: 4px solid #000000;
            transition: all 0.2s ease;
        }

        .resume-item:hover {
            background: #f0f0f0;
            transform: translateX(5px);
        }

        .resume-item a {
            text-decoration: none;
            color: inherit;
            display: block;
        }

        .resume-name {
            font-family: 'Crimson Text', serif;
            font-size: 16pt;
            font-weight: 600;
            color: #000000;
            margin-bottom: 5px;
        }

        .resume-title {
            font-size: 11pt;
            color: #555555;
        }

        .resume-links {
            margin-top: 10px;
            display: flex;
            gap: 15px;
        }

        .resume-links a {
            font-size: 10pt;
            color: #0066cc;
            text-decoration: none;
        }

        .resume-links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Reider Family Resumes</h1>
    <ul class="resume-list">
        <li class="resume-item">
            <a href="matt/">
                <div class="resume-name">Matthew Reider</div>
                <div class="resume-title">Principal Product Manager</div>
            </a>
            <div class="resume-links">
                <a href="matt/">View Resume</a>
                <a href="matt/resume.pdf">Download PDF</a>
            </div>
        </li>
        <li class="resume-item">
            <a href="alison/">
                <div class="resume-name">Alison S. Cohen</div>
                <div class="resume-title">Senior People Experience Business Partner</div>
            </a>
            <div class="resume-links">
                <a href="alison/">View Resume</a>
                <a href="alison/resume.pdf">Download PDF</a>
            </div>
        </li>
        <li class="resume-item">
            <a href="max/">
                <div class="resume-name">Max Reider</div>
                <div class="resume-title">University Student - Business Management & Psychology</div>
            </a>
            <div class="resume-links">
                <a href="max/">View Resume</a>
                <a href="max/resume.pdf">Download PDF</a>
            </div>
        </li>
    </ul>
</body>
</html>"""

    index_path = os.path.join(hugo_static_resume, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"Index page created at: {index_path}")


def generate_resume(person: str, script_dir: str, hugo_static_resume: str):
    """Generate resume for a specific person"""
    config = PERSON_CONFIGS[person]
    input_file = os.path.join(script_dir, config['input_file'])
    output_subdir = os.path.join(hugo_static_resume, config['output_dir'])

    print(f"\n{'='*50}")
    print(f"Generating resume for: {person.upper()}")
    print(f"{'='*50}")

    # Create output directory
    os.makedirs(output_subdir, exist_ok=True)

    # Parse resume data
    print(f"  Reading {config['input_file']}...")
    data = parse_resume_data(input_file)

    # Generate HTML based on resume type
    print("  Generating HTML...")
    if config['resume_type'] == 'student_twocol':
        html = generate_student_twocol_html(data, config)
    else:
        html = generate_html(data, config)

    # Write index.html
    html_path = os.path.join(output_subdir, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  HTML written to: {html_path}")

    # Copy assets
    assets = ['acrobat-logo.png', 'linkedin-logo.png']
    if config.get('profile_image'):
        assets.append(config['profile_image'])

    for asset in assets:
        src = os.path.join(script_dir, asset)
        if os.path.exists(src):
            dst = os.path.join(output_subdir, asset)
            shutil.copy2(src, dst)
            print(f"  Copied: {asset}")

    # Generate PDF
    print("  Generating PDF...")
    generate_pdf(output_subdir)

    print(f"  Resume generated for {person}")


def main():
    """Main function to generate all resumes"""
    parser = argparse.ArgumentParser(description='Generate resumes for the Reider family')
    parser.add_argument('--person', choices=['matt', 'max', 'alison', 'all'], default='all',
                        help='Which person to generate resume for (default: all)')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    hugo_static_resume = os.path.join(script_dir, '..', 'static', 'resume')

    # Create main resume directory
    os.makedirs(hugo_static_resume, exist_ok=True)

    try:
        if args.person == 'all':
            # Generate all resumes
            for person in PERSON_CONFIGS.keys():
                generate_resume(person, script_dir, hugo_static_resume)

            # Generate index page
            print(f"\n{'='*50}")
            print("Generating index page...")
            print(f"{'='*50}")
            generate_index_page(script_dir, hugo_static_resume)
        else:
            # Generate single resume
            generate_resume(args.person, script_dir, hugo_static_resume)

        print(f"\n{'='*50}")
        print("Resume generation complete!")
        print(f"Output directory: {hugo_static_resume}")
        print(f"{'='*50}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
