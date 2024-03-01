from agency_swarm.agents import Agent

class SpringDeveloper(Agent):
    def __init__(self):
        super().__init__(
            name="SpringDeveloper",
            description="Implements RESTful APIs according to the specifications provided by the Software Architect.",
            instructions="./instructions_spring_developer.md",
            tools_folder="./tools"
        )
