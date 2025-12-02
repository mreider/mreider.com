#!/usr/bin/env python3
"""
Resume Generator Script
Converts resume.txt to styled HTML resume and PDF
"""

import re
import subprocess
import sys
from typing import List, Dict, Any

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
    summary_match = re.search(r'SUMMARY:\n(.+?)(?=\n[A-Z])', content, re.DOTALL)
    data['summary'] = summary_match.group(1).strip()

    # Parse transition note
    transition_match = re.search(r'TRANSITION NOTE:\n(.+)', content)
    data['transition'] = transition_match.group(1) if transition_match else ""

    # Parse jobs
    data['jobs'] = []

    # Pattern for jobs with bullets (HR roles)
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

    # Pattern for jobs without bullets (counseling roles)
    job_without_bullets_pattern = r'JOB TITLE: (.+?)\nCOMPANY: (.+?)\nDATES: (.+?)(?=\n\n|\nJOB TITLE|\nMATERNITY|\nEARLY|\nCORE|\nEDUCATION|\nPERSONAL|$)'
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



    # Parse competencies
    comp_match = re.search(r'CORE COMPETENCIES:\n(.+?)(?=\n[A-Z])', content, re.DOTALL)
    if comp_match:
        comp_text = comp_match.group(1).strip()
        data['competencies'] = [line.strip('• ').strip() for line in comp_text.split('\n') if line.strip().startswith('•')]
    else:
        data['competencies'] = []

    # Parse education from text file
    data['education'] = []
    edu_match = re.search(r'EDUCATION:\n\n(.+?)(?=\n[A-Z][A-Z\s&]+:|$)', content, re.DOTALL)
    if edu_match:
        edu_text = edu_match.group(1).strip()
        lines = edu_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # New format: degree comes first
            if line and not line.startswith('Graduated') and not line.startswith('Pupil Personnel'):
                degree = line
                school = ""
                date = ""
                details = ""

                # Get school from next line
                if i + 1 < len(lines):
                    school = lines[i + 1].strip()

                # Get graduation date from next line
                if i + 2 < len(lines) and lines[i + 2].strip().startswith('Graduated'):
                    date = lines[i + 2].strip().replace('Graduated ', '')
                    i += 1  # Skip the date line

                # Check for additional details (like credentials)
                if i + 2 < len(lines) and lines[i + 2].strip() and not lines[i + 2].strip().startswith('Bachelor') and not lines[i + 2].strip().startswith('Master'):
                    details = lines[i + 2].strip()
                    i += 1  # Skip the details line

                data['education'].append({
                    'degree': degree,
                    'school': school,
                    'date': date,
                    'details': details if details else None
                })
                i += 2  # Skip school line
            else:
                i += 1

    # Parse licenses & certifications
    data['certifications'] = []
    cert_match = re.search(r'LICENSES & CERTIFICATIONS:\n\n(.+?)(?=\n[A-Z][A-Z\s&]+:|$)', content, re.DOTALL)
    if cert_match:
        cert_text = cert_match.group(1).strip()
        lines = cert_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # New format: certification name comes first
            if line and not line.startswith('Issued'):
                cert_name = line
                organization = ""
                date = ""

                # Get organization from next line
                if i + 1 < len(lines):
                    organization = lines[i + 1].strip()

                # Get issue date from next line
                if i + 2 < len(lines) and lines[i + 2].strip().startswith('Issued'):
                    date = lines[i + 2].strip().replace('Issued ', '')

                data['certifications'].append({
                    'name': cert_name,
                    'organization': organization,
                    'date': date
                })
                i += 3  # Skip organization and date lines
            else:
                i += 1

    # Parse personal
    personal_match = re.search(r'PERSONAL:\n(.+)', content, re.DOTALL)
    data['personal'] = personal_match.group(1).strip() if personal_match else ""

    return data

def generate_html(data: Dict[str, Any]) -> str:
    """Generate HTML from parsed data"""

    # Generate jobs HTML
    jobs_html = ""
    for job in data['jobs']:
        bullets_html = ""
        if job['bullets']:  # Only add bullets if they exist
            for bullet in job['bullets']:
                bullets_html += f"                        <li>{bullet}</li>\n"
            bullets_section = f"""                    <ul class="achievements">
{bullets_html}                    </ul>"""
        else:
            bullets_section = ""

        jobs_html += f"""            <div class="job">
                <div class="job-header">
                    <div>
                        <span class="job-title">{job['title']}</span>
                        <span class="company">{job['company']}</span>
                    </div>
                    <span class="job-duration">{job['dates']}</span>
                </div>
{bullets_section}
            </div>

"""

    # Generate skills HTML in grid format
    skills_html = ""
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

    # Generate education HTML
    edu_html = ""
    for edu in data['education']:
        location_date = f"{edu['date']}"
        edu_html += f"""                <div class="education-item">
                    <div class="degree">{edu['degree']}</div>
                    <div class="school">{edu['school']}</div>
                    <div class="location">{location_date}</div>
                </div>
"""

    # Generate certifications HTML
    cert_html = ""
    for cert in data['certifications']:
        cert_html += f"""                <div class="cert-item">
                    <div class="cert-name">{cert['name']}</div>
                    <div class="cert-org">{cert['organization']}</div>
                    <div class="cert-date">{cert['date']}</div>
                </div>
"""

    # Process personal section to replace newlines with <br>
    personal_html = data['personal'].replace('\n', '<br>\n                    ')

    # Complete HTML template with styling adapted from alison.red
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']} - Resume</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600&display=swap');

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.45;
            color: #000000;
            font-weight: 400;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.4in 0.5in 0.2in 0.5in;
            background: #ffffff;
            font-size: 11pt;
        }}

        .container {{
            background: #ffffff;
            overflow: hidden;
            position: relative;
        }}

        .header {{
            padding: 18pt 32pt 14pt 32pt;
            background: #ffffff;
            color: #000000;
            position: relative;
            border-bottom: 1.5pt solid #000000;
            margin-bottom: 14pt;
        }}

        .header-content {{
            display: flex;
            align-items: center;
            gap: 24pt;
        }}

        .header img {{
            width: 100pt;
            height: 100pt;
            border-radius: 50%;
            object-fit: cover;
            border: 2pt solid #cccccc;
        }}

        .header-text {{
            flex: 1;
        }}

        .header h1 {{
            margin: 0 0 10pt 0;
            color: #000000;
            font-family: 'Crimson Text', serif;
            font-size: 22pt;
            font-weight: 700;
            letter-spacing: -0.8pt;
        }}

        .contact-info {{
            display: flex;
            flex-wrap: wrap;
            gap: 18pt;
            margin-top: 8pt;
        }}

        .contact-info span {{
            color: #555555;
            font-size: 11pt;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 5pt;
            padding: 3pt 0;
        }}

        .content {{
            padding: 0pt 32pt 0pt 32pt;
        }}

        .section {{
            margin-bottom: 18pt;
        }}

        .section:last-child {{
            margin-bottom: 0pt;
        }}

        .section-title {{
            color: #000000;
            font-family: 'Crimson Text', serif;
            font-size: 14pt;
            font-weight: 700;
            margin: 16pt 0 10pt 0;
            padding-bottom: 5pt;
            border-bottom: 1.5pt solid #000000;
            letter-spacing: -0.3pt;
            position: relative;
        }}

        .section-title:first-child {{
            margin-top: 0;
        }}

        .summary {{
            background: #f7f7f7;
            padding: 14pt 16pt;
            margin-bottom: 18pt;
            border-left: 4pt solid #000000;
            border-top: 0.75pt solid #cccccc;
            border-bottom: 0.75pt solid #cccccc;
        }}

        .summary p {{
            margin: 0;
            font-size: 10.5pt;
            line-height: 1.5;
            color: #222222;
            font-weight: 400;
            font-style: italic;
        }}

        .job {{
            margin-bottom: 14pt;
            padding: 0;
            background: #ffffff;
        }}

        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            margin-bottom: 9pt;
        }}

        .job-title {{
            font-weight: 600;
            color: #000000;
            font-size: 12pt;
            font-family: 'Crimson Text', serif;
            line-height: 1.2;
        }}

        .company {{
            color: #555555;
            font-weight: 500;
            padding-left: 10pt;
            font-size: 10pt;
        }}

        .job-duration {{
            color: #555555;
            font-size: 10pt;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
        }}

        .achievements {{
            margin: 0 0 8pt 0;
            padding-left: 20pt;
            list-style: disc;
        }}

        .achievements li {{
            margin-bottom: 5pt;
            line-height: 1.5;
            color: #333333;
            font-size: 10pt;
            font-weight: 400;
        }}

        .education-item {{
            margin-bottom: 6pt;
            padding: 10pt 12pt;
            background: #f7f7f7;
            border: 1pt solid #cccccc;
            border-left: 4pt solid #000000;
        }}

        .education-item:last-child {{
            margin-bottom: 10pt;
        }}

        .degree {{
            font-weight: 600;
            color: #000000;
            font-size: 11pt;
            font-family: 'Crimson Text', serif;
            margin-bottom: 4pt;
            line-height: 1.2;
        }}

        .school {{
            color: #555555;
            font-weight: 600;
            margin-bottom: 3pt;
            text-transform: uppercase;
            font-size: 8.5pt;
            letter-spacing: 0.8pt;
        }}

        .location {{
            color: #000000;
            font-size: 8.5pt;
            font-weight: 600;
        }}

        .cert-item {{
            margin-bottom: 6pt;
            padding: 10pt 12pt;
            background: #f7f7f7;
            border: 1pt solid #cccccc;
            border-left: 4pt solid #000000;
        }}

        .cert-item:last-child {{
            margin-bottom: 0pt;
        }}

        .cert-name {{
            font-weight: 600;
            color: #000000;
            font-size: 11pt;
            font-family: 'Crimson Text', serif;
            margin-bottom: 4pt;
        }}

        .cert-org {{
            color: #555555;
            font-weight: 500;
            font-size: 9.5pt;
            margin-bottom: 2pt;
        }}

        .cert-date {{
            color: #000000;
            font-size: 8.5pt;
            font-weight: 600;
        }}

        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10pt;
        }}

        .skill-category {{
            background: #f7f7f7;
            padding: 10pt 12pt;
            border: 1pt solid #cccccc;
            border-left: 4pt solid #000000;
        }}

        .skill-category h4 {{
            color: #000000;
            margin-bottom: 6pt;
            font-size: 10.5pt;
            font-family: 'Crimson Text', serif;
            font-weight: 600;
        }}

        .skill-category ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .skill-category li {{
            padding: 2pt 0;
            color: #333333;
            font-size: 9.5pt;
        }}

        .personal {{
            background: #f7f7f7;
            padding: 14pt 16pt;
            border-left: 4pt solid #000000;
            border-top: 0.75pt solid #cccccc;
            border-bottom: 0.75pt solid #cccccc;
            font-style: italic;
            color: #222222;
            font-size: 10.5pt;
            line-height: 1.8;
        }}

        .personal::after {{
            content: '';
            display: table;
            clear: both;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
        }}

        @media screen and (max-width: 768px) {{
            body {{
                padding: 0.2in 0.3in;
                font-size: 10pt;
            }}

            .header {{
                padding: 12pt 16pt 10pt 16pt;
            }}

            .header-content {{
                flex-direction: column;
                text-align: center;
                gap: 12pt;
            }}

            .header img {{
                width: 80pt;
                height: 80pt;
                align-self: center;
            }}

            .header h1 {{
                font-size: 20pt;
                text-align: center;
            }}

            .contact-info {{
                justify-content: center;
                gap: 12pt;
            }}

            .contact-info span {{
                font-size: 10pt;
            }}

            .content {{
                padding: 0pt 16pt;
            }}

            .section-title {{
                font-size: 13pt;
            }}

            .summary {{
                padding: 12pt 14pt;
                margin-bottom: 16pt;
            }}

            .summary p {{
                font-size: 10pt;
            }}

            .job-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 4pt;
            }}

            .job-title {{
                font-size: 11pt;
            }}

            .company {{
                font-size: 9pt;
                padding-left: 0;
            }}

            .job-duration {{
                font-size: 9pt;
                color: #666666;
                font-weight: 600;
            }}

            .achievements li {{
                font-size: 9pt;
                margin-bottom: 4pt;
            }}

            .education-item {{
                padding: 10pt 12pt;
            }}

            .degree {{
                font-size: 11pt;
            }}

            .school {{
                font-size: 8pt;
            }}
        }}

        @media screen and (max-width: 480px) {{
            body {{
                padding: 0.15in 0.2in;
                font-size: 9pt;
            }}

            .header {{
                padding: 10pt 12pt 8pt 12pt;
            }}

            .header h1 {{
                font-size: 18pt;
            }}

            .contact-info {{
                flex-direction: column;
                gap: 8pt;
            }}

            .content {{
                padding: 0pt 12pt;
            }}

            .section-title {{
                font-size: 12pt;
            }}

            .job-title {{
                font-size: 10pt;
            }}

            .company {{
                font-size: 8pt;
            }}

            .job-duration {{
                font-size: 8pt;
            }}

            .achievements li {{
                font-size: 8pt;
            }}

            .degree {{
                font-size: 10pt;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <img src="matt-profile-image.jpeg" alt="{data['name']}">
                <div class="header-text">
                    <h1>{data['name']}</h1>
                    <div class="contact-info">
                        <span>{data['location']}</span>
                        <span>{data['email']}</span>
                        <span>{data['phone']}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="content">
            <section class="summary">
                <h2 class="section-title">Professional Summary</h2>
                <p>
                    {data['summary']}
                </p>
            </section>

            <section>
                <h2 class="section-title">Work Experience</h2>

{jobs_html}            </section>

            <section>
                <h2 class="section-title">Core Competencies</h2>
                <div class="skills-grid">
{skills_html}                </div>
            </section>

            <section>
                <h2 class="section-title">Education & Certifications</h2>
{edu_html}
{cert_html}            </section>

            <section>
                <div class="personal">
                    {personal_html}
                </div>
            </section>
        </div>
    </div>
</body>
</html>"""

    return html_template

def generate_pdf():
    """Generate PDF from HTML using various methods"""

    methods = [
        # Try Chrome/Chromium headless first - macOS path
        ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless', '--disable-gpu', '--print-to-pdf=resume.pdf', '--no-margins', '--no-pdf-header-footer', 'index.html'],
        # Try standard PATH locations
        ['google-chrome', '--headless', '--disable-gpu', '--print-to-pdf=resume.pdf', '--no-margins', '--no-pdf-header-footer', 'index.html'],
        ['chromium-browser', '--headless', '--disable-gpu', '--print-to-pdf=resume.pdf', '--no-margins', '--no-pdf-header-footer', 'index.html'],
        ['chrome', '--headless', '--disable-gpu', '--print-to-pdf=resume.pdf', '--no-margins', '--no-pdf-header-footer', 'index.html'],
    ]

    for method in methods:
        try:
            result = subprocess.run(method, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ PDF generated using {method[0]}")
                return True
        except FileNotFoundError:
            continue

    print("⚠️  Could not generate PDF automatically.")
    print("   Please print index.html to PDF manually:")
    print("   1. Open index.html in Chrome/Safari/Firefox")
    print("   2. Press Ctrl+P (or Cmd+P)")
    print("   3. Choose 'Save as PDF'")
    print("   4. Save as 'resume.pdf'")
    return False

def main():
    """Main function to generate resume"""
    import os
    import shutil
    
    try:
        # Determine paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        hugo_static_resume = os.path.join(script_dir, '..', 'static', 'resume')
        
        print("Reading resume data...")
        data = parse_resume_data('matt_resume.txt')

        print("Generating HTML...")
        html = generate_html(data)

        # Add action icons to HTML
        html = html.replace(
            '<body>\n    <div class="container">\n        <div class="header">',
            '''<body>
    <div class="container">
        <div class="action-icons">
            <a href="resume.pdf" title="Download PDF" target="_blank">
                <img src="acrobat-logo.png" alt="Download PDF">
            </a>
            <a href="https://linkedin.com/in/mreider" title="LinkedIn Profile" target="_blank">
                <img src="linkedin-logo.png" alt="LinkedIn">
            </a>
        </div>
        <div class="header">'''
        )
        
        # Add action icons CSS before .content
        action_icons_css = '''
        .action-icons {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 12px;
            z-index: 1000;
        }

        .action-icons a {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
            text-decoration: none;
            padding: 6px;
        }

        .action-icons a:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .action-icons img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .content {'''
        
        html = html.replace('        .content {', action_icons_css)
        
        # Update print media query to hide action icons
        html = html.replace(
            '        @media print {\n            body {\n                background: white;\n                padding: 0;\n            }',
            '''        @media print {
            body {
                background: white;
                padding: 0;
            }
            .action-icons {
                display: none !important;
            }'''
        )

        print("Writing index.html...")
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print("✓ HTML resume generated successfully!")

        print("Generating PDF...")
        generate_pdf()

        # Copy files to Hugo static directory
        print("Copying files to Hugo static/resume directory...")
        os.makedirs(hugo_static_resume, exist_ok=True)
        
        files_to_copy = [
            'index.html',
            'resume.pdf',
            'matt-profile-image.jpeg',
            'acrobat-logo.png',
            'linkedin-logo.png'
        ]
        
        for filename in files_to_copy:
            src = os.path.join(script_dir, filename)
            if os.path.exists(src):
                dst = os.path.join(hugo_static_resume, filename)
                shutil.copy2(src, dst)
                print(f"  ✓ Copied {filename}")
            else:
                print(f"  ⚠ Warning: {filename} not found")

        print("✓ Resume generation complete!")
        print(f"Files created in: {script_dir}")
        print(f"Files copied to: {hugo_static_resume}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())