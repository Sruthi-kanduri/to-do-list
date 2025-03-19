import os
from flask import Flask, render_template, request, jsonify, redirect
import json
from datetime import datetime

app = Flask(__name__)
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['description']
    due_date = request.form['due_date']
    new_task = {
        "description": description,
        "due_date": due_date,
        "reminder_sent": False
    }
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
    save_tasks(tasks)
    return redirect('/')

@app.route('/notify', methods=['POST'])
def send_notification():
    """Sends a notification request to the client."""
    data = request.get_json()
    title = data.get('title', 'Task Reminder')
    message = data.get('message', 'This is your reminder.')
    return jsonify({"title": title, "message": message}), 200

if __name__ == "__main__":
    # Bind to the correct host and port
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT as an environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
