const express = require('express');
const path = require('path');
const cors = require('cors');
const { google } = require('googleapis');
const nodemailer = require('nodemailer');
const { OAuth2Client } = require('google-auth-library');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
require('dotenv').config();

// Import User model
const User = require(path.join(__dirname, 'models', 'User'));
const UserChoice = require(path.join(__dirname, 'models', 'UserChoice'));

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files from the root directory
app.use(express.static(path.join(__dirname)));

// add 
const BASE_PATH = process.env.NODE_ENV === 'production' ? '/ReXrank' : '';
app.use(BASE_PATH, express.static(path.join(__dirname)));


const MONGODB_URI = process.env.MONGODB_URI;
const PORT = process.env.PORT || 8080;

console.log('Attempting to connect to MongoDB...');
console.log('MONGODB_URI:', MONGODB_URI);

mongoose.connect(MONGODB_URI, {
  serverSelectionTimeoutMS: 5000
})
.then(() => console.log('Connected to MongoDB successfully'))
.catch(err => {
  console.error('Failed to connect to MongoDB:', err);
});

console.log('Current directory:', __dirname);
console.log('Index.html path:', path.join(__dirname, 'index.html'));

const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 5 // 限制每个 IP 15 分钟内最多 5 次尝试
});

// Google Sheets authentication
const auth = new google.auth.GoogleAuth({
  credentials: JSON.parse(process.env.GOOGLE_APPLICATION_CREDENTIALS),
  scopes: ['https://www.googleapis.com/auth/spreadsheets'],
});

// Set up OAuth2 client
const oauth2Client = new OAuth2Client(
  process.env.CLIENT_ID,
  process.env.CLIENT_SECRET,
  'https://developers.google.com/oauthplayground'
);

oauth2Client.setCredentials({
  refresh_token: process.env.REFRESH_TOKEN
});

// Create Nodemailer transporter
const createTransporter = async () => {
  const accessToken = await oauth2Client.getAccessToken();
  return nodemailer.createTransport({
    service: 'gmail',
    auth: {
      type: 'OAuth2',
      user: process.env.EMAIL_USER,
      clientId: process.env.CLIENT_ID,
      clientSecret: process.env.CLIENT_SECRET,
      refreshToken: process.env.REFRESH_TOKEN,
      accessToken: accessToken.token
    }
  });
};

// Function to send email
const sendEmail = async (to, subject, text) => {
  try {
    const emailTransporter = await createTransporter();
    await emailTransporter.sendMail({
      from: process.env.EMAIL_USER,
      to,
      subject,
      text
    });
    console.log('Email sent successfully');
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
};

function generateToken(length = 20) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let token = '';
  for (let i = 0; i < length; i++) {
    token += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return token;
}

function validateUsername(username) {
  const validUsernameRegex = /^[a-zA-Z0-9-_]+$/;
  return validUsernameRegex.test(username);
}


// Existing route for submitting votes
app.post('/submit-votes', async (req, res) => {
  try {
    console.log('Attempting to append data to Google Sheets');
    const client = await auth.getClient();
    console.log('Client authenticated');
    const sheets = google.sheets({ version: 'v4', auth: client });
    console.log('Sheets API initialized');


    const votes = req.body.votes;
    const timestamp = new Date().toISOString();

    const values = Object.entries(votes).map(([index, vote]) => [timestamp, index, vote]);

    await sheets.spreadsheets.values.append({
      spreadsheetId: '1-EM5gflTN2GmsKBwMFI68IvNXxMoACEuwvQTx_oAV48',
      range: 'Sheet1!A:C',
      valueInputOption: 'RAW',
      resource: { values },
    });

    console.log('Data appended successfully');
    res.json({ success: true });
  } catch (error) {
    console.error('Detailed error:', error);
    console.error('Error message:', error.message);
    if (error.response) {
      console.error('Error response:', error.response.data);
    }
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      details: error.message
    });
  }
});


// Existing route for submitting a single vote
app.post('/submit-vote', async (req, res) => {
  try {
    console.log('Attempting to append single vote to Google Sheets');
    const client = await auth.getClient();
    console.log('Client authenticated');
    const sheets = google.sheets({ version: 'v4', auth: client });
    console.log('Sheets API initialized');

    const { image_id, selected_report, user_id, username } = req.body;
    const timestamp = new Date().toISOString();

    const values = [[timestamp, image_id, selected_report, user_id, username]];

    await sheets.spreadsheets.values.append({
      spreadsheetId: '1-EM5gflTN2GmsKBwMFI68IvNXxMoACEuwvQTx_oAV48',
      range: 'Sheet2!A:E',  // Updated range to include user columns
      valueInputOption: 'RAW',
      resource: { values },
    });

    // const { image_id, selected_report } = req.body;
    // const timestamp = new Date().toISOString();

    // const values = [[timestamp, image_id, selected_report]];

    // await sheets.spreadsheets.values.append({
    //   spreadsheetId: '1-EM5gflTN2GmsKBwMFI68IvNXxMoACEuwvQTx_oAV48',
    //   range: 'Sheet2!A:E',
    //   valueInputOption: 'RAW',
    //   resource: { values },
    // });

    console.log('Single vote data appended successfully');

    // Send confirmation email after successful single vote submission
    // await sendEmail(req.body.userEmail, 'Single Vote Confirmation', 'Your single vote has been successfully submitted. Thank you for your participation!');

    res.json({ success: true, message: 'Vote submitted successfully' });
  } catch (error) {
    console.error('Detailed error:', error);
    console.error('Error message:', error.message);
    if (error.response) {
      console.error('Error response:', error.response.data);
    }
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      details: error.message
    });
  }
});


// Save user choice
app.post('/save-choice', async (req, res) => {
  try {
    const { userId, imageId, choice } = req.body;
    const timestamp = new Date().toISOString();

    // Authenticate and get the Google Sheets client
    const client = await auth.getClient();
    const sheets = google.sheets({ version: 'v4', auth: client });

    // Append the choice to Google Sheets
    await sheets.spreadsheets.values.append({
      spreadsheetId: '1-EM5gflTN2GmsKBwMFI68IvNXxMoACEuwvQTx_oAV48',
      range: 'Sheet2!A:D',
      valueInputOption: 'RAW',
      resource: {
        values: [[timestamp, userId, imageId, choice]],
      },
    });

    res.json({ success: true, message: 'Choice saved successfully' });
  } catch (error) {
    console.error('Error saving choice:', error);
    res.status(500).json({ success: false, message: 'Failed to save choice', error: error.message });
  }
});

// Get user choices
app.get('/get-choices/:userId', async (req, res) => {
  try {
    const userId = req.params.userId;

    // Authenticate and get the Google Sheets client
    const client = await auth.getClient();
    const sheets = google.sheets({ version: 'v4', auth: client });

    // Fetch all choices for the user from Google Sheets
    const response = await sheets.spreadsheets.values.get({
      spreadsheetId: '1-EM5gflTN2GmsKBwMFI68IvNXxMoACEuwvQTx_oAV48',
      range: 'Sheet2!A:D',
    });

    const rows = response.data.values || [];
    const choicesMap = rows.reduce((acc, [timestamp, rowUserId, imageId, choice]) => {
      if (rowUserId === userId) {
        acc[imageId] = choice;
      }
      return acc;
    }, {});

    res.json({ success: true, choices: choicesMap });
  } catch (error) {
    console.error('Error getting user choices:', error);
    res.status(500).json({ success: false, message: 'Failed to get user choices', error: error.message });
  }
});

const SALT_ROUNDS = 10; // Add this line to define SALT_ROUNDS

app.post('/login',loginLimiter， async (req, res) => {
  try {
    const { username, password } = req.body;
    console.log('Login attempt for username:', username);
    console.log('Provided password:', password);

    const user = await User.findOne({ username });
    if (!user) {
      console.log('User not found:', username);
      return res.status(400).json({ message: 'Invalid credentials' });
    }

    console.log('User found:', user);

    if (!user.isVerified) {
      return res.status(400).json({ message: 'Please verify your email before logging in' });
    }
    
    console.log('Stored hashed password:', user.password);
    console.log('Provided password:', password);

    // 手动哈希和比较
    const manualHash = await bcrypt.hash(password, 10);
    console.log('Manually hashed provided password:', manualHash);
    const manualCompare = await bcrypt.compare(password, manualHash);
    console.log('Manual password compare result:', manualCompare);

    // 原始比较
    const isMatch = await bcrypt.compare(password, user.password);
    console.log('Original password match:', isMatch);

    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }
    
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    
    res.json({ token, user: { id: user._id, username: user.username, email: user.email } });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

app.post('/check-username', async (req, res) => {
  try {
    const { username } = req.body;

    if (!username) {
      return res.status(400).json({ error: 'Username is required' });
    }

    // 使用与注册相同的用户名验证逻辑
    const user = await User.findOne({ username });
    
    res.json({ available: !user });
  } catch (error) {
    console.error('Error checking username:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/register', loginLimiter, async (req, res) => {
  try {
    const { username, password, email, institution, degree, country } = req.body;
    console.log('Sending registration data:', { username, password, email, institution, degree, country });
    
    if (!validateUsername(username)) {
      return res.status(400).json({ message: 'Invalid username format' });
    }

    let user = await User.findOne({ $or: [{ username }, { email }] });
    if (user) {
      return res.status(400).json({ message: 'User already exists' });
    }

    console.log('Registering new user:', username);

    const salt = await bcrypt.genSalt(SALT_ROUNDS);
    const hashedPassword = await bcrypt.hash(password, salt);

    // 生成验证令牌
    const verificationToken = crypto.randomBytes(20).toString('hex');

    user = new User({
      username,
      password: hashedPassword,
      email,
      institution,
      degree,
      country,
      isVerified: false,
      verificationToken
    });

    await user.save();

    console.log('User saved to database');

    // add 
    const DEFAULT_BASE_URL = 'https://rexrank.azurewebsites.net/';
    const GITHUB_BASE_URL = 'https://rajpurkarlab.github.io/ReXrank/';

    // 使用环境变量或根据主机名决定 BASE_URL
    const BASE_URL = process.env.BASE_URL || 
                    (process.env.NODE_ENV === 'production' ? GITHUB_BASE_URL : DEFAULT_BASE_URL);

    console.log('BASE_URL:', BASE_URL);


    // 构建验证链接
    const verificationLink = new URL(`verify?token=${verificationToken}`, BASE_URL).toString();

    console.log('Verification link:', verificationLink);

    await sendEmail(
      user.email,
      'Verify Your Email',
      `Please click this link to verify your email: ${verificationLink}`
    );

    console.log('Verification email sent to:', user.email);

    res.status(201).json({ message: 'User registered successfully. Please check your email to verify your account.' });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

app.get('/verify', async (req, res) => {
  try {
    const token = req.query.token;
    console.log('Received verification request with token:', token);

    if (!token) {
      return res.status(400).json({ message: 'Verification token is missing' });
    }

    const user = await User.findOne({ verificationToken: token });
    if (!user) {
      console.log('No user found with token:', token);
      return res.status(400).json({ message: 'Invalid verification token' });
    }
    
    if (user.isVerified) {
      console.log('User already verified:', user.email);
      return res.redirect('/login.html?message=already-verified');
    }
    

    user.isVerified = true;
    // user.verificationToken = undefined;
    await user.save();

    console.log('User verified successfully:', user.email);
    res.redirect('/login.html?message=verified');
  } catch (error) {
    console.error('Verification error:', error);
    res.status(500).json({ message: 'Server error', error: error.message });
  }
});

//     if (user.isVerified) {
//       console.log('User already verified:', user.email);
//       return res.json({ message: 'Email already verified. You can now log in.' });
//     }

//     user.isVerified = true;
//     user.verificationToken = undefined;
//     await user.save();
    
//     console.log('User verified successfully:', user.email);
//     res.json({ message: 'Email verified successfully. You can now log in.' });
//   } catch (error) {
//     console.error('Verification error:', error);
//     res.status(500).json({ message: 'Server error', error: error.message });
//   }
// });



// // 添加邮件验证路由
// app.get('/verify/:token', async (req, res) => {
//   try {
//     const user = await User.findOne({ verificationToken: req.params.token });
//     if (!user) {
//       // 检查是否有已验证的用户曾经使用过这个令牌
//       const verifiedUser = await User.findOne({ 
//         verificationToken: { $exists: false }, 
//         isVerified: true 
//       });
//       if (verifiedUser) {
//         return res.json({ message: 'Email already verified. You can now log in.' });
//       }
//       return res.status(400).json({ message: 'Invalid verification token' });
//     }
    
//     if (user.isVerified) {
//       return res.json({ message: 'Email already verified. You can now log in.' });
//     }

//     user.isVerified = true;
//     user.verificationToken = undefined;
//     await user.save();
    
//     res.json({ message: 'Email verified successfully. You can now log in.' });
//   } catch (error) {
//     console.error('Verification error:', error);
//     res.status(500).json({ message: 'Server error', error: error.message });
//   }
// });

// Root route
app.get(BASE_PATH + '/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get(BASE_PATH + '/*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});


// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error', details: err.message });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Serving static files from: ${path.join(__dirname)}`);
  console.log(`Base path: ${BASE_PATH}`);
});