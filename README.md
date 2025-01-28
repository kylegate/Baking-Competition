# Baking-Competition

# Secure Voting System - Web Application

This project is part of the **Secure, Parallel, and Distributed Computing** course. The goal was to build a secure, full-stack web application using Flask and SQLite3. The system implements role-based access control (RBAC), encrypted data storage, and secure data transmission for a voting system using socket programming.

## Key Features

- **Role-Based Access Control (RBAC)**: Only authorized users (e.g., admin, voter) can access certain parts of the application.
- **Encryption**: Sensitive data is encrypted using the PyCryptodome library and cryptographic techniques.
- **Socket Programming**: The voting system uses encrypted and authenticated socket communication (HMAC, SHA3-512) for secure data transmission.
- **Form-Based User Registration**: Robust client-side and server-side validation to ensure data integrity.
- **Full-Stack Development**: The application is built using Flask (Python), SQLite3 (database), HTML, and CSS.

## Prerequisites

To run the project locally, you'll need:
- Python 3.8 or higher
- Flask
- PyCryptodome
- SQLite3

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/username/Baking-Competition.git
