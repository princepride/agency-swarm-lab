from agency_swarm.agents import Agent

class SoftwareArchitect(Agent):
    def __init__(self):
        super().__init__(
            name="SoftwareArchitect",
            description="Responsible for designing the system architecture and defining API specifications based on client requirements.",
            instructions="./instructions_software_architect.md",
            files_folder="./files",
            tools_folder="./tools"
        )
