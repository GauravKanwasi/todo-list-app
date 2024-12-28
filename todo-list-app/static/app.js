document.addEventListener("DOMContentLoaded", function () {
  const addTaskForm = document.getElementById("addTaskForm");
  const taskInput = document.getElementById("taskInput");
  const taskList = document.getElementById("taskList");

  // Handle task addition
  addTaskForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const task = taskInput.value.trim();
    if (task) {
      fetch("/add", {
        method: "POST",
        body: new URLSearchParams({ task: task }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      })
        .then((response) => response.json())
        .then((data) => {
          renderTasks(data.tasks);
          taskInput.value = "";
        });
    }
  });

  // Handle task completion and deletion
  taskList.addEventListener("click", function (e) {
    const taskId = e.target.closest("li").dataset.id;
    if (e.target.classList.contains("toggle-btn")) {
      fetch(`/toggle/${taskId}`, { method: "POST" })
        .then((response) => response.json())
        .then((data) => renderTasks(data.tasks));
    }
    if (e.target.classList.contains("delete-btn")) {
      fetch(`/delete/${taskId}`, { method: "POST" })
        .then((response) => response.json())
        .then((data) => renderTasks(data.tasks));
    }
  });

  // Render tasks on page
  function renderTasks(tasks) {
    taskList.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.dataset.id = task.id;
      li.classList.toggle("completed", task.completed);
      li.innerHTML = `
                <span class="task-text">${task.task}</span>
                <button class="toggle-btn">✔️</button>
                <button class="delete-btn">❌</button>
            `;
      taskList.appendChild(li);
    });
  }

  // Initialize tasks from server
  fetch("/")
    .then((response) => response.json())
    .then((data) => renderTasks(data.tasks));
});
