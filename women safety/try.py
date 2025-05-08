import webbrowser
import time
import pyautogui
import geocoder
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_current_location():
    """Get current location using IP address"""
    g = geocoder.ip('me')
    return g.latlng

def open_whatsapp_web():
    """Open WhatsApp Web in Chrome"""
    driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
    driver.get("https://web.whatsapp.com")
    return driver

def send_whatsapp_message(driver, contact_name, message):
    """Send a message to a WhatsApp contact"""
    try:
        # Wait for WhatsApp Web to load (you'll need to scan QR code manually the first time)
        wait = WebDriverWait(driver, 60)
        
        # Find the search box and search for the contact
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        search_box.clear()
        search_box.send_keys(contact_name)
        time.sleep(2)  # Wait for search results
        search_box.send_keys(Keys.ENTER)
        
        # Find the message box and type the message
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        
        time.sleep(2)  # Wait for message to send
        
    except Exception as e:
        print(f"Error sending message to {contact_name}: {str(e)}")

def main():
    # Get current location
    latitude, longitude = get_current_location()
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    message = f"My current location: {google_maps_link}"
    
    # Specify your three contacts here
    contacts = ["Arpit"]  # Replace with actual contact names
    
    # Open WhatsApp Web
    driver = open_whatsapp_web()
    
    # Send location to each contact
    for contact in contacts:
        send_whatsapp_message(driver, contact, message)
        print(f"Location sent to {contact}")
    
    # Close the browser after a delay
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()  