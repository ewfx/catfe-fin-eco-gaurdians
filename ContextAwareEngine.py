import os
import torch
import subprocess
import pandas as pd
from docx import Document
from transformers import T5Tokenizer, T5ForConditionalGeneration
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
from huggingface_hub import login

# ✅ Authenticate with Hugging Face
HUGGINGFACE_TOKEN = ""
login(token=HUGGINGFACE_TOKEN)

class ContextAwareTestingSystem:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.app_url = None

    def scan_existing_step_definitions(self):
        """Scan all existing step definition files for already defined steps"""
        existing_steps = set()
        steps_folder = "features/steps"
        
        if not os.path.exists(steps_folder):
            return existing_steps

        for file in os.listdir(steps_folder):
            if file.endswith("_steps.py"):
                file_path = os.path.join(steps_folder, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.search(r'@(given|when|then)\(["\'](.+?)["\']\)', line)
                        if match:
                            existing_steps.add(match.group(2))  # Store existing step text
        
        return existing_steps

    def generate_feature_file(self, file_name, scenarios):
        """Generate a single feature file with multiple scenarios using Gherkin syntax"""
        feature_content = f"""Feature: {file_name}\n\n"""
        for scenario, steps in scenarios.items():
            feature_content += f"  Scenario: {scenario}\n"
            for i, step in enumerate(steps):
                if i == 0:
                    feature_content += f"    Given {step}\n"  # First step uses 'Given'
                elif i == len(steps) - 1:
                    feature_content += f"    Then {step}\n"  # Last step uses 'Then'
                else:
                    feature_content += f"    When {step}\n"  # Intermediate steps use 'When'
        return feature_content

    def extract_url_from_steps(self, steps):
        """Extract application URL from test input file if present"""
        for step in steps:
            match = re.search(r'open\s+(\S+)', step)
            if match:
                self.app_url = match.group(1)
                break

    def process_file(self, file_path):
        """Dynamically process different file types, including CSV files"""
        file_extension = os.path.splitext(file_path)[-1].lower()
        if file_extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                return file.readlines()
        elif file_extension == ".csv":
            df = pd.read_csv(file_path, header=None, engine='python', error_bad_lines=False)
            return df.iloc[:, 0].dropna().astype(str).tolist()
        elif file_extension == ".docx":
            doc = Document(file_path)
            return [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        elif file_extension == ".feature":
            with open(file_path, "r", encoding="utf-8") as file:
                return file.readlines()
        else:
            print(f"❌ Unsupported file type: {file_extension}")
            return []

    def process_test_inputs(self, input_folder):
        """Process all test input files and generate corresponding feature and step definition files"""
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)

        existing_steps = self.scan_existing_step_definitions()  # Scan for existing step definitions

        for file_name in os.listdir(input_folder):
            file_path = os.path.join(input_folder, file_name)
            print(f"📂 Processing: {file_name}")
            steps = self.process_file(file_path)
            print(f"📌 Extracted Steps: {steps}")  # Debugging
            self.extract_url_from_steps(steps)
            
            scenarios = {}
            scenario_name = None
            
            for line in steps:
                line = line.strip()
                if line.lower().startswith("test scenario"):
                    scenario_name = line.replace("test scenario", "").strip()
                    scenarios[scenario_name] = []
                elif scenario_name and line:
                    scenarios[scenario_name].append(line)
            
            print(f"📌 Extracted Scenarios: {scenarios}")  # Debugging
            
            if scenarios:
                self.create_files(file_name, scenarios, existing_steps)
                self.execute_scenario(file_name)

    def create_files(self, file_name, scenarios, existing_steps):
        """Save a single feature file and step definitions for all scenarios in a file"""
        os.makedirs("features/steps", exist_ok=True)
        feature_file_path = f"features/{file_name.replace(' ', '_')}.feature"
        step_def_file_path = f"features/steps/{file_name.replace(' ', '_')}_steps.py"
        
        with open(feature_file_path, "w") as f:
            f.write(self.generate_feature_file(file_name, scenarios))
        
        # Check if step definition file exists
        if os.path.exists(step_def_file_path):
            print(f"⚠️ Step definition file already exists: {step_def_file_path} - Skipping generation.")
        else:
            with open(step_def_file_path, "w") as f:
                f.write(self.generate_step_definitions(file_name, scenarios, existing_steps))
            print(f"✅ Step definitions created: {step_def_file_path}")

        print(f"✅ Feature file created: {feature_file_path}")

    def generate_step_definitions(self, file_name, scenarios, existing_steps):
        """Generate step definitions dynamically, avoiding duplicates"""
        step_definitions = f"""
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

driver = None

def get_driver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
"""

        # Ensure "I open the application" step is defined only once globally
        if "I open the application" not in existing_steps:
            step_definitions += f"""
@given('I open the application')
def step_open_browser(context):
    driver = get_driver()
    driver.get("http://localhost:3000/crud-app")
"""
            existing_steps.add("I open the application")

        for scenario, steps in scenarios.items():
            for i, step in enumerate(steps):
                if step not in existing_steps:
                    # Determine the decorator based on the step's position
                    if i == 0:
                        decorator = "@given"
                    elif i == len(steps) - 1:
                        decorator = "@then"
                    else:
                        decorator = "@when"

                    selenium_logic = self.generate_selenium_logic(step)  # Generate Selenium logic
                    # Properly indent the Selenium logic
                    indented_logic = "\n    ".join(selenium_logic.splitlines())
                    step_definitions += f"""
{decorator}('{step}')
def step_{decorator.strip('@')}_{i}(context):
    {indented_logic}
"""
                    existing_steps.add(step)

        # Ensure "I close the browser" step is defined only once
        if "I close the browser" not in existing_steps:
            step_definitions += """
@then("I close the browser")
def step_close_browser(context):
    global driver
    if driver:
        driver.quit()
        driver = None
"""
            existing_steps.add("I close the browser")

        return step_definitions

    def generate_selenium_logic(self, step):
        """Generate Selenium logic based on the step text"""
        if "open" in step and "localhost" in step:
            # Example: Open a specific URL
            url = re.search(r'open\s+(\S+)', step).group(1)
            return f"driver.get('{url}')"
        elif "Login using" in step:
            # Example: Login logic
            match = re.search(r'Login using (\S+) (\S+) and (\S+) (\S+)', step)
            if match:
                email = match.group(2)
                password = match.group(4)
                return f"""
driver.find_element(By.ID, 'email').send_keys('{email}')
driver.find_element(By.ID, 'password').send_keys('{password}')
driver.find_element(By.ID, 'login-button').click()
"""
        elif "click" in step:
            # Example: Click a button
            button_text = re.search(r'click\s+(.+)', step).group(1)
            return f"driver.find_element(By.XPATH, \"//button[text()='{button_text}']\").click()"
        elif "verify" in step:
            # Example: Verify an element is displayed
            element_text = re.search(r'verify\s+(.+)', step).group(1)
            return f"""
element = driver.find_element(By.XPATH, \"//*[text()='{element_text}']\")
assert element.is_displayed(), 'Element not displayed'
"""
        else:
            # Default placeholder logic
            return "pass  # Add custom Selenium logic here"

    def execute_scenario(self, file_name):
        """Run the generated test cases using Behave"""
        print(f"🚀 Running: {file_name}.feature")
        subprocess.run(f"behave features/{file_name.replace(' ', '_')}.feature", shell=True)

# ✅ Load the T5-base model
model = T5ForConditionalGeneration.from_pretrained("t5-base")
tokenizer = T5Tokenizer.from_pretrained("t5-base", use_fast=False, legacy=False)

testing_system = ContextAwareTestingSystem(model, tokenizer)

testing_system.process_test_inputs("test_inputs")
