const taskForm = document.getElementById("taskForm");
const taskInput = document.getElementById("taskInput");
const dueDateInput = document.getElementById("dueDateInput");
const taskList = document.getElementById("taskList");
const progressBar = document.getElementById("progressBar");
let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

// Load tasks on page load
document.addEventListener("DOMContentLoaded", loadTasks);

function loadTasks() {
  taskList.innerHTML = "";
  tasks.forEach((task, index) => {
    addTaskToUI(task.description, task.dueDate, task.completed, index);
    scheduleReminder(task.description, task.dueDate);
  });
  updateStats();
  updateProgressBar();
}

function addTaskToUI(description, dueDate, completed, index) {
  const taskItem = document.createElement("li");
  taskItem.classList.add("taskItem");

  taskItem.innerHTML = `
    <input type="checkbox" ${completed ? "checked" : ""} onclick="toggleTaskCompletion(${index})" />
    <span class="task-desc ${completed ? "completed" : ""}">${description}</span>
    <span>Due: ${new Date(dueDate).toLocaleString()}</span>
    <div class="icons">
      <img src="/static/images/delete.jpg" alt="Delete Task" onclick="deleteTask(${index})" />
    </div>
  `;

  taskList.appendChild(taskItem);
}

taskForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const description = taskInput.value.trim();
  const dueDate = dueDateInput.value;
  if (description && dueDate) {
    tasks.push({ description, dueDate, completed: false });
    saveTasks();
    loadTasks();
    taskInput.value = "";
    dueDateInput.value = "";
  }
});

function deleteTask(index) {
  tasks.splice(index, 1);
  saveTasks();
  loadTasks();
}

function toggleTaskCompletion(index) {
  tasks[index].completed = !tasks[index].completed;
  saveTasks();
  loadTasks();
}

function saveTasks() {
  localStorage.setItem("tasks", JSON.stringify(tasks));
}

function updateStats() {
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  document.getElementById("numbers").innerText = `${completedTasks}/${totalTasks}`;
}

function updateProgressBar() {
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const progressPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  progressBar.style.width = `${progressPercentage}%`;
  progressBar.innerText = `${Math.round(progressPercentage)}%`;
  
  // Ensure progress bar is visible
  if (totalTasks === 0) {
    progressBar.style.display = "none"; // Hide if no tasks
  } else {
    progressBar.style.display = "block"; // Show if tasks exist
  }
}


// Schedule Desktop Reminders
function scheduleReminder(taskDescription, dueDate) {
  const reminderTime = new Date(dueDate).getTime();
  const currentTime = new Date().getTime();
  const timeDifference = reminderTime - currentTime;

  if (timeDifference > 0) {
    setTimeout(() => {
      showDesktopReminder(taskDescription);
    }, timeDifference);
  }
}

function showDesktopReminder(taskDescription) {
  if (Notification.permission === "granted") {
    new Notification("Task Reminder", {
      body: `Reminder: Your task "${taskDescription}" is pending!`,
      icon: "/static/images/remainder.png"
    });
  } else {
    Notification.requestPermission().then((permission) => {
      if (permission === "granted") {
        showDesktopReminder(taskDescription);
      }
    });
  }
}
