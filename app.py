import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import get_session, Candidate, Skill, Education, WorkExperience
from parser import parse_resume

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key_192837")

# Config database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///resume_parser.db")
db_session = get_session(DATABASE_URL)

# Config uploads
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    candidates = db_session.query(Candidate).order_by(Candidate.created_at.desc()).all()
    # Serialize for frontend if needed, or pass directly
    return render_template('index.html', candidates=candidates)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'No file part'}), 400
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'No selected file'}), 400
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                # Parse the resume
                parsed_data = parse_resume(file_path)
                
                # Save to database
                candidate = Candidate(
                    name=parsed_data['name'],
                    email=parsed_data['email'],
                    phone=parsed_data['phone'],
                    summary=parsed_data['summary'],
                    raw_text=parsed_data['raw_text']
                )
                db_session.add(candidate)
                db_session.flush()  # Get candidate ID
                
                # Add skills
                for skill_name in parsed_data['skills']:
                    skill = Skill(candidate_id=candidate.id, name=skill_name)
                    db_session.add(skill)
                    
                # Add education
                for edu_data in parsed_data['education']:
                    edu = Education(
                        candidate_id=candidate.id,
                        degree=edu_data.get('degree'),
                        institution=edu_data.get('institution'),
                        field_of_study=edu_data.get('field_of_study'),
                        start_year=edu_data.get('start_year'),
                        end_year=edu_data.get('end_year')
                    )
                    db_session.add(edu)
                    
                # Add experience
                for exp_data in parsed_data['experience']:
                    exp = WorkExperience(
                        candidate_id=candidate.id,
                        job_title=exp_data.get('job_title'),
                        company=exp_data.get('company'),
                        start_date=exp_data.get('start_date'),
                        end_date=exp_data.get('end_date'),
                        description=exp_data.get('description')
                    )
                    db_session.add(exp)
                    
                db_session.commit()
                
                # Clean up uploaded file
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': True, 
                        'message': 'Resume parsed and saved successfully!',
                        'candidate_id': candidate.id
                    })
                
                flash('Resume uploaded and parsed successfully!')
                return redirect(url_for('index'))
                
            except Exception as e:
                db_session.rollback()
                if os.path.exists(file_path):
                    os.remove(file_path)
                print(f"Error processing upload: {e}")
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': False, 'message': f'Error parsing resume: {str(e)}'}), 500
                    
                flash(f'Error parsing resume: {str(e)}')
                return redirect(request.url)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Invalid file type. Only PDF and DOCX are allowed.'}), 400
            flash('Allowed file types are pdf, docx')
            return redirect(request.url)
            
    return render_template('upload.html')

@app.route('/resume/<int:candidate_id>')
def view_resume(candidate_id):
    candidate = db_session.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        flash('Candidate not found.')
        return redirect(url_for('index'))
    return render_template('detail.html', candidate=candidate)

@app.route('/api/candidates', methods=['GET'])
def get_candidates_api():
    candidates = db_session.query(Candidate).order_by(Candidate.created_at.desc()).all()
    return jsonify([c.to_dict() for c in candidates])

@app.route('/api/export/<int:candidate_id>', methods=['GET'])
def export_candidate(candidate_id):
    candidate = db_session.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    return jsonify(candidate.to_dict())

@app.route('/api/delete/<int:candidate_id>', methods=['DELETE', 'POST'])
def delete_candidate(candidate_id):
    # Support both DELETE method (for AJAX) and POST (for fallback forms)
    candidate = db_session.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.method == 'DELETE':
            return jsonify({'success': False, 'message': 'Candidate not found'}), 404
        flash('Candidate not found.')
        return redirect(url_for('index'))
        
    try:
        db_session.delete(candidate)
        db_session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.method == 'DELETE':
            return jsonify({'success': True, 'message': 'Candidate deleted successfully'})
            
        flash('Candidate deleted successfully.')
        return redirect(url_for('index'))
    except Exception as e:
        db_session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.method == 'DELETE':
            return jsonify({'success': False, 'message': f'Error deleting candidate: {str(e)}'}), 500
        flash(f'Error deleting candidate: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Try importing en_core_web_sm to verify NLP engine download
    try:
        import spacy
        spacy.load("en_core_web_sm")
    except OSError:
        print("Initial download of spaCy model 'en_core_web_sm'...")
        os.system("python -m spacy download en_core_web_sm")
        
    app.run(host='0.0.0.0', port=5000, debug=True)
