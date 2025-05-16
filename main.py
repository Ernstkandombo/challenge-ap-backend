from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine
from models import Student, Base
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Registration API")

# CORS configuration for frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/total-registrations")
def get_total_registrations(db: Session = Depends(get_db)):
    """Get the total number of student registrations"""
    total = db.query(Student).count()
    return {"total_registrations": total}

@app.get("/api/registrations-by-programme")
def get_registrations_by_programme(db: Session = Depends(get_db)):
    """Get the number of registrations per study programme"""
    registrations = db.query(
        Student.study_programme,
        func.count(Student.id).label("total")
    ).group_by(Student.study_programme).all()
    
    return {
        "registrations": [
            {
                "programme": reg[0],
                "total": reg[1]
            } for reg in registrations
        ]
    }

@app.get("/api/registrations-by-school")
def get_registrations_by_school(db: Session = Depends(get_db)):
    """Get the number of registrations per secondary school"""
    registrations = db.query(
        Student.secondary_school,
        func.count(Student.id).label("total")
    ).group_by(Student.secondary_school).all()
    
    return {
        "registrations": [
            {
                "school": reg[0],
                "total": reg[1]
            } for reg in registrations
        ]
    }

@app.get("/api/registrations-by-year")
def get_registrations_by_year(db: Session = Depends(get_db)):
    """Get the number of registrations per academic year"""
    registrations = db.query(
        Student.academic_year,
        func.count(Student.id).label("total")
    ).filter(Student.academic_year != None).group_by(Student.academic_year).all()
    
    return {
        "registrations": [
            {
                "year": reg[0],
                "total": reg[1]
            } for reg in registrations
        ]
    }

@app.get("/api/top-schools")
def get_top_schools(limit: int = 10, db: Session = Depends(get_db)):
    """Get the top secondary schools by number of registrations"""
    top_schools = db.query(
        Student.secondary_school,
        func.count(Student.id).label("total")
    ).group_by(Student.secondary_school)\
     .order_by(func.count(Student.id).desc())\
     .limit(limit)\
     .all()
    
    return {
        "top_schools": [
            {
                "school": school[0],
                "total": school[1]
            } for school in top_schools
        ]
    }

# Additional helpful endpoints

@app.get("/api/student/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db)):
    """Get details of a specific student by their student ID"""
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/api/programmes")
def get_programmes(db: Session = Depends(get_db)):
    """Get list of all study programmes"""
    programmes = db.query(Student.study_programme)\
        .distinct()\
        .order_by(Student.study_programme)\
        .all()
    return {"programmes": [prog[0] for prog in programmes]}

@app.get("/api/schools")
def get_schools(db: Session = Depends(get_db)):
    """Get list of all secondary schools"""
    schools = db.query(Student.secondary_school)\
        .distinct()\
        .order_by(Student.secondary_school)\
        .all()
    return {"schools": [school[0] for school in schools]}





