# # app.py
# import os
# import uuid
# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import re
# import base64
# from io import BytesIO
# from flask import Response

# # Import all your analyzer classes
# from ats_analyzer.skill_matcher import SkillMatcher
# from ats_analyzer.experience_matcher import ExperienceMatcher
# from ats_analyzer.project_matcher import ProjectMatcher
# from ats_analyzer.quantifiable_checker import QuantifiableChecker
# from ats_analyzer.education_checker import EducationChecker
# from ats_analyzer.keyword_checker import KeywordChecker
# from ats_analyzer.formatting_checker import FormattingChecker
# from ats_analyzer.feedback_generator import FeedbackGenerator
# from ats_analyzer.pdf_processor import PDFProcessor
# from ats_analyzer.report_generator import ReportGenerator

# app = Flask(__name__)
# app.secret_key = 'your-secret-key-here'  # Change this in production
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.jinja_env.cache = {}

# # Configure a temporary upload folder
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Allowed extensions for file uploads
# ALLOWED_EXTENSIONS = {'pdf'}

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # ROUTE 1: Display the main upload page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # ROUTE 2: Handle the file upload and analysis
# @app.route('/analyze', methods=['POST'])
# def analyze():
#     if 'resume' not in request.files or 'job_description' not in request.files:
#         flash('Please upload both resume and job description files.')
#         return redirect(url_for('index'))

#     resume_file = request.files['resume']
#     jd_file = request.files['job_description']

#     if resume_file.filename == '' or jd_file.filename == '':
#         flash('Please select both resume and job description files.')
#         return redirect(url_for('index'))

#     if not (allowed_file(resume_file.filename) and allowed_file(jd_file.filename)):
#         flash('Only PDF files are allowed.')
#         return redirect(url_for('index'))

#     if resume_file and jd_file:
#         # Create unique filenames and save files
#         resume_filename = str(uuid.uuid4()) + ".pdf"
#         jd_filename = str(uuid.uuid4()) + ".pdf"
#         resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
#         jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
#         resume_file.save(resume_path)
#         jd_file.save(jd_path)
        
#         try:
#             # --- CORE ANALYSIS LOGIC ---
#             resume_processor = PDFProcessor(resume_path)
#             job_processor = PDFProcessor(jd_path)
#             resume_text = resume_processor.extract_text()
#             job_text = job_processor.extract_text()

#             print("===== RESUME TEXT PREVIEW =====")
#             print(resume_text[:2000])  # first 2000 chars
#             print("===============================")

            
#             if not resume_text.strip() or not job_text.strip():
#                 flash('Could not extract text from the uploaded PDFs. Please ensure they contain selectable text.')
#                 os.remove(resume_path)
#                 os.remove(jd_path)
#                 return redirect(url_for('index'))
                
#             resume_text_normalized = resume_processor.normalize_text()
#             job_text_normalized = job_processor.normalize_text()
            
#             skill_score, skill_details = SkillMatcher.calculate_score(resume_text_normalized, job_text_normalized)
#             exp_score, exp_details = ExperienceMatcher.calculate_experience_score(resume_text, job_text)
#             project_score, project_details = ProjectMatcher.calculate_project_skill_score(resume_text, skill_details["matched_skills"])
#             achievement_score, achievement_details = QuantifiableChecker.calculate_achievement_score(resume_text)
#             education_score, education_details = EducationChecker.calculate_education_score(resume_text, job_text)
#             keyword_score, keyword_details = KeywordChecker.calculate_keyword_score(resume_text, job_text)
#             formatting_score, formatting_details = FormattingChecker.calculate_formatting_score(resume_text)
            
#             os.remove(resume_path)
#             os.remove(jd_path)
            
#             weights = { 
#                 "skills": 0.40, 
#                 "experience": 0.20, 
#                 "projects": 0.10, 
#                 "achievements": 0.10, 
#                 "education": 0.05, 
#                 "keywords": 0.05, 
#                 "formatting": 0.10 
#             }
            
#             scores = {
#                 "Skill Matching": skill_score, 
#                 "Experience Relevance": exp_score,
#                 "Skill Usage in Projects": project_score, 
#                 "Quantifiable Achievements": achievement_score,
#                 "Education Alignment": education_score, 
#                 "Keyword Optimization": keyword_score,
#                 "Formatting Compliance": formatting_score
#             }
            
#             final_weighted_score = sum(scores[cat] * weights[key] for cat, key in zip(scores.keys(), weights.keys()))
            
#             all_details = {
#                 'skills': skill_details, 
#                 'experience': exp_details, 
#                 'projects': project_details,
#                 'achievements': achievement_details, 
#                 'education': education_details, 
#                 'keywords': keyword_details,
#                 'formatting': formatting_details
#             }
            
#             feedback_report = FeedbackGenerator.generate_feedback(all_details)

#             # Render the NEW results.html template with the analysis data
#             return render_template('results.html', 
#                                    final_score=final_weighted_score, 
#                                    scores=scores, 
#                                    feedback=feedback_report)
                                   
#         except Exception as e:
#             # Clean up files in case of error
#             if os.path.exists(resume_path):
#                 os.remove(resume_path)
#             if os.path.exists(jd_path):
#                 os.remove(jd_path)
                
#             app.logger.error(f'Error during analysis: {str(e)}')
#             flash('An error occurred during analysis. Please try again with different files.')
#             return redirect(url_for('index'))

#     return redirect(url_for('index'))


# if __name__ == '__main__':
#     app.run(debug=True)






import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
import re
import tempfile

# Make dotenv optional for development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip loading .env file
    pass

# Import all your analyzer classes
from ats_analyzer.skill_matcher import SkillMatcher
from ats_analyzer.experience_matcher import ExperienceMatcher
from ats_analyzer.project_matcher import ProjectMatcher
from ats_analyzer.quantifiable_checker import QuantifiableChecker
from ats_analyzer.education_checker import EducationChecker
from ats_analyzer.keyword_checker import KeywordChecker
from ats_analyzer.formatting_checker import FormattingChecker
from ats_analyzer.feedback_generator import FeedbackGenerator
from ats_analyzer.pdf_processor import PDFProcessor

app = Flask(__name__)

# Production-ready configuration
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
app.config['TEMPLATES_AUTO_RELOAD'] = False if os.environ.get('RAILWAY_ENVIRONMENT') else True
app.jinja_env.cache = None if os.environ.get('RAILWAY_ENVIRONMENT') else {}

# Use system temp directory for Railway, local uploads folder for development
if os.environ.get('RAILWAY_ENVIRONMENT'):
    UPLOAD_FOLDER = tempfile.gettempdir()
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit
else:
    UPLOAD_FOLDER = 'uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ROUTE 1: Display the main upload page
@app.route('/')
def index():
    return render_template('index.html')

# ROUTE 2: Handle the file upload and analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files or 'job_description' not in request.files:
        flash('Please upload both resume and job description files.')
        return redirect(url_for('index'))

    resume_file = request.files['resume']
    jd_file = request.files['job_description']

    if resume_file.filename == '' or jd_file.filename == '':
        flash('Please select both resume and job description files.')
        return redirect(url_for('index'))

    if not (allowed_file(resume_file.filename) and allowed_file(jd_file.filename)):
        flash('Only PDF files are allowed.')
        return redirect(url_for('index'))

    if resume_file and jd_file:
        # Create unique filenames and save files
        resume_filename = str(uuid.uuid4()) + ".pdf"
        jd_filename = str(uuid.uuid4()) + ".pdf"
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        resume_file.save(resume_path)
        jd_file.save(jd_path)
        
        try:
            # --- CORE ANALYSIS LOGIC ---
            resume_processor = PDFProcessor(resume_path)
            job_processor = PDFProcessor(jd_path)
            resume_text = resume_processor.extract_text()
            job_text = job_processor.extract_text()

            # Only print debug info in development
            if not os.environ.get('RAILWAY_ENVIRONMENT'):
                print("===== RESUME TEXT PREVIEW =====")
                print(resume_text[:2000])  # first 2000 chars
                print("===============================")

            
            if not resume_text.strip() or not job_text.strip():
                flash('Could not extract text from the uploaded PDFs. Please ensure they contain selectable text.')
                # Clean up files
                if os.path.exists(resume_path):
                    os.remove(resume_path)
                if os.path.exists(jd_path):
                    os.remove(jd_path)
                return redirect(url_for('index'))
                
            resume_text_normalized = resume_processor.normalize_text(resume_text)
            job_text_normalized = job_processor.normalize_text(job_text)
            
            skill_score, skill_details = SkillMatcher.calculate_score(resume_text_normalized, job_text_normalized)
            exp_score, exp_details = ExperienceMatcher.calculate_experience_score(resume_text, job_text)
            project_score, project_details = ProjectMatcher.calculate_project_skill_score(resume_text, job_text)
            achievement_score, achievement_details = QuantifiableChecker.calculate_achievement_score(resume_text)
            education_score, education_details = EducationChecker.calculate_education_score(resume_text, job_text)
            keyword_score, keyword_details = KeywordChecker.calculate_keyword_score(resume_text, job_text)
            formatting_score, formatting_details = FormattingChecker.calculate_formatting_score(resume_text)
            
            # Clean up uploaded files
            if os.path.exists(resume_path):
                os.remove(resume_path)
            if os.path.exists(jd_path):
                os.remove(jd_path)
            
            weights = { 
                "skills": 0.40, 
                "experience": 0.20, 
                "projects": 0.10, 
                "achievements": 0.10, 
                "education": 0.05, 
                "keywords": 0.05, 
                "formatting": 0.10 
            }
            
            scores = {
                "Skill Matching": skill_score, 
                "Experience Relevance": exp_score,
                "Skill Usage in Projects": project_score, 
                "Quantifiable Achievements": achievement_score,
                "Education Alignment": education_score, 
                "Keyword Optimization": keyword_score,
                "Formatting Compliance": formatting_score
            }
            
            final_weighted_score = sum(scores[cat] * weights[key] for cat, key in zip(scores.keys(), weights.keys()))
            
            all_details = {
                'skills': skill_details, 
                'experience': exp_details, 
                'projects': project_details,
                'achievements': achievement_details, 
                'education': education_details, 
                'keywords': keyword_details,
                'formatting': formatting_details
            }
            
            # Generate feedback with semantic enhancements
            feedback_report = FeedbackGenerator.generate_feedback(all_details, job_text_normalized)

            # Render the results template
            return render_template('results.html', 
                                   final_score=final_weighted_score, 
                                   scores=scores, 
                                   feedback=feedback_report)
                                   
        except Exception as e:
            # Clean up files in case of error
            if os.path.exists(resume_path):
                os.remove(resume_path)
            if os.path.exists(jd_path):
                os.remove(jd_path)
                
            # Log error appropriately
            if os.environ.get('RAILWAY_ENVIRONMENT'):
                app.logger.error(f'Error during analysis: {str(e)}')
            else:
                print(f'Error during analysis: {str(e)}')
                
            flash('An error occurred during analysis. Please try again with different files.')
            return redirect(url_for('index'))

    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('RAILWAY_ENVIRONMENT') is None
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=debug_mode,
        threaded=True
    )