# Resume Generator

Generates HTML and PDF resumes for the Reider family from text files and publishes to Hugo site.

## Supported People

- **Matt** - Professional resume with skills grid, certifications, and personal section
- **Max** - Student resume with education, leadership training, activities, and skills
- **Alison** - Professional HR resume with work experience and education

## Files

- `matt_resume.txt` - Matt's resume content
- `max_resume.txt` - Max's resume content
- `alison_resume.txt` - Alison's resume content
- `generate.py` - Generator script
- `matt-profile-image.jpeg` - Matt's profile photo
- `alison.jpeg` - Alison's profile photo
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
python3 generate.py --person max
python3 generate.py --person alison
```

Then rebuild Hugo site:
```bash
cd ..
hugo
```

## What it does

1. Parses the text file for the specified person(s)
2. Generates styled HTML with:
   - Profile photo (if available)
   - PDF download button
   - LinkedIn profile button (if available)
3. Creates PDF using Chrome headless
4. Copies all files to `../static/resume/{person}/`:
   - `index.html`
   - `resume.pdf`
   - Profile image and icons
5. Creates index page at `../static/resume/index.html`

## Resume format

See text files for structure. Key sections:

### Common
- NAME, PHONE, EMAIL, LOCATION
- SUMMARY
- JOB TITLE, COMPANY, DATES (with optional bullets)
- EDUCATION (degree, school, date)

### Matt only
- CORE COMPETENCIES (automatically organized into grid)
- LICENSES & CERTIFICATIONS (name, org, date)
- PERSONAL

### Max only
- LEADERSHIP TRAINING (program details with bullets)
- ACTIVITIES (club activities and athletics)
- SKILLS (simple list)
- LANGUAGES

## Output URLs

- Index page: `https://mreider.com/resume/`
- Matt's resume: `https://mreider.com/resume/matt/`
- Max's resume: `https://mreider.com/resume/max/`
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
