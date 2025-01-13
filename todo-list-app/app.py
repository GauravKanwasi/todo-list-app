from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

# In-memory task storage (store tasks temporarily)
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_data = request.form.get('task')
    
    # Validate input
    if not task_data:
        return jsonify({"error": "Task description cannot be empty"}), 400
    
    task = {
        'id': str(uuid.uuid4()),  # Unique ID for each task
        'task': task_data,
        'completed': False
    }
    tasks.append(task)
    return jsonify(tasks=tasks)

@app.route('/toggle/<task_id>', methods=['POST'])
def toggle_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    # Error handling if task not found
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    task['completed'] = not task['completed']
    return jsonify(tasks=tasks)

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    # Error handling if task not found
    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify(tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
