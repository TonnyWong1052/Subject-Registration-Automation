from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Process
import datetime
import time
import pytz
import sys
import time
import json
import os

os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'

filename = 'subject_data.json'
# current_directory = os.path.dirname(os.path.abspath(__file__))
# filename = os.path.join(current_directory, filename)


def get_user_input(prompt, default=None):
    user_input = input(prompt)
    return user_input if user_input else default

def get_subject_data():
    reg_subject_code = get_user_input('Enter registration subject code (e.g. SO2S01): ')
    subject_group = get_user_input('Enter subject group (e.g. 201): ')
    component_codes_input = get_user_input('Enter target component codes separated by commas (e.g., LAB001,TUT001,LEC001): ')
    target_component_codes = set(component_codes_input.split(',')) if component_codes_input else set()
    
    return {
        'reg_subject_code': reg_subject_code,
        'subject_group': subject_group,
        'target_component_codes': list(target_component_codes)
    }

def print_user_data(data):
    print("\nSaved Data:")
    print(f"Username: {data['username']}")
    print(f"Password: {data['password']}")
    print(f"Time: {data['booking_date']}")
    print("Subject List:")
    for index, subject in enumerate(data['subject_size'], start=1):
        print(f"  Subject {index}:")
        print(f"    Registration Subject Code: {subject['reg_subject_code']}")
        print(f"    Subject Group: {subject['subject_group']}")
        print(f"    Target Component Codes: {', '.join(subject['target_component_codes'])}")

def show_all_data():
    with open(filename, 'r') as file:
        saved_data = json.load(file)
        print_user_data(saved_data)

def change_user_data():
    username = get_user_input('Enter your PolyU student ID (e.g., 23123456D): ')
    password = get_user_input('Enter your password (e.g., pass0rd): ')
    booking_date = get_user_input('Enter your start time (e.g., 9:00): ')

    subject_data_array = []
    while True:
        subject_data = get_subject_data()
        subject_data_array.append(subject_data)
        
        if get_user_input('Add another subject? (yes/no): ').lower() != 'yes':
            break

    data = {
        'subject_size': subject_data_array,
        'username': username,
        'password': password,
        'booking_date': booking_date
    }

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data saved to {filename}")

    show_all_data()

def subtract_minutes(time_str, minutes):
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    result_obj = time_obj - datetime.timedelta(minutes=minutes)
    result_str = result_obj.strftime("%H:%M")
    
    return result_str

def set_alarm(alarm_time):
    hong_kong_tz = pytz.timezone('Asia/Hong_Kong')
    
    alarm_time = datetime.datetime.strptime(alarm_time, '%H:%M')
    alarm_time = alarm_time.strftime('%H:%M')
    sum = 0
    while True:
        now = datetime.datetime.now(tz=hong_kong_tz).strftime("%H:%M")
        time.sleep(1)
        if now == alarm_time:
            return
        elif sum % 20 == 0:
            print("waitting for the time.....")
            print("Now Time: " + str(now) + ", Alarm setting: " + str(alarm_time))
        sum = sum + 1

def webDriverCover(driver, by_name, element_name):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.presence_of_element_located((by_name, element_name)))

def webdrver_automation(index, reg_subject_code, subject_group, target_component_codes, booking_date, is_alarm, username, password, is_not_testing_verion):
    driver = webdriver.Chrome()

    driver.maximize_window()

    # reg_subject_code = 'SO2S01'
    # subject_group = '201'
    # target_component_codes = {"LAB001", "TUT001", "LEC001"}
    index = str(index)
    beginer_url = 'https://www38.polyu.edu.hk/eStudent/login.jsf'
    driver.get(beginer_url)
    time.sleep(5)

    username_txt = driver.find_element(By.NAME, 'username')
    password_txt = driver.find_element(By.NAME, 'j_password') 

    username_txt.send_keys(username)
    password_txt.send_keys(password)

    signInButton = driver.find_element(By.ID, 'login-button')
    signInButton.click()

    if beginer_url == driver.current_url:
        print(index + ":PolyU estudent account or password incorret!")
        print(index + ":plz config the problem")
        sys.exit(0)

    welcome_url = 'https://www38.polyu.edu.hk/eStudent/secure/home.jsf'

    driver.get(welcome_url)

    if is_not_testing_verion == True:
        nextStep = driver.find_element(By.LINK_TEXT, 'Subject Registration')
    else:
        nextStep = driver.find_element(By.LINK_TEXT, 'Mock Subject Registration')
    print(index + ":Login to PolyU estudent successfully")

    if is_alarm == True:
        set_alarm(booking_date)

    nextStep.click()
    
    try:
        regSubButton = driver.find_element(By.ID, 'mainForm:nextButton')
        regSubButton.click()
    except NoSuchElementException:
        print(index + ":something get error: This function is not available. Please refer to Registration Schedule for details.")
        return
    
    if reg_subject_code is not None:
        searchSubject = driver.find_element(By.ID, 'mainForm:basicSearchSubjectCode')
        searchSubject.send_keys(reg_subject_code)
        print(index + ":Your provided subject code: " + reg_subject_code )

    searchSubButton = driver.find_element(By.ID, 'mainForm:basicSearchButton')
    searchSubButton.click()

    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.ID, "mainForm:basicSearchTable:0:basicSearchAddSubjectButton_")))
    table.click()

    wait = WebDriverWait(driver, 10)
    dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "mainForm:selectCompSubjectGroup")))

    select = Select(dropdown_element)

    for option in select.options:
        if subject_group in option.text: 
            select.select_by_visible_text(option.text)
            break

    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.ID, "mainForm:ComponentTable")))

    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.ID, "mainForm:ComponentTable")))

    rows = table.find_elements(By.TAG_NAME, "tr")

    click_count = len(target_component_codes)
    for row in rows:
        try:
            component_code_cell = row.find_element(By.CSS_SELECTOR, "span[id*='selectCompCode']")
            #print(index + ":found existing component code: " + component_code_cell.text)
            if component_code_cell.text in target_component_codes:
                checkbox = row.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                checkbox.click()
                click_count = click_count - 1
                print(index + ":component code: " + component_code_cell.text + " has been select")
                if click_count == 0:
                    break
        except Exception:
            table = wait.until(EC.presence_of_element_located((By.ID, "mainForm:ComponentTable")))
            rows = table.find_elements(By.TAG_NAME, "tr")
            continue
        
    if click_count != 0:
        print(index + ":Something get error: target_component_codes error")
        return

    webDriverCover(driver, By.ID, 'mainForm:selectButton').click()
    webDriverCover(driver, By.ID, 'mainForm:confirmButton').click()
    webDriverCover(driver, By.ID, 'mainForm:confirmButton').click()

    info_block_text = driver.find_element(By.CLASS_NAME ,"info-block").text

    if 'successfully completed' in info_block_text and 'unsuccessfully' not in info_block_text:
        print("\n" + index + ":Subject Registration successfully!!! " + reg_subject_code)
    else:
        print(index + ":Registration unsuccessfully!!! " + reg_subject_code)
    print(index + ":PolyU eStudent System Message:\n" + info_block_text)

    driver.quit()

def run_webDriver_via_data(is_not_testing_verion, is_alarm):
    with open(filename, 'r') as file:
        data = json.load(file)

    username = data.get('username')
    password = data.get('password')
    booking_date = data.get('booking_date')

    if is_alarm == True:
        print(f"open the browser when time's up {booking_date} - 5 min")
        print("Sleeping model start: ")
        set_alarm(subtract_minutes(booking_date, 5))
    processes = []
    with open(filename, 'r') as file:
        for index, subject in enumerate(data['subject_size'], start=1):
            process = Process(target=webdrver_automation, args=(index, subject['reg_subject_code'], subject['subject_group'], subject['target_component_codes'],
                                  booking_date, is_alarm, username, password, is_not_testing_verion,))
            process.start()
            processes.append(process)

            # webdrver_automation(index, subject['reg_subject_code'], subject['subject_group'], subject['target_component_codes'],
            #                       booking_date, is_alarm, username, password, is_not_testing_verion)

        for process in processes:
            process.join()

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()

    print("\nWelcome to PolyU subject registration program! ")
    while True:
        number = input("\nEnter 1 to edit subject data, 2 to run the program, 3 to show all data, 4 to exit the program. ")
        if number == "1":
            change_user_data()
        elif number == "2":
            verion_num = input("Enter 0 for the testing version (Mock subject registration). otherwise, proceed with the actual subject registration (eg. 1)). ")
            alarm_num = input("Enter 0 for alarm mode. otherwise, run the program in real-time. \n")
            
            if int(verion_num) == 0:
                verion_bool = False
            else:
                verion_bool = True
            
            if int(alarm_num) == 0:
                alarm_bool = True
            else:
                alarm_bool = False

            run_webDriver_via_data(is_not_testing_verion=verion_bool, is_alarm=alarm_bool)
        elif number == "3":
            show_all_data()
        elif number == "4":
            break
    print("System exit")