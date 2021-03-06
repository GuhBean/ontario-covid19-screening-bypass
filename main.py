import driver as webdriver
import mail
import json
from datetime import date
    
def get_filename():
    """Creates filenames for the screenshots"""

    # Naming according to the current date
    return 'screenshots/' + str(date.today()) + '.png'

def get_config():
    """Read the config file"""

    try:
        with open('default.json', mode='r', encoding='utf-8') as config_file:    
           return json.load(config_file)

    except FileNotFoundError:
        with open('config.json', mode='r', encoding='utf-8') as config_file:    
           return json.load(config_file)
       

def handle_website():
    """Handles Driver class from driver.py"""

    # Initialize Driver class
    driver = webdriver.Driver( 
    website = 'https://covid-19.ontario.ca/school-screening/',
    delay = 10
    )

    # Handle screening form
    print('Opening website...')
    driver.open_website()

    print('Starting school screening...')
    driver.start_school_screening()

    print('Selecting student...')
    driver.select_student()

    print('Selecting continue...')
    driver.select_continue('/html/body/div/div[1]/div[2]/main/div/div/div/div[2]/button')

    for i in range(4):
        print(f"No I have not #{i+1}...")
        driver.select_no('/html/body/div/div[1]/div[2]/main/div/div/div/div/div[2]/button[1]')

    print('Selecting continue again...')
    driver.select_continue('/html/body/div/div[1]/div[2]/main/div/div/div/div/div[2]/button')
    
    print('Selecting no...')
    driver.select_no('/html/body/div/div[1]/div[2]/main/div/div/div/div/div[2]/button[1]')

    # Take a screenshot of the verification page and name according to current date
    print('Taking a screenshot...')
    driver.screenshot(get_filename()) 

    # Close browser
    print('Closing the browser...')
    driver.driver.close()

def handle_email():
    """Handles Email class from mail.py"""

    email = mail.Email('smtp.office365.com', 587)

    print('Reading contacts...')
    email.get_contacts()

    print('Reading email template...')
    email.read_template()

    # Setup SMTP server and email to all contacts
    print('Setting up SMTP connection')    
    data = get_config()
    email_address = data['address']
    password = data['password']
    email.setup_smtp_server(email_address, password)
    email.send_email_to_each_contact(
        email_address=email_address, 
        email_subject='COVID-19 Screening', 
        image_path=get_filename()
        )
    
    print('Email(s) Sent!')

def main():
    """Main function"""

    handle_website()
    handle_email()

if __name__ == '__main__':
    main()