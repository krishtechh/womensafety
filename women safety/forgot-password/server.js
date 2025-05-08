// server.js
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

// Twilio configuration
const accountSid = 'ACe5d4f7c41d4b0ba0b413e297df632650';
const authToken = process.env.TWILIO_AUTH_TOKEN; // Get this from your .env file
const verifySid = 'VA663e371814da4100ff60ae76549f995c';
const client = require('twilio')(accountSid, authToken);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Serve the main HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API endpoint to send OTP
app.post('/api/send-otp', async (req, res) => {
  const { phoneNumber } = req.body;
  
  if (!phoneNumber) {
    return res.status(400).json({ success: false, message: 'Phone number is required' });
  }

  try {
    const verification = await client.verify.v2.services(verifySid)
      .verifications
      .create({ to: phoneNumber, channel: 'sms' });
    
    console.log(`Verification SID: ${verification.sid}`);
    res.json({ success: true, message: 'OTP sent successfully' });
  } catch (error) {
    console.error('Error sending OTP:', error);
    res.status(500).json({ 
      success: false, 
      message: error.message || 'Failed to send OTP'
    });
  }
});

// API endpoint to verify OTP
app.post('/api/verify-otp', async (req, res) => {
  const { phoneNumber, otp } = req.body;
  
  if (!phoneNumber || !otp) {
    return res.status(400).json({ success: false, message: 'Phone number and OTP are required' });
  }

  try {
    const verificationCheck = await client.verify.v2.services(verifySid)
      .verificationChecks
      .create({ to: phoneNumber, code: otp });
    
    if (verificationCheck.status === 'approved') {
      res.json({ success: true, message: 'OTP verified successfully' });
    } else {
      res.json({ success: false, message: 'Invalid OTP' });
    }
  } catch (error) {
    console.error('Error verifying OTP:', error);
    res.status(500).json({ 
      success: false, 
      message: error.message || 'Failed to verify OTP'
    });
  }
});

// API endpoint to reset password (this would connect to your database in a real application)
app.post('/api/reset-password', (req, res) => {
  const { phoneNumber, newPassword } = req.body;
  
  if (!phoneNumber || !newPassword) {
    return res.status(400).json({ success: false, message: 'Phone number and new password are required' });
  }

  // In a real application, you would update the password in your database
  // This is just a mock implementation
  console.log(`Resetting password for ${phoneNumber}`);
  res.json({ success: true, message: 'Password reset successfully' });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});