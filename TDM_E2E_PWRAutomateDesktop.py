import keyboard
import time
import os
import sys
import pyautogui
from datetime import datetime

class TDM_E2E_PWRAutomateDesktop:
    def __init__(self, file_name, timeout, interval):
        self.file_name = file_name
        self.timeout = timeout
        self.interval = interval
        # Get the Jenkins build number from the environment variables
        self.build_number = os.environ.get('BUILD_NUMBER')
        self.jenkins_buildNumber_file_path = os.path.expanduser("~") + '/Jenkins_BuildNumber.txt'
        self.directory_path = os.path.expanduser("~") + "/screenshots/" + self.build_number
        self.file_path = self.directory_path + '\\' + self.file_name + '.txt'

    def ensure_directory_exists(self, directory):
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Directory '{directory}' created successfully.")
            except OSError as e:
                print(f"Failed to create directory '{directory}': {e}")
        else:
            print(f"Directory '{directory}' already exists.")

    def delete_file_if_exists(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print(f"File '{self.file_path}' deleted successfully.")
        else:
            print(f"File '{self.file_path}' does not exist.")

    def read_file_content(self):
        start_time = time.time()
               
        while time.time() - start_time < self.timeout:
            if os.path.isfile(self.file_path):
                with open(self.file_path, 'r') as file:
                    print(f"File found: {self.file_path}")
                    try:
                        with open(self.file_path, 'r', encoding='utf-16') as file:
                            content = file.read().strip()
                            return content
                    except FileNotFoundError:
                        print(f"Error: File '{self.file_path}' not found.")
                        return None
                return content
            else:
                print(f"File not found: {self.file_path}. Checking again in {self.interval} seconds.")
                time.sleep(self.interval)
        print(f"Failure: File not found within the given timeout period of {self.timeout} seconds.")
        return None

    def check_file_content(self, file_content):
        if file_content == 'True':
            print("File content: " + file_content)
            end_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print('End Time: ' + end_time)
            sys.exit(0)
        elif file_content is not None:
            print("File content: " + file_content)
            end_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print('End Time: ' + end_time)
            sys.exit(1)
        else:
            end_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print('End Time: ' + end_time)
            sys.exit(1)
            
    def write_build_number(self, build_number, jenkins_buildNumber_file_path):
        # Write the build number to the file
        with open(jenkins_buildNumber_file_path, 'w') as file:
            file.write(build_number)
        print(f"Build number {self.build_number} has been written to {self.jenkins_buildNumber_file_path}")

    def run(self):
        execution_start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print('Start Time: ' + execution_start_time)
        self.write_build_number(self.build_number, self.jenkins_buildNumber_file_path)
        self.ensure_directory_exists(self.directory_path)
        self.delete_file_if_exists()
        keyboard.send("ctrl+alt+s")
        print("Keys Pressed to close existing running power automate flow")
        time.sleep(10)
        keyboard.send("ctrl+alt+p")
        print("Keys Pressed and Wait for default timeout of 15 Minutes")
        time.sleep(30)
        screenshot = pyautogui.screenshot()
        screenshot.save(self.directory_path + '/TDM_E2E_screenshot_start.png')
        time.sleep(600)
        print("Checking file status after 10 Minutes")
        file_content = self.read_file_content()
        screenshot = pyautogui.screenshot()
        screenshot.save(self.directory_path + '/TDM_E2E_screenshot_end.png')
        self.check_file_content(file_content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python TDM_E2E_PWRAutomateDesktop.py <timeout> <interval>")
        sys.exit(1)
    file_name = 'TDM_E2E_FlowStatus'
    timeout = int(sys.argv[1])
    interval = int(sys.argv[2])
    automation = TDM_E2E_PWRAutomateDesktop(file_name, timeout, interval)
    automation.run()
