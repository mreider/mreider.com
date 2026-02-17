# Resume Generator

Generates HTML, PDF, and DOCX resumes from text files and publishes to Hugo site.

## Supported People

- **Matt** - Professional resume with certifications and personal section
- **Alison** - Professional HR resume with work experience and skills

## Files

- `matt_resume.txt` - Matt's resume content
- `alison_resume.txt` - Alison's resume content
- `generate.py` - Generator script
- `matt-profile-image.jpeg` - Matt's profile photo
- `acrobat-logo.png` - PDF download icon
- `linkedin-logo.png` - LinkedIn icon

## Usage

Generate all resumes:
```bash
cd resume-generator
python3 generate.py
```

Generate a specific person's resume:
```bash
python3 generate.py --person matt
python3 generate.py --person alison
```

Then rebuild Hugo site:
```bash
cd ..
hugo
```

## What it does

1. Parses the text file for the specified person(s)
2. Generates ATS-friendly HTML
3. Creates PDF using Chrome headless
4. Creates Word document (.docx)
5. Copies all files to `../static/resume/{person}/`

## Resume format

See text files for structure. Key sections:

### Common
- NAME, PHONE, EMAIL, LOCATION
- SUMMARY
- JOB TITLE, COMPANY, DATES (with optional bullets)
- EDUCATION (degree, school, date)
- SKILLS (simple list)

### Matt only
- LICENSES & CERTIFICATIONS (name, org, date)
- PERSONAL

## Output URLs

- Matt's resume: `https://mreider.com/resume/matt/`
- Alison's resume: `https://mreider.com/resume/alison/`

## Configuration

Person-specific settings are in `PERSON_CONFIGS` in `generate.py`:
- `input_file` - Source text file
- `profile_image` - Profile photo filename (or None)
- `linkedin_url` - LinkedIn profile URL (or None)
- `output_dir` - Output subdirectory name
- `resume_type` - 'professional' or 'student'
- `show_skills_grid` - Show skills in grid format
- `show_certifications` - Include certifications section
- `show_personal` - Include personal section
