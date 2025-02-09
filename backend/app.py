from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
import os
import tempfile
import subprocess
import json
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("Gemini API key is missing. Ensure it is set in the environment variables.")

OUTPUT_DIR = 'output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("Gemini API key loaded successfully.")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def process_with_gemini(data):
    """
    Process the resume data using Gemini API to clean and format it.
    """
    prompt = f"""
    Clean and format the following resume data professionally. 
    Return a JSON object of the same structure and 
    ensure all details are in their original structure and use an 'action - change - effect' format.
    Keep all sections and formatting intact.
    Ignore if any field is empty and do not raise any other messages.

    Input data:
    {json.dumps(data, indent=2)}
    """

    print("Sending data to Gemini:")
    print(json.dumps(data, indent=2))

    response = model.generate_content(prompt)

    if not response.text:
        print("Empty response from Gemini.")
        return data  # Return original data if response is empty

print("Gemini response:")
print(response.text)

try:
    cleaned_data = json.loads(response.text.strip())
except json.JSONDecodeError:
    print("Gemini returned non-JSON response. Attempting to extract structured data.")
    cleaned_data = {"formatted_text": response.text.strip()}
return cleaned_data


def compile_latex(tex_content) :
    try:
        tex_path = os.path.join(OUTPUT_DIR, 'resume.tex')
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        
        process = subprocess.run(
            [
                'pdflatex',
                '-interaction=nonstopmode',
                '-halt-on-error',
                f'-output-directory={OUTPUT_DIR}',
                tex_path
            ],
            capture_output=True,
            text=True,
            check=False
        )
        
        pdf_path = os.path.join(OUTPUT_DIR, 'resume.pdf')
        print(pdf_path)
        
        if os.path.exists(pdf_path):
            return True, pdf_path
        
        log_path = os.path.join(OUTPUT_DIR, 'resume_generation.log')
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                log_content = f.read()
        else:
            log_content = "no log file generated"
        
        return False, f"LaTeX error : {process.stderr}\n\nLog : {log_content}"
    except Exception as e:
        return False, str(e) 

# Modified compile_latex function
# def compile_latex(tex_content):
#     try:
#         # Create temporary directory
#         with tempfile.TemporaryDirectory() as tmpdir:
#             tex_path = os.path.join(tmpdir, 'resume.tex')
#             pdf_path = os.path.join(tmpdir, 'resume.pdf')
            
#             # Write LaTeX content
#             with open(tex_path, 'w', encoding='utf-8') as f:
#                 f.write(tex_content)

#             # Compile LaTeX
#             result = subprocess.run(
#                 ['pdflatex', '-interaction=nonstopmode', '-output-directory', tmpdir, tex_path],
#                 capture_output=True,
#                 text=True,
#                 timeout=30
#             )

#             if result.returncode != 0:
#                 return False, f"LaTeX Error:\n{result.stderr}"

#             if not os.path.exists(pdf_path):
#                 return False, "PDF generation failed - no output file"

#             # Read PDF content
#             with open(pdf_path, 'rb') as f:
#                 pdf_content = f.read()

#             return True, pdf_content

#     except Exception as e:
#         return False, str(e)

# Modified generate_resume endpoint
@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    data = request.json
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        # Process data with Gemini
        cleaned_data = process_with_gemini(data)
        
        # Create LaTeX content
        latex_content = create_latex_content(cleaned_data)
        
        # Compile LaTeX to PDF
        success, result = compile_latex(latex_content)
        
        if not success:
            return jsonify({
                'error': 'LaTeX compilation failed',
                'details': result,
                'latex_source': latex_content
            }), 500

        # Encode PDF to base64 for response
        pdf_b64 = base64.b64encode(result).decode('utf-8')
        
        return jsonify({
            'pdf': pdf_b64,
            'latex': latex_content
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# def create_latex_content(data):
#     """
#     Replace placeholders in LaTeX template with resume data.
#     """
#     with open('templates/resume_template.tex', 'r') as file:
#         template = file.read()

#     replacements = {
#         'NAME': data.get('name', ''),
#         'LOCATION': data.get('location', ''),
#         'PHONE': data.get('phone', ''),
#         'EMAIL': data.get('email', ''),
#         'LINKEDIN': data.get('linkedin', ''),
#         'GITHUB': data.get('github', '')
#     }

#     for placeholder, value in replacements.items():
#         template = template.replace(placeholder, value)

#     # Format experience section
#     experience = '\n'.join(f"""
#         \\resumeSubheading
#         {{{exp.get('company', '')}}}
#         {{{exp.get('date', '')}}}
#         {{{exp.get('title', '')}}}
#         {{{exp.get('location', '')}}}
#         \\resumeItemListStart
#         \\resumeItem{{{exp.get('description', '')}}}
#         \\resumeItemListEnd
#     """ for exp in data.get('experience', []))
    
#     template = template.replace('EXPERIENCE_PLACEHOLDER', experience)

#     # Format education section
#     education = '\n'.join(f"""
#         \\resumeSubheading
#         {{{edu.get('school', '')}}}
#         {{{edu.get('date', '')}}}
#         {{{edu.get('degree', '')}}}
#         {{{edu.get('location', '')}}}
#     """ for edu in data.get('education', []))

#     template = template.replace('EDUCATION_PLACEHOLDER', education)

#     # Format projects section
#     projects = '\n'.join(f"""
#         \\resumeProjectHeading
#         {{{{{proj.get('name', '')}}} \\emph{{{proj.get('technologies', '')}}}}}
#         \\resumeItemListStart
#         \\resumeItem{{{proj.get('description', '')}}}
#         \\resumeItemListEnd
#     """ for proj in data.get('projects', []))

#     template = template.replace('PROJECTS_PLACEHOLDER', projects)

#     # Format skills
#     skills = data.get('skills', '').replace(',', ' \\textbullet{} ')
#     template = template.replace('SKILLS_PLACEHOLDER', skills)

#     return template

# Modified create_latex_content function
def create_latex_content(data : dict):
    with open('templates/resume_template.tex', 'r') as file:
        template = file.read()

    # Basic replacements
    replacements = {
        'NAME': data.get('name', ''),
        'LOCATION': data.get('location', ''),
        'PHONE': data.get('phone', ''),
        'EMAIL': data.get('email', ''),
        'LINKEDIN': data.get('linkedin', '').split('/')[-1],  # Just handle username
        'GITHUB': data.get('github', '').split('/')[-1]
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, str(value))

    # Experience Section
    experience = []
    for exp in data.get('experience', []):
        experience.append(f"""
\\resumeSubheading
{{{exp.get('company', '')}}}
{{{exp.get('date', '')}}}
{{{exp.get('title', '')}}}
{{{exp.get('location', '')}}}
\\resumeItemListStart
{''.join([f'\\resumeItem{{{item}}}' for item in exp.get('description', [])])}
\\resumeItemListEnd
""")
    template = template.replace('EXPERIENCE_PLACEHOLDER', '\n'.join(experience))

    # Education Section
    education = []
    for edu in data.get('education', []):
        education.append(f"""
\\resumeSubheading
{{{edu.get('school', '')}}}
{{{edu.get('date', '')}}}
{{{edu.get('degree', '')}}}
{{{edu.get('location', '')}}}
""")
    template = template.replace('EDUCATION_PLACEHOLDER', '\n'.join(education))

    # Projects Section
    projects = []
    for proj in data.get('projects', []):
        projects.append(f"""
\\resumeProjectHeading
{{{proj.get('name', '')}}} $|$ {{{proj.get('technologies', '')}}}
\\resumeItemListStart
\\resumeItem{{{proj.get('description', '')}}}
\\resumeItemListEnd
""")
    template = template.replace('PROJECTS_PLACEHOLDER', '\n'.join(projects))

    # Skills Section
    # skills = ' $\\textbullet$ '.join(data.get('skills', []))
    # skills = 
    # template = template.replace('SKILLS_PLACEHOLDER', skills)
    skills = data.get('skills', '').replace(',', ' \\textbullet{} ')
    template = template.replace('SKILLS_PLACEHOLDER', skills)

    return template

# @app.route('/generate-resume', methods=['POST'])
# def generate_resume():
#     """
#     API endpoint to generate a resume PDF from JSON input.
#     """
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No input data provided'}), 400

#     # Process data with Gemini
#     cleaned_data = process_with_gemini(data)

#     # Create LaTeX content
#     latex_content = create_latex_content(cleaned_data)
    
#     success, result = compile_latex(latex_content)

#     if not success:
#         return jsonify({
#             'error' : 'LaTeX compilation failed',
#             'details' : result,
#             'latex_source' : latex_content
#         }), 500
    
#     return jsonify({
#         'latex_source' : latex_content,
#         'pdf_url' : '/download-pdf'
#     })

    # # Create temporary directory for LaTeX compilation
    # with tempfile.TemporaryDirectory() as tmpdir:
    #     tex_path = os.path.join(tmpdir, 'resume.tex')
    #     pdf_path = os.path.join(tmpdir, 'resume.pdf')

    #     with open(tex_path, 'w') as f:
    #         f.write(latex_content)

    #     # Compile LaTeX to PDF
    #     try:
    #         subprocess.run(['pdflatex', '--max-print-line=10000', '-synctex=1', '-file-line-error', '-recorder', '-interaction=nonstopmode', '-output-directory', tmpdir, tex_path], check=True)
    #         # subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', tmpdir, tex_path], check=True)  # Run twice for references
    #     except subprocess.CalledProcessError as e:
    #         print("LaTeX compilation failed:", e)
    #         return jsonify({'error': 'Failed to generate PDF. Check LaTeX logs.'}), 500

    #     # Save PDF in a global temporary location for download
    #     global last_generated_pdf
    #     last_generated_pdf = pdf_path

    #     return jsonify({
    #         'latex_source': latex_content,
    #         'pdf_url': '/download-pdf'
    #     })

@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    """
    API endpoint to download the generated resume PDF.
    """
    pdf_path = os.path.join(OUTPUT_DIR, 'resume.pdf')
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    return jsonify({'error': 'PDF not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
