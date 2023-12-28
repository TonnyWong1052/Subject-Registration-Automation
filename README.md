# Universit Subject Registration Automation

## Overview
This Python script automates the process of registering subjects at university. It allows users to enter their login credentials, select subject codes, groups, and components, and then saves this data to a JSON file. The script can be extended or modified for more complex automation tasks.

## Project Structure
### reg_subject.py
   - **Functionality**: Automates logging into the university system, selecting subjects, and navigating the registration system.
   - **Special Features**:
     - **Alarm Mode**: Allows users to set a specific time for the script to run, automating the process at the scheduled time.
     - **Testing Version (Mock Subject Registration)**: Simulates the registration process, for testing purposes.


## Features
- User input for registration subject code, subject group, and target component codes.
- Saving user credentials and subject information in a JSON file.
- User-friendly display of saved data.

## Requirements
- Python 3.x or above
- Selenium WebDriver
- ChromeDriver (or any compatible driver for your browser)

## Setup and Installation
1. **Install Python**: Ensure you have Python 3.x installed on your machine.
2. **Install Selenium**: Run `pip install selenium` to install the Selenium package.
3. **Download WebDriver**: Download the WebDriver for your browser (e.g., ChromeDriver for Google Chrome) and ensure it's in your PATH.

## Usage
1. **Run the Script**: Execute the script using Python.
   ```bash
   python reg_subject.py
