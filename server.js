const express = require("express");
const cors = require("cors");
const nodemailer = require("nodemailer");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Server is running...");
});

app.post("/contact", async (req, res) => {
  const { name, email, subject, message } = req.body;

  const transporter = nodemailer.createTransport({
    host: "smtp.hostinger.com",
    port: 465,
    secure: true,
    auth: {
      user: process.env.MAIL_USER,
      pass: process.env.MAIL_PASS,
    },
  });

 const mailOptions = {
  from: `"${name}" <info@ayuvanaa.com>`,  // ✅ Sender MUST match your SMTP login
  to: process.env.MAIL_RECEIVER,
  subject: `Ayuvanaa Contact - ${subject}`,
  text: `
You received a new message from the Ayuvanaa website:

Name: ${name}
Email: ${email}
Subject: ${subject}
Message:
${message}
  `
};


  try {
    await transporter.sendMail(mailOptions);
    res.status(200).json({ success: true, message: "Email sent successfully." });
  } catch (error) {
    console.error("Mail send error:", error);
    res.status(500).json({ success: false, message: "Failed to send email." });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
