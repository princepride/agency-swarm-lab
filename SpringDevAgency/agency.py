from agency_swarm import Agency, set_openai_key
from CEO import CEO
from SoftwareArchitect import SoftwareArchitect
from SpringDeveloper import SpringDeveloper
from TestEngineer import TestEngineer
import os

# load env from .env
from dotenv import load_dotenv
load_dotenv()

set_openai_key(os.environ["OPENAI_API_KEY"])

ceo = CEO()
softwareArchitect = SoftwareArchitect()
springDeveloper = SpringDeveloper()
testEngineer = TestEngineer()

agency = Agency([ceo, softwareArchitect, springDeveloper,
                 [ceo, softwareArchitect],
                 [softwareArchitect, springDeveloper],
                 [springDeveloper, testEngineer]],
                shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    # agency.demo_gradio(height=400)
    agency.run_demo()