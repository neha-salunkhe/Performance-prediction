#  Student Performance Predictor
**DS Mini Project | AIDS Sem 4 | NMIET Pune**

A full-stack web app that predicts student academic performance using a weighted scoring model (rule-based ML). Data is stored locally in a JSON file — no SQL or database setup required.

---

## Project Structure

```
student-performance-predictor/
├── app.py            ← Flask backend (REST API + serves index.html)
├── index.html        ← Frontend UI (HTML/CSS/JS)
├── students.json     ← JSON data store (auto-created)
└── README.md         ← This file
```

---

##  Setup & Run

### 1. Install dependencies
```bash
pip install flask
```

### 2. Run the server
```bash
python app.py
```

### 3. Open browser
```
http://localhost:5000
```

Both frontend and backend run on the **same port (5000)** — Flask serves `index.html` directly.

---

##  Prediction Algorithm

The model uses a **weighted scoring system** across 4 features:

| Feature                  | Weight |
|--------------------------|--------|
| Attendance (%)           | 30%    |
| Daily Study Hours        | 25%    |
| Previous Semester Score  | 30%    |
| Assignments Completed (%)| 15%    |

### Grade Mapping

| Score Range | Grade | Label         |
|-------------|-------|---------------|
| 80–100      | A     | Excellent      |
| 65–79       | B     | Good           |
| 50–64       | C     | Average        |
| 35–49       | D     | Below Average  |
| 0–34        | F     | At Risk        |

---

## API Endpoints

| Method | Endpoint               | Description                    |
|--------|------------------------|--------------------------------|
| GET    | `/`                    | Serves the frontend HTML       |
| GET    | `/api/students`        | Get all student records        |
| POST   | `/api/students`        | Add student + get prediction   |
| DELETE | `/api/students/<id>`   | Delete a student record        |
| GET    | `/api/stats`           | Get summary statistics         |

### POST `/api/students` — Sample Request Body
```json
{
  "name": "Ruchi Sharma",
  "roll_no": "AIDS2401",
  "branch": "AIDS",
  "semester": "4",
  "attendance": 85,
  "study_hours": 5,
  "previous_score": 72,
  "assignments_completed": 90
}
```

---

## Features

 Real-time performance prediction on form submit
 Stats dashboard (total students, avg score, at-risk count)
Grade distribution bar chart
 Personalized improvement tips per student
 Delete student records
 JSON file persistence (no DB setup needed)
 Responsive design

---

##  Team

| Member  | Role            |
|---------|-----------------|
| You     | Full Stack (Flask + Frontend) |

---

##  Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Storage:** JSON file (`students.json`)
- **Port:** 5000 (single port for both frontend and API)
