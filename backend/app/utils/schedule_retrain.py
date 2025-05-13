import time
import schedule
import logging
from app.utils.retrain_model import retrain_model  # Import the retrain function

# Set up logging to track the retraining process
logging.basicConfig(level=logging.INFO)

def job():
    logging.info("Retraining model started...")
    retrain_model()  # Call the retrain function
    logging.info("Retraining model completed.")

# Schedule the retraining to run every week
schedule.every().week.do(job)

# Run the scheduler
while True:
    schedule.run_pending()  # Check if it's time to run the job
    time.sleep(60)  # Sleep for 1 minute before checking again
