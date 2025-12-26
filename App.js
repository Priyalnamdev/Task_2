import React, { useEffect, useState } from "react";
import API from "./src/api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [taskTitle, setTaskTitle] = useState("");
  const [selectedTask, setSelectedTask] = useState(null);
  const [commentText, setCommentText] = useState("");
  const [comments, setComments] = useState([]);

  // Load all tasks
  const loadTasks = async () => {
    const res = await API.get("/tasks");
    setTasks(res.data);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  // Create task
  const createTask = async () => {
    if (!taskTitle) return alert("Enter task title");
    await API.post("/tasks", { title: taskTitle });
    setTaskTitle("");
    loadTasks();
  };

  // Load comments of selected task
  const loadComments = async (taskId) => {
    setSelectedTask(taskId);
    const res = await API.get(`/tasks/${taskId}/comments`);
    setComments(res.data);
  };

  // Add comment
  const addComment = async () => {
    if (!commentText) return alert("Enter comment");
    await API.post(`/tasks/${selectedTask}/comments`, {
      content: commentText,
    });
    setCommentText("");
    loadComments(selectedTask);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Task & Comment Manager</h2>

      {/* Create Task */}
      <h3>Create Task</h3>
      <input
        value={taskTitle}
        onChange={(e) => setTaskTitle(e.target.value)}
        placeholder="Task title"
      />
      <button onClick={createTask}>Add Task</button>

      <hr />

      {/* Task List */}
      <h3>Tasks</h3>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {task.title}
            <button
              style={{ marginLeft: "10px" }}
              onClick={() => loadComments(task.id)}
            >
              View Comments
            </button>
          </li>
        ))}
      </ul>

      <hr />

      {/* Comments Section */}
      {selectedTask && (
        <>
          <h3>Comments for Task ID {selectedTask}</h3>

          <input
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            placeholder="Write a comment"
          />
          <button onClick={addComment}>Add Comment</button>

          <ul>
            {comments.map((c) => (
              <li key={c.id}>{c.content}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
