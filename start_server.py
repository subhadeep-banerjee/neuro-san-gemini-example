import os
from dotenv import load_dotenv
from neuro_san.service.main_loop.server_main_loop import ServerMainLoop

print("1. Loading Environment Variables from .env...")
# This automatically reads the .env file in the same folder
load_dotenv()

if __name__ == "__main__":
    # Fetching variables just to print a clean startup message
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION")
    
    print(f"2. Environment locked. Targeting GCP Project: {project_id} ({region})")
    print("3. Igniting Neuro SAN Server...")
    
    # Trigger the framework
    ServerMainLoop().main_loop()