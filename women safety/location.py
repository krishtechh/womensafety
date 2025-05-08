import sys
import io
import requests
import time
import pyautogui
import subprocess

# Fix Unicode errors in Windows CMD
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_current_location():
    try:
        # Try Google Geolocation API
        url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyD9ByIVGvJxHm-6e9k8kP7XQYJN2kXqX9Y'
        data = {'considerIp': True, 'wifiAccessPoints': [], 'cellTowers': []}
        response = requests.post(url, json=data).json()
        if 'location' in response:
            return response['location']['lat'], response['location']['lng']
    except:
        pass
    
    # Fallback to IP-based geolocation
    try:
        response = requests.get('https://ipinfo.io/json').json()
        loc = response['loc'].split(',')
        return float(loc[0]), float(loc[1])
    except Exception as e:
        raise Exception(f"Could not determine location: {str(e)}")

def send_whatsapp_location_fully_auto(phone_numbers):
    try:
        # Get current location
        latitude, longitude = get_current_location()
        maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
        
        for phone in phone_numbers:
            # Method 1: Try opening WhatsApp via Start Menu (works on most systems)
            try:
                subprocess.Popen(["WhatsApp"])  # Opens via Start Menu name
            except:
                # Method 2: Try default install path (update if needed)
                whatsapp_paths = [
                    "C:\\Program Files\\WindowsApps\\5319275A.WhatsAppDesktop_2.2405.6.0_x64__cv1g1gvanyjgm\\WhatsApp.exe",
                    "C:\\Users\\hp\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
                ]
                for path in whatsapp_paths:
                    try:
                        subprocess.Popen([path])
                        break
                    except:
                        continue
                else:
                    raise Exception("WhatsApp not found. Install it first.")

            time.sleep(5)  # Wait for WhatsApp to load

            # Focus search bar (Ctrl + N)
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(1)

            # Type phone number & press Enter
            pyautogui.write(phone)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)  # Wait for chat to open

            # Send Google Maps link
            pyautogui.write(maps_link)
            time.sleep(1)
            pyautogui.press('enter')
            print(f"✓ Location sent to {phone}")

            # Close chat (optional)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'w')

    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    phone_numbers = ["919311293521"]  # No + symbol
    send_whatsapp_location_fully_auto(phone_numbers)

if __name__ == "__main__":
    main()