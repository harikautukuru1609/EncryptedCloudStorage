# 🔐 Encrypted Cloud Storage

A secure cloud storage web application developed using **Python and Flask**. The project allows users to register, log in, upload files, and manage their files with encryption for improved data security.

## 📌 Project Overview

**Encrypted Cloud Storage** is a cloud-based file storage system designed to protect user files from unauthorized access.

The application provides a simple web interface where users can:

* Create an account
* Log in securely
* Upload files
* Store encrypted files
* View stored files
* Download files
* Manage their uploaded files

## 🚀 Features

* 🔐 **File Encryption** – Uploaded files are encrypted before storage.
* 👤 **User Authentication** – Registration and login functionality.
* ☁️ **Cloud Storage Concept** – Files are stored and managed through a web application.
* 📁 **File Management** – Users can upload and access their stored files.
* 🛡️ **Secure Storage** – Sensitive files and encryption keys are excluded from GitHub.
* 🌐 **Flask Web Application** – Simple and user-friendly web interface.

## 🛠️ Technologies Used

| Technology   | Purpose             |
| ------------ | ------------------- |
| Python       | Backend programming |
| Flask        | Web framework       |
| HTML         | Web page structure  |
| CSS          | Web page styling    |
| SQLite       | Database            |
| Encryption   | File security       |
| Git & GitHub | Version control     |

## 📂 Project Structure

```text
EncryptedCloudStorage/
│
├── app.py
├── .gitignore
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── test.txt
│
├── uploads/
│   └── ...
│
├── database.db
└── secret.key
```

> **Note:** `database.db`, `secret.key`, and files inside `uploads/` are intentionally excluded from GitHub using `.gitignore`.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/harikautukuru1609/EncryptedCloudStorage-cloud-computing-pro4.git
```

### 2. Open the project

```bash
cd EncryptedCloudStorage-cloud-computing-pro4
```

### 3. Install required packages

```bash
pip install flask cryptography
```

If your project has a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

Go to:

```text
http://127.0.0.1:5000/
```

## 🔒 Security

This project uses encryption to protect uploaded files.

Sensitive files such as:

```text
secret.key
database.db
uploads/
```

are excluded from version control through `.gitignore`.

**Important:** Never upload your actual encryption key or database containing private user information to a public GitHub repository.

## 🎯 Objectives

The main objectives of this project are:

1. To provide secure cloud-based file storage.
2. To protect files using encryption.
3. To implement user authentication.
4. To provide easy file upload and download functionality.
5. To demonstrate the use of cloud computing and cybersecurity concepts.

## 🔮 Future Enhancements

* Two-factor authentication
* Password reset functionality
* Email verification
* File sharing between users
* Cloud deployment using AWS/Azure
* Improved encryption and key management
* File size and storage limits
* Activity and download history
* Admin dashboard

## 👩‍💻 Developer

**Harika Utukuru**

B.Tech – Artificial Intelligence and Data Science

## 📄 License

This project is developed for **educational and academic purposes**.
