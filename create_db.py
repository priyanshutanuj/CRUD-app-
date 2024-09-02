from app import app, db  # Import app and db from your main application file

# Initialize the Flask app context
with app.app_context():
    db.create_all()  # Create database tables
    print("Database and tables created.")
