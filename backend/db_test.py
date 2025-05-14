import sys
from app.database import SessionLocal, DiseaseLog, engine, Base

print('Database URL:', engine.url)
print('SQLAlchemy version:', engine.dialect.driver)

# Try creating tables
try:
    print('Creating tables...')
    Base.metadata.create_all(bind=engine)
    print('Tables created successfully')
except Exception as e:
    print(f'Error creating tables: {e}', file=sys.stderr)
    sys.exit(1)

# Try to connect to the database
db = SessionLocal()
print('Testing database connection...')

try:
    print('Querying DiseaseLog table...')
    result = db.query(DiseaseLog).first()
    if result:
        print(f'Connection successful. Found record: {result.id}, {result.result}')
    else:
        print('Connection successful. No records found.')
    
    # Try adding a test record
    print('Adding test record...')
    test_log = DiseaseLog(
        user_id=999,
        image_name='test_image.jpg',
        result='test_result'
    )
    db.add(test_log)
    db.commit()
    print('Test record added successfully with ID:', test_log.id)
    
    # Clean up
    db.delete(test_log)
    db.commit()
    print('Test record deleted')

except Exception as e:
    print(f'Database error: {e}', file=sys.stderr)
finally:
    db.close()
