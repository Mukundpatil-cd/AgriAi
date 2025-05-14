import sys
from app.database import engine, Base
from sqlalchemy import inspect

# Get database schema
try:
    # Get connection and introspect tables
    conn = engine.connect()
    insp = inspect(engine)
    
    # Check disease_logs table columns
    print("Checking disease_logs table structure:")
    if "disease_logs" in insp.get_table_names():
        columns = insp.get_columns("disease_logs")
        print("Columns in disease_logs table:")
        for column in columns:
            print(f"  - {column['name']} ({column['type']})")
    else:
        print("disease_logs table does not exist!")
        
    conn.close()
except Exception as e:
    print(f"Error accessing database: {e}")
    sys.exit(1)
