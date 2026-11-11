from flask import Flask, jsonify, request
app = Flask(__name__)
print("Python backend running using Flask")

students = [{"id": 1, "name": "Rahul"}, {"id": 2, "name": "Priya"}]

@app.get("/")
def home():
    return "Flask backend is running!"

@app.get("/students")
def get_students():
    return jsonify(students)

@app.post("/students")
def add_student():
    data = request.get_json(silent=True) or {}
    if not data.get("name"):
        return jsonify({"error": "name is required"}), 400
    student = {"id": max([s["id"] for s in students], default=0) + 1,
               "name": data["name"]}
    students.append(student)
    return jsonify(student), 201

@app.put("/students/<int:student_id>")
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    for student in students:
        if student["id"] == student_id:
            student["name"] = data.get("name", student["name"])
            return jsonify(student)
    return jsonify({"error": "student not found"}), 404

@app.delete("/students/<int:student_id>")
def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return jsonify({"message": "deleted"})
    return jsonify({"error": "student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)