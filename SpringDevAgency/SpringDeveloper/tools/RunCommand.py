import os
import subprocess
from typing import Literal
from pydantic import BaseModel, Field
import xml.etree.ElementTree as ET

class SpringBootRunCommand(BaseModel):
    """Enables you to execute certain Spring Boot development commands using Maven."""
    command: Literal['init', 'add-dependency', 'run'] = Field(
        ...,
        description='The terminal command to execute. Initialize a new project with `init`, add a new dependency with `add-dependency`, or start the application with `run`.'
    )
    options: str = Field(
        default='',
        description='Additional options to pass to the command. For `init`, specify project details. For `add-dependency`, specify groupId:artifactId:version. For `run`, options are not necessary.',
        examples=['web,data-jpa,h2,lombok', 'org.springframework.boot:spring-boot-starter-security:[2.3.0.RELEASE,)', 'my-spring-app']
    )

    def find_pom_xml(self, start_path):
        """Search for pom.xml in the current and subdirectories."""
        for root, dirs, files in os.walk(start_path):
            if 'pom.xml' in files:
                return True, os.path.join(root, 'pom.xml')
        return False, None
    
    def run(self):
        try:
            options_list = [option.strip() for option in self.options.split(',') if option.strip()]
            
            if self.command == 'init':
                if 'my-spring-app' not in options_list:
                    return 'Please provide a name for the app when using the `init` command.'
                
                cmd = ['curl', 'https://start.spring.io/starter.zip', '-d', 'dependencies=' + self.options, '-d', 'name=my-spring-app', '-d', 'type=maven-project', '-o', 'my-spring-app.zip']
                subprocess.run(cmd, check=True)
                subprocess.run(['unzip', 'my-spring-app.zip', '-d', 'my-spring-app'], check=True)
                return 'Spring Boot project initialized successfully.'
            
            if self.command == 'add-dependency':
                pom_exists, pom_path = self.find_pom_xml(os.getcwd())
                if not pom_exists:
                    return 'pom.xml does not exist in the current or subdirectory. Are you in the right directory?'

                options_list = [option.strip() for option in self.options.split(',') if option.strip()]
                if not options_list:
                    return 'Please specify the dependency to add using groupId:artifactId:version format.'

                dependency = options_list[0]
                add_dependency_to_pom(pom_path, dependency)

                subprocess.run(['mvn', 'install'], check=True, cwd=os.path.dirname(pom_path))
                return f'Dependency {dependency} added to pom.xml and installed successfully.'

            elif self.command == 'run':
                pom_exists, pom_path = self.find_pom_xml(os.getcwd())
                if not pom_exists:
                    return 'pom.xml does not exist in the current or subdirectory. Are you in the right directory?'

                subprocess.run(['mvn', 'spring-boot:run'], check=True, cwd=os.path.dirname(pom_path))
                return 'Spring Boot application started successfully.'
            
            
            return 'Invalid command. Please use either `init`, `add-dependency`, or `run`.'
        
        except subprocess.CalledProcessError as e:
            return f'Error executing command: {e}'
        
def add_dependency_to_pom(pom_path, dependency):
    groupId, artifactId, version = dependency.split(':')
    
    tree = ET.parse(pom_path)
    root = tree.getroot()

    ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}

    dependencies_tag = root.find('maven:dependencies', ns)

    if dependencies_tag is None:
        dependencies_tag = ET.SubElement(root, 'dependencies')

    dependency_tag = ET.SubElement(dependencies_tag, 'dependency')
    groupId_tag = ET.SubElement(dependency_tag, 'groupId')
    groupId_tag.text = groupId
    artifactId_tag = ET.SubElement(dependency_tag, 'artifactId')
    artifactId_tag.text = artifactId
    version_tag = ET.SubElement(dependency_tag, 'version')
    version_tag.text = version
    tree.write(pom_path, encoding="utf-8", xml_declaration=True)