import os
import json
import threading
import time
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)
TASKS_FILE = "tasks.json"
REMINDER_INTERVAL = 300  # Set reminder interval in seconds (5 minutes)

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
    return render_template('index.html', tasks=tasks, completion_percentage=calculate_completion())

@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['description']
    due_date = request.form['due_date']
    new_task = {
        "description": description,
        "due_date": due_date,
        "completed": False,
        "reminder_sent": False
    }
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """Marks a task as completed and updates the progress bar."""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True  # Mark as completed
    save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Deletes a task by index."""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
    save_tasks(tasks)
    return redirect('/')

def calculate_completion():
    """Calculates task completion percentage."""
    tasks = load_tasks()
    if not tasks:
        return 0
    completed_tasks = sum(1 for task in tasks if task.get("completed", False))
    return round((completed_tasks / len(tasks)) * 100, 2)

def send_notifications():
    """Sends task reminders periodically."""
    while True:
        tasks = load_tasks()
        for task in tasks:
            if not task["completed"] and not task["reminder_sent"]:
                print(f"Reminder: {task['description']} is due on {task['due_date']}")
                task["reminder_sent"] = True
        save_tasks(tasks)
        time.sleep(REMINDER_INTERVAL)  # Wait before sending the next notification

# Start background thread for reminders
threading.Thread(target=send_notifications, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
