from flask import Flask, request, jsonify
from flask_cors import CORS  
import pyodbc

app = Flask(__name__)
CORS(app)  

def connect_db():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-R2CBT3QU\\SQLEXPRESS;"
        "DATABASE=accidents_db;"
        "Trusted_Connection=yes;"
    )
    return conn

@app.route('/')
def home():
    return "Traffic Accidents API is running!"
@app.route('/get_accidents', methods=['GET'])
def get_accidents():
    date = request.args.get('date')  
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM traffic_accidents WHERE accident_date = ?"
    cursor.execute(query, (date,))
    
    accidents = []
    for row in cursor.fetchall():
        accidents.append({
            "id": row.accident_id,
            "date": row.accident_date.strftime("%Y-%m-%d"),
            "time": row.accident_time.strftime("%H:%M"),
            "location": row.location,
            "weather": row.weather,
            "cause": row.cause,
            "vehicles_involved": row.vehicles_involved,
            "casualties": row.casualties
        })

    conn.close()
    
    if not accidents:
        return jsonify({"message": "No accidents found for this date"}), 404

    return jsonify(accidents)

@app.route('/add_accident', methods=['POST'])
def add_accident():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    
    query = """INSERT INTO traffic_accidents 
               (accident_date, accident_time, location, weather, cause, vehicles_involved, casualties) 
               VALUES (?, ?, ?, ?, ?, ?, ?)"""
    
    cursor.execute(query, (
        data['date'], data['time'], data['location'], data['weather'], 
        data['cause'], data['vehicles_involved'], data['casualties']
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Accident record added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
