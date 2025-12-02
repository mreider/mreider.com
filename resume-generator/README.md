# Resume Generator

Generates HTML and PDF resume from text file and publishes to Hugo site.

## Files

- `matt_resume.txt` - Resume content (edit this)
- `generate.py` - Generator script
- `matt-profile-image.jpeg` - Profile photo
- `acrobat-logo.png` - PDF download icon
- `linkedin-logo.png` - LinkedIn icon

## Usage

1. Edit `matt_resume.txt` with resume updates
2. Run generator:
   ```bash
   cd resume-generator
   python3 generate.py
   ```
3. Rebuild Hugo site:
   ```bash
   cd ..
   hugo
   ```

## What it does

1. Parses `matt_resume.txt`
2. Generates styled HTML with:
   - Profile photo
   - PDF download button
   - LinkedIn profile button
3. Creates PDF using Chrome headless
4. Copies all files to `../static/resume/`:
   - `index.html`
   - `resume.pdf`
   - `matt-profile-image.jpeg`
   - `acrobat-logo.png`
   - `linkedin-logo.png`

## Resume format

See `matt_resume.txt` for structure. Key sections:
- NAME, PHONE, EMAIL, LOCATION
- SUMMARY
- JOB TITLE, COMPANY, DATES (with optional bullets)
- CORE COMPETENCIES (automatically organized into grid)
- EDUCATION (degree, school, date)
- LICENSES & CERTIFICATIONS (name, org, date)
- PERSONAL

## Output

Resume accessible at: `https://mreider.com/resume/`
Linked from About page.
