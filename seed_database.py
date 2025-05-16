import json
from datetime import datetime
from database import engine, SessionLocal, Base
from models import Student

def load_student_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Read JSON file
    with open('mock_student_data.json', 'r') as file:
        students_data = json.load(file)
    
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Student).delete()
        
        # Process and insert each student
        for student_data in students_data:
            # Convert registration_date from string to date object
            if student_data['registration_date']:
                registration_date = datetime.strptime(
                    student_data['registration_date'], 
                    '%m/%d/%Y'
                ).date()
            else:
                registration_date = None
            
            # Create student object
            student = Student(
                id=student_data['id'],
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                email=student_data['email'],
                gender=student_data['gender'],
                student_id=student_data['student_id'],
                study_programme=student_data['study_programme'],
                secondary_school=student_data['secondary_school'],
                registration_date=registration_date,
                academic_year=student_data['academic_year']
            )
            db.add(student)
        
        # Commit all changes
        db.commit()
        print("Successfully loaded student data into database!")
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_student_data() 