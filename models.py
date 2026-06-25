import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=True)
    email = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=True)
    summary = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    skills = relationship("Skill", back_populates="candidate", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="candidate", cascade="all, delete-orphan")
    experience = relationship("WorkExperience", back_populates="candidate", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name or 'Unknown Candidate',
            'email': self.email or 'N/A',
            'phone': self.phone or 'N/A',
            'summary': self.summary or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'skills': [skill.name for skill in self.skills],
            'education': [
                {
                    'degree': edu.degree or '',
                    'institution': edu.institution or '',
                    'field_of_study': edu.field_of_study or '',
                    'start_year': edu.start_year or '',
                    'end_year': edu.end_year or ''
                } for edu in self.education
            ],
            'experience': [
                {
                    'job_title': exp.job_title or '',
                    'company': exp.company or '',
                    'start_date': exp.start_date or '',
                    'end_date': exp.end_date or '',
                    'description': exp.description or ''
                } for exp in self.experience
            ]
        }

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    name = Column(String(100), nullable=False)
    
    candidate = relationship("Candidate", back_populates="skills")

class Education(Base):
    __tablename__ = 'education'
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    degree = Column(String(150), nullable=True)
    institution = Column(String(200), nullable=True)
    field_of_study = Column(String(200), nullable=True)
    start_year = Column(String(10), nullable=True)
    end_year = Column(String(10), nullable=True)
    
    candidate = relationship("Candidate", back_populates="education")

class WorkExperience(Base):
    __tablename__ = 'work_experience'
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_title = Column(String(150), nullable=True)
    company = Column(String(150), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    
    candidate = relationship("Candidate", back_populates="experience")

# Setup helper for Session
def get_session(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
