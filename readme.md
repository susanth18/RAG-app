# RAG Application Setup Guide

This guide will walk you through setting up and running the RAG (Retrieval-Augmented Generation) application that will answer queries related to DeepSeek. Follow the steps below to get started.


---


## Step 1: Clone the Repository

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/RAG.git
   cd RAG-app

## Step 2: Set Up MySQL Database

1. Log in to MySQL:

    ```bash
    mysql -u root -p
2. Create the Database:
     ```bash
    CREATE DATABASE IF NOT EXISTS chatbot_db 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;
     
    USE chatbot_db;
3. Create the chat_history Table:

   ```bash
   CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role ENUM('user', 'system') NOT NULL,
    content TEXT NOT NULL
    );
4. Exit MySQL:
   ```bash
   exit;


## Set up environment variables
1. Create a .env file in the root directory.
2. add the following API keys(for few days i'll keep my api keys here)
   ```bash
   TOGETHER_API_KEY="c00990c5a990a5fea3ea5f3fbeb2fdb751931022d8482f99bd3f6bbc649f9305"
   TOGETHER_BASE_URL="https://api.together.xyz/v1"
   PINECONE_API_KEY="pcsk_7Dz93d_JBq4S38v3DnTVpvsDHWr1udqUMSXM3mru2r41WpRimSaGGCe3tQC8X1zjVebdh2"
   MYSQL_HOST="localhost"
   MYSQL_USER="root"
   MYSQL_PASSWORD="root"
   MYSQL_DB="chatbot_db"

## Install Dependencies
Use the `pip install -r requirements.txt` to install the dependencies


# Run the application:
1. Start the Flask app:
   ```bash
   python app.py

2. Open your application and go to:
   ```bash
   http://localhost:5000

## Demo Questions
1) Why did the US stocks fell?
2) Comparison between DeepSeek and GPT.



   
