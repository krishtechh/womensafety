import pyautogui
import time
import os
import subprocess
import psutil

def whatsapp_auto_call_with_message(contact_name, message_file, max_attempts=10):
    """
    Automatically call a contact on WhatsApp Desktop until they pick up,
    then play a recorded message.
    
    Args:
        contact_name (str): Exact name of the contact as saved in your phone
        message_file (str): Path to the audio file to play when call is answered
        max_attempts (int): Maximum number of call attempts before giving up
    """
    
    # Verify message file exists
    if not os.path.exists(message_file):
        print(f"Error: Message file '{message_file}' not found.")
        return
    
    # Check if WhatsApp is running, if not launch it
    if not "WhatsApp.exe" in (p.name() for p in psutil.process_iter()):
        os.startfile("whatsapp://")  # This works on Windows
        time.sleep(10)  # Wait for WhatsApp to launch
        
    attempts = 0
    call_answered = False
    
    print(f"Starting automated WhatsApp call to {contact_name}...")
    
    while attempts < max_attempts and not call_answered:
        attempts += 1
        print(f"Attempt {attempts} of {max_attempts}...")
        
        try:
            # Focus on WhatsApp window (assuming it's already open)
            pyautogui.hotkey('alt', 'tab')  # Switch to WhatsApp
            time.sleep(1)
            
            # Open search to find contact
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(1)
            pyautogui.write(contact_name)
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(2)
            
            # Click call button (you'll need to provide coordinates or image)
            try:
                # Method 1: Use image recognition (recommended)
                # You need a screenshot of the call button named 'whatsapp_call_button.png'
                call_button = pyautogui.locateOnScreen('call_button.png', confidence=0.8)
                if call_button:
                    pyautogui.click(call_button)
                
                # Method 2: Use relative coordinates (fragile)
                # pyautogui.click(x=1200, y=150)  # Adjust these coordinates for your screen
                
                print("Call button clicked.")
                time.sleep(2)
                
                # Wait for call to connect (adjust timing as needed)
                print("Waiting for call to be answered...")
                time.sleep(15)  # Assuming call is answered after 15 seconds
                
                # Play the recorded message
                print("Playing recorded message...")
                try:
                    if os.name == 'posix':  # Linux/Mac
                        subprocess.call(['afplay' if os.uname().sysname == 'Darwin' else 'aplay', message_file])
                    else:  # Windows
                        os.startfile(message_file)
                    call_answered = True
                    print("Message played successfully.")
                except Exception as play_error:
                    print(f"Error playing message: {play_error}")
                
            except Exception as e:
                print(f"Could not initiate call: {str(e)}")
                time.sleep(2)
                continue
                
        except Exception as e:
            print(f"Error during attempt {attempts}: {str(e)}")
            time.sleep(5)
            
    if not call_answered:
        print(f"Maximum attempts ({max_attempts}) reached without answer.")
    else:
        print("Call completed successfully.")

if __name__ == "__main__":
    # Configuration - change these values
    CONTACT_NAME = "Arpit"  # Exact name as saved in your contacts
    MESSAGE_FILE = "message.wav"  # Path to your recorded message file
    
    whatsapp_auto_call_with_message(CONTACT_NAME, MESSAGE_FILE)