from flask import Flask, request, jsonify, send_from_directory
import json
import os
import math
from datetime import datetime

app = Flask(__name__, static_folder='.')

DATA_FILE = 'students.json'

# ── helpers ──────────────────────────────────────────────────────────────────

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def predict_performance(student):
    """Simple rule-based ML-style prediction using weighted scoring."""
    score = 0

    # Attendance weight: 30%
    att = student['attendance']
    if att >= 90: score += 30
    elif att >= 75: score += 22
    elif att >= 60: score += 12
    else: score += 0

    # Study hours weight: 25%
    hrs = student['study_hours']
    if hrs >= 6: score += 25
    elif hrs >= 4: score += 18
    elif hrs >= 2: score += 10
    else: score += 3

    # Previous score weight: 30%
    prev = student['previous_score']
    score += (prev / 100) * 30

    # Assignments weight: 15%
    asgn = student['assignments_completed']
    if asgn >= 90: score += 15
    elif asgn >= 70: score += 10
    elif asgn >= 50: score += 6
    else: score += 2

    # Map score → grade & label
    if score >= 80:
        grade, label, color = 'A', 'Excellent', 'excellent'
    elif score >= 65:
        grade, label, color = 'B', 'Good', 'good'
    elif score >= 50:
        grade, label, color = 'C', 'Average', 'average'
    elif score >= 35:
        grade, label, color = 'D', 'Below Average', 'below'
    else:
        grade, label, color = 'F', 'At Risk', 'risk'

    # Build tips
    tips = []
    if att < 75:
        tips.append("Attendance is critically low — aim for at least 75%.")
    if hrs < 4:
        tips.append("Increase daily study hours to at least 4 hrs.")
    if prev < 50:
        tips.append("Focus on revisiting fundamentals from previous semester.")
    if asgn < 70:
        tips.append("Complete pending assignments to improve internal marks.")
    if not tips:
        tips.append("Great consistency! Keep it up and aim for higher targets.")

    return {
        'predicted_score': round(score, 2),
        'grade': grade,
        'label': label,
        'color': color,
        'tips': tips
    }

# ── routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(load_data())

@app.route('/api/students', methods=['POST'])
def add_student():
    body = request.get_json()
    required = ['name', 'roll_no', 'attendance', 'study_hours',
                'previous_score', 'assignments_completed']
    for field in required:
        if field not in body:
            return jsonify({'error': f'Missing field: {field}'}), 400

    data = load_data()

    # Check duplicate roll number
    for s in data:
        if s['roll_no'] == body['roll_no']:
            return jsonify({'error': 'Roll number already exists'}), 409

    prediction = predict_performance(body)
    student = {
        'id': int(datetime.now().timestamp() * 1000),
        'name': body['name'],
        'roll_no': body['roll_no'],
        'branch': body.get('branch', 'N/A'),
        'semester': body.get('semester', 'N/A'),
        'attendance': float(body['attendance']),
        'study_hours': float(body['study_hours']),
        'previous_score': float(body['previous_score']),
        'assignments_completed': float(body['assignments_completed']),
        'prediction': prediction,
        'created_at': datetime.now().isoformat()
    }

    data.append(student)
    save_data(data)
    return jsonify(student), 201

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    data = load_data()
    new_data = [s for s in data if s['id'] != student_id]
    if len(new_data) == len(data):
        return jsonify({'error': 'Student not found'}), 404
    save_data(new_data)
    return jsonify({'message': 'Deleted successfully'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    data = load_data()
    if not data:
        return jsonify({'total': 0, 'avg_score': 0, 'grade_dist': {}})

    total = len(data)
    avg_score = sum(s['prediction']['predicted_score'] for s in data) / total
    grade_dist = {}
    for s in data:
        g = s['prediction']['grade']
        grade_dist[g] = grade_dist.get(g, 0) + 1

    at_risk = sum(1 for s in data if s['prediction']['grade'] == 'F')

    return jsonify({
        'total': total,
        'avg_score': round(avg_score, 2),
        'grade_dist': grade_dist,
        'at_risk': at_risk
    })

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        save_data([])
    print("🚀 Student Performance Predictor running at http://localhost:5000")
    app.run(debug=True, port=5000)
