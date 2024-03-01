from agency_swarm.agents import Agent

class TestEngineer(Agent):
    def __init__(self):
        super().__init__(
            name="TestEngineer",
            description="Designs and executes a comprehensive testing strategy for the RESTful APIs, ensuring they meet quality standards.",
            instructions="./instructions_test_engineer.md",
            tools_folder="./tools"
        )
