from app.database import SessionLocal, DiseaseLog

# Try to connect to the database
db = SessionLocal()
print('Testing database connection and DiseaseLog schema...')

try:
    # Try creating a test record
    print('Adding test record to disease_logs...')
    test_log = DiseaseLog(
        image_name='test_image.jpg',
        predicted_class='test_disease'
    )
    db.add(test_log)
    db.commit()
    print('Test record added successfully with ID:', test_log.id)
    
    # Query the record back
    result = db.query(DiseaseLog).filter_by(id=test_log.id).first()
    print(f"Retrieved record: ID={result.id}, Image={result.image_name}, Prediction={result.predicted_class}")
    
    # Clean up
    db.delete(test_log)
    db.commit()
    print('Test record deleted')

except Exception as e:
    db.rollback()
    print(f'Database error: {e}')
finally:
    db.close()
