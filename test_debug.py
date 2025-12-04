
try:
    print("Importing flask...")
    from flask import Flask, render_template, jsonify
    print("Importing mysql.connector...")
    import mysql.connector
    from mysql.connector import Error
    print("Importing os...")
    import os
    print("Importing dotenv...")
    from dotenv import load_dotenv

    print("Loading dotenv...")
    load_dotenv()
    print("Dotenv loaded.")
    
    print("Connecting to DB...")
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    print("Connected.")
    conn.close()
    
    app = Flask(__name__)
    print("Flask app created.")

except Exception as e:
    print(f"CRASHED: {e}")
