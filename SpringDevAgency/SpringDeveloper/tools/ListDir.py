from pydantic import Field
from agency_swarm.tools import BaseTool
import os

class ListDir(BaseTool):
    """
    This tool returns the tree structure of the directory, specifically tailored for Spring Boot projects.
    """
    dir_path: str = Field(
        ..., description="Path of the directory to read.",
        examples=["./", "./src", "../my-project"]
    )

    def run(self):
        if not os.path.exists(self.dir_path):
            return f"The directory {self.dir_path} does not exist."

        tree = []

        def list_directory_tree(path, indent=''):
            """Recursively list the contents of a directory in a tree-like format."""
            if not os.path.isdir(path):
                raise ValueError(f"The path {path} is not a valid directory")

            items = os.listdir(path)
            # Exclude common hidden files and directories specific to Java/Spring Boot projects
            exclude = ['.git', '.idea', '__pycache__', 'node_modules', '.DS_Store', '.vscode', 'target', 'build', '.mvn', '.gradle']
            items = [item for item in items if item not in exclude]

            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                if i < len(items) - 1:
                    tree.append(indent + '├── ' + item)
                    if os.path.isdir(item_path):
                        list_directory_tree(item_path, indent + '│   ')
                else:
                    tree.append(indent + '└── ' + item)
                    if os.path.isdir(item_path):
                        list_directory_tree(item_path, indent + '    ')

        list_directory_tree(self.dir_path)

        return "\n".join(tree)
