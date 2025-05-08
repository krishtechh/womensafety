from flask import Flask, request, jsonify
from flask_cors import CORS
from random import randint
from twilio.rest import Client

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Twilio Credentials (Replace with your real credentials)
TWILIO_ACCOUNT_SID = "ACe5d4f7c41d4b0ba0b413e297df632650"
TWILIO_AUTH_TOKEN = "36f3273d98db21159ff4d9e5589b8e61"
TWILIO_PHONE_NUMBER = "9311293521"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Dictionary to store OTPs temporarily (In real apps, use a database)
otp_storage = {}

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    phone = data.get('phone')

    if not phone:
        return jsonify({"success": False, "message": "Phone number required"}), 400

    otp = str(randint(1000, 9999))  # Generate a random 4-digit OTP
    otp_storage[phone] = otp  # Store OTP temporarily

    try:
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        return jsonify({"success": True, "message": "OTP sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error sending OTP: {str(e)}"}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    phone = data.get('phone')
    otp = data.get('otp')

    if phone in otp_storage and otp_storage[phone] == otp:
        del otp_storage[phone]  # Remove OTP after verification
        return jsonify({"success": True, "message": "OTP Verified!"})
    return jsonify({"success": False, "message": "Invalid OTP!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
