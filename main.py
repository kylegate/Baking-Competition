from database.ddl_create_tables import create_person_table, create_entry_table
from database.dml_insert_persons import insert_person_data
from database.dml_insert_entries import insert_entry_data
import subprocess
import sys

def install_requirements():
    """Installs packages from requirements.txt if not already installed."""
    print("Installing required Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All required packages are installed.")
    except Exception as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)


if __name__ == "__main__":
    install_requirements()

    print("Initializing Databases...")
    create_person_table()
    create_entry_table()
    insert_person_data()
    insert_entry_data()
    print("Databases Initialized Successfully!")

    # Start app.py
    print("Starting the main app server...")
    subprocess.Popen(["python", "app.py"])

    # Start entry deletion server
    print("Starting the entry deletion server...")
    subprocess.Popen(["python", "entry_deletion_server.py"])

    # Start vote submission server
    print("Starting the vote submission server...")
    subprocess.Popen(["python", "vote_submission_server.py"])

    print("All servers are up and running!")
