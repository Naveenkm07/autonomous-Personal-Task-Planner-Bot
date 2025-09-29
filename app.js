// Application Data
const applicationData = {
  "agents": [
    {
      "id": "wf1",
      "name": "Collector Agent",
      "description": "Monitors and collects data every 15 minutes",
      "status": "active",
      "lastExecution": "2025-09-29T20:45:00Z",
      "nextExecution": "2025-09-29T21:00:00Z",
      "successRate": 98.5,
      "avgExecutionTime": 12.3,
      "schedule": "*/15 * * * *"
    },
    {
      "id": "wf2",
      "name": "Planner Agent",
      "description": "Intelligent planning and conflict resolution",
      "status": "active",
      "lastExecution": "2025-09-29T20:46:15Z",
      "nextExecution": "On demand",
      "successRate": 95.2,
      "avgExecutionTime": 8.7,
      "schedule": "Triggered by Collector"
    },
    {
      "id": "wf3",
      "name": "Executor Agent",
      "description": "Executes approved plans and notifications",
      "status": "active",
      "lastExecution": "2025-09-29T20:47:30Z",
      "nextExecution": "On demand",
      "successRate": 97.1,
      "avgExecutionTime": 6.2,
      "schedule": "Triggered by Planner"
    },
    {
      "id": "wf4",
      "name": "Reviewer & Learner Agent",
      "description": "Analyzes patterns daily at 10 PM",
      "status": "scheduled",
      "lastExecution": "2025-09-28T22:00:00Z",
      "nextExecution": "2025-09-29T22:00:00Z",
      "successRate": 100,
      "avgExecutionTime": 45.8,
      "schedule": "0 22 * * *"
    }
  ],
  "tasks": [
    {
      "id": "task-1",
      "title": "Morning workout",
      "description": "30-minute cardio session",
      "priority": 2,
      "status": "completed",
      "deadline": "2025-09-30T07:00:00Z",
      "createdAt": "2025-09-29T06:00:00Z",
      "completedAt": "2025-09-29T07:15:00Z"
    },
    {
      "id": "task-2", 
      "title": "Team meeting preparation",
      "description": "Review agenda and prepare presentation",
      "priority": 1,
      "status": "in-progress",
      "deadline": "2025-09-30T14:00:00Z",
      "createdAt": "2025-09-29T09:00:00Z"
    },
    {
      "id": "task-3",
      "title": "Grocery shopping",
      "description": "Weekly grocery run - check weather",
      "priority": 3,
      "status": "pending",
      "deadline": "2025-09-30T18:00:00Z",
      "createdAt": "2025-09-29T10:30:00Z"
    },
    {
      "id": "task-4",
      "title": "Code review",
      "description": "Review pull requests for autonomous planner",
      "priority": 1,
      "status": "pending",
      "deadline": "2025-09-30T16:00:00Z",
      "createdAt": "2025-09-29T11:00:00Z"
    }
  ],
  "systemMetrics": {
    "uptime": "15 days, 7 hours, 23 minutes",
    "totalExecutions": 1247,
    "successfulExecutions": 1211,
    "failedExecutions": 36,
    "averageResponseTime": 15.7,
    "apiCalls": {
      "gemini": 892,
      "googleCalendar": 445,
      "notion": 623,
      "openWeather": 289,
      "telegram": 156
    }
  },
  "recentActivity": [
    {
      "timestamp": "2025-09-29T20:47:30Z",
      "agent": "Executor Agent",
      "action": "Created 3 calendar events",
      "status": "success"
    },
    {
      "timestamp": "2025-09-29T20:46:15Z",
      "agent": "Planner Agent", 
      "action": "Optimized daily plan - resolved 2 conflicts",
      "status": "success"
    },
    {
      "timestamp": "2025-09-29T20:45:00Z",
      "agent": "Collector Agent",
      "action": "Data collection completed",
      "status": "success"
    },
    {
      "timestamp": "2025-09-29T20:30:12Z",
      "agent": "Collector Agent",
      "action": "Weather data updated - Rain expected",
      "status": "info"
    }
  ],
  "analytics": {
    "executionTimes": [
      {"time": "06:00", "collector": 11.2, "planner": 7.8, "executor": 5.9},
      {"time": "12:00", "collector": 12.8, "planner": 9.1, "executor": 6.4},
      {"time": "18:00", "collector": 13.5, "planner": 8.9, "executor": 6.8},
      {"time": "22:00", "collector": 12.1, "planner": 8.2, "executor": 6.1}
    ],
    "successRates": [
      {"date": "2025-09-25", "collector": 98, "planner": 95, "executor": 97, "reviewer": 100},
      {"date": "2025-09-26", "collector": 99, "planner": 94, "executor": 98, "reviewer": 100},
      {"date": "2025-09-27", "collector": 97, "planner": 96, "executor": 96, "reviewer": 100},
      {"date": "2025-09-28", "collector": 99, "planner": 95, "executor": 97, "reviewer": 100},
      {"date": "2025-09-29", "collector": 98, "planner": 95, "executor": 97, "reviewer": 100}
    ]
  }
};

// Global variables
let currentView = 'overview';
let currentTaskFilter = 'all';
let currentEditingTask = null;
let executionChart = null;
let successChart = null;

// Utility functions
function formatDateTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString();
}

function formatTimeAgo(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffInMinutes = Math.floor((now - date) / (1000 * 60));
  
  if (diffInMinutes < 1) return 'Just now';
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
  return `${Math.floor(diffInMinutes / 1440)}d ago`;
}

function getPriorityText(priority) {
  const priorities = { 1: 'High', 2: 'Medium', 3: 'Low' };
  return priorities[priority] || 'Unknown';
}

function getStatusClass(status) {
  const statusClasses = {
    'active': 'status--success',
    'scheduled': 'status--warning',
    'inactive': 'status--error',
    'pending': 'status--pending',
    'in-progress': 'status--info',
    'completed': 'status--completed'
  };
  return statusClasses[status] || 'status--info';
}

// Navigation
function initNavigation() {
  const navButtons = document.querySelectorAll('.nav-btn');
  navButtons.forEach(button => {
    button.addEventListener('click', () => {
      const view = button.getAttribute('data-view');
      switchView(view);
      
      // Update active button
      navButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
    });
  });
}

function switchView(viewId) {
  // Hide all views
  document.querySelectorAll('.view').forEach(view => {
    view.classList.remove('active');
  });
  
  // Show selected view
  document.getElementById(viewId).classList.add('active');
  currentView = viewId;
  
  // Initialize view-specific content
  switch (viewId) {
    case 'overview':
      initOverviewView();
      break;
    case 'agents':
      initAgentsView();
      break;
    case 'tasks':
      initTasksView();
      break;
    case 'analytics':
      initAnalyticsView();
      break;
    case 'config':
      initConfigView();
      break;
    case 'logs':
      initLogsView();
      break;
  }
}

// Overview View
function initOverviewView() {
  renderRecentActivity();
  updateAgentTriggerButtons();
}

function renderRecentActivity() {
  const activityList = document.getElementById('activityList');
  if (!activityList) return;
  
  activityList.innerHTML = '';
  
  applicationData.recentActivity.forEach(activity => {
    const activityItem = document.createElement('div');
    activityItem.className = `activity-item ${activity.status}`;
    activityItem.innerHTML = `
      <div class="activity-info">
        <div class="activity-agent">${activity.agent}</div>
        <div class="activity-action">${activity.action}</div>
      </div>
      <div class="activity-time">${formatTimeAgo(activity.timestamp)}</div>
    `;
    activityList.appendChild(activityItem);
  });
}

function updateAgentTriggerButtons() {
  const triggerButtons = document.querySelectorAll('.trigger-btn');
  triggerButtons.forEach(button => {
    button.addEventListener('click', () => {
      const agentId = button.getAttribute('data-agent');
      triggerAgent(agentId, button);
    });
  });
}

function triggerAgent(agentId, button) {
  const originalText = button.textContent;
  button.innerHTML = '<span class="loading"></span> Executing...';
  button.disabled = true;
  
  // Simulate agent execution
  setTimeout(() => {
    button.textContent = originalText;
    button.disabled = false;
    
    // Add to recent activity
    const agent = applicationData.agents.find(a => a.id === agentId);
    if (agent) {
      const newActivity = {
        timestamp: new Date().toISOString(),
        agent: agent.name,
        action: 'Manual execution completed',
        status: 'success'
      };
      applicationData.recentActivity.unshift(newActivity);
      if (applicationData.recentActivity.length > 10) {
        applicationData.recentActivity.pop();
      }
      
      // Re-render activity if we're on overview
      if (currentView === 'overview') {
        renderRecentActivity();
      }
    }
  }, 2000);
}

// Agents View
function initAgentsView() {
  const agentSelector = document.getElementById('agentSelector');
  const executeButton = document.getElementById('executeAgent');
  const viewLogsButton = document.getElementById('viewLogs');
  
  if (agentSelector) {
    agentSelector.addEventListener('change', updateAgentDetails);
  }
  
  if (executeButton) {
    executeButton.addEventListener('click', () => {
      const selectedAgent = agentSelector ? agentSelector.value : 'wf1';
      triggerAgent(selectedAgent, executeButton);
    });
  }
  
  if (viewLogsButton) {
    viewLogsButton.addEventListener('click', () => {
      switchView('logs');
    });
  }
  
  updateAgentDetails();
}

function updateAgentDetails() {
  const agentSelector = document.getElementById('agentSelector');
  const agentInfo = document.getElementById('agentInfo');
  
  if (!agentSelector || !agentInfo) return;
  
  const selectedAgentId = agentSelector.value;
  const agent = applicationData.agents.find(a => a.id === selectedAgentId);
  
  if (agent) {
    agentInfo.innerHTML = `
      <div class="info-section">
        <div class="info-label">Status</div>
        <div class="info-value">
          <span class="status ${getStatusClass(agent.status)}">${agent.status.toUpperCase()}</span>
        </div>
      </div>
      <div class="info-section">
        <div class="info-label">Last Execution</div>
        <div class="info-value">${formatDateTime(agent.lastExecution)}</div>
      </div>
      <div class="info-section">
        <div class="info-label">Next Execution</div>
        <div class="info-value">${agent.nextExecution === 'On demand' ? 'On demand' : formatDateTime(agent.nextExecution)}</div>
      </div>
      <div class="info-section">
        <div class="info-label">Success Rate</div>
        <div class="info-value">${agent.successRate}%</div>
      </div>
      <div class="info-section">
        <div class="info-label">Avg Execution Time</div>
        <div class="info-value">${agent.avgExecutionTime}s</div>
      </div>
      <div class="info-section">
        <div class="info-label">Schedule</div>
        <div class="info-value">${agent.schedule}</div>
      </div>
      <div class="info-section">
        <div class="info-label">Description</div>
        <div class="info-value">${agent.description}</div>
      </div>
    `;
  }
}

// Tasks View
function initTasksView() {
  const createTaskBtn = document.getElementById('createTaskBtn');
  const taskModal = document.getElementById('taskModal');
  const closeModal = document.getElementById('closeModal');
  const cancelTask = document.getElementById('cancelTask');
  const saveTask = document.getElementById('saveTask');
  const filterButtons = document.querySelectorAll('.filter-btn');
  
  if (createTaskBtn) {
    createTaskBtn.addEventListener('click', () => openTaskModal());
  }
  
  if (closeModal) {
    closeModal.addEventListener('click', () => closeTaskModal());
  }
  
  if (cancelTask) {
    cancelTask.addEventListener('click', () => closeTaskModal());
  }
  
  if (saveTask) {
    saveTask.addEventListener('click', () => saveTaskData());
  }
  
  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.getAttribute('data-filter');
      setTaskFilter(filter);
      
      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
    });
  });
  
  renderTasks();
}

function setTaskFilter(filter) {
  currentTaskFilter = filter;
  renderTasks();
}

function renderTasks() {
  const taskGrid = document.getElementById('taskGrid');
  if (!taskGrid) return;
  
  taskGrid.innerHTML = '';
  
  const filteredTasks = currentTaskFilter === 'all' 
    ? applicationData.tasks
    : applicationData.tasks.filter(task => task.status === currentTaskFilter);
  
  filteredTasks.forEach(task => {
    const taskCard = document.createElement('div');
    taskCard.className = 'task-card';
    taskCard.innerHTML = `
      <div class="task-header">
        <h4 class="task-title">${task.title}</h4>
        <div class="priority-badge priority-${task.priority}">${getPriorityText(task.priority)}</div>
      </div>
      <div class="task-description">${task.description}</div>
      <div class="task-meta">
        <div class="task-status">
          <span class="status ${getStatusClass(task.status)}">${task.status.replace('-', ' ').toUpperCase()}</span>
        </div>
        <div class="task-deadline">Due: ${formatDateTime(task.deadline)}</div>
      </div>
    `;
    
    taskCard.addEventListener('click', () => editTask(task));
    taskGrid.appendChild(taskCard);
  });
}

function openTaskModal(task = null) {
  const modal = document.getElementById('taskModal');
  const modalTitle = document.getElementById('modalTitle');
  const taskTitle = document.getElementById('taskTitle');
  const taskDescription = document.getElementById('taskDescription');
  const taskPriority = document.getElementById('taskPriority');
  const taskDeadline = document.getElementById('taskDeadline');
  
  if (!modal) return;
  
  currentEditingTask = task;
  
  if (task) {
    if (modalTitle) modalTitle.textContent = 'Edit Task';
    if (taskTitle) taskTitle.value = task.title;
    if (taskDescription) taskDescription.value = task.description;
    if (taskPriority) taskPriority.value = task.priority.toString();
    if (taskDeadline) {
      const deadlineDate = new Date(task.deadline);
      taskDeadline.value = deadlineDate.toISOString().slice(0, 16);
    }
  } else {
    if (modalTitle) modalTitle.textContent = 'Create New Task';
    if (taskTitle) taskTitle.value = '';
    if (taskDescription) taskDescription.value = '';
    if (taskPriority) taskPriority.value = '2';
    if (taskDeadline) taskDeadline.value = '';
  }
  
  modal.classList.remove('hidden');
}

function closeTaskModal() {
  const modal = document.getElementById('taskModal');
  if (modal) {
    modal.classList.add('hidden');
  }
  currentEditingTask = null;
}

function editTask(task) {
  openTaskModal(task);
}

function saveTaskData() {
  const taskTitle = document.getElementById('taskTitle');
  const taskDescription = document.getElementById('taskDescription');
  const taskPriority = document.getElementById('taskPriority');
  const taskDeadline = document.getElementById('taskDeadline');
  
  if (!taskTitle || !taskDescription || !taskPriority || !taskDeadline) {
    console.error('Task form elements not found');
    return;
  }
  
  const titleValue = taskTitle.value.trim();
  const descriptionValue = taskDescription.value.trim();
  const priorityValue = parseInt(taskPriority.value);
  const deadlineValue = taskDeadline.value;
  
  if (!titleValue || !deadlineValue) {
    alert('Please fill in title and deadline fields');
    return;
  }
  
  if (currentEditingTask) {
    // Edit existing task
    const taskIndex = applicationData.tasks.findIndex(t => t.id === currentEditingTask.id);
    if (taskIndex !== -1) {
      applicationData.tasks[taskIndex] = {
        ...applicationData.tasks[taskIndex],
        title: titleValue,
        description: descriptionValue,
        priority: priorityValue,
        deadline: new Date(deadlineValue).toISOString()
      };
    }
  } else {
    // Create new task
    const newTask = {
      id: `task-${Date.now()}`,
      title: titleValue,
      description: descriptionValue,
      priority: priorityValue,
      status: 'pending',
      deadline: new Date(deadlineValue).toISOString(),
      createdAt: new Date().toISOString()
    };
    applicationData.tasks.push(newTask);
  }
  
  closeTaskModal();
  renderTasks();
}

// Analytics View
function initAnalyticsView() {
  renderExecutionChart();
  renderSuccessChart();
}

function renderExecutionChart() {
  const ctx = document.getElementById('executionChart');
  if (!ctx) return;
  
  const context = ctx.getContext('2d');
  
  if (executionChart) {
    executionChart.destroy();
  }
  
  executionChart = new Chart(context, {
    type: 'line',
    data: {
      labels: applicationData.analytics.executionTimes.map(item => item.time),
      datasets: [
        {
          label: 'Collector Agent',
          data: applicationData.analytics.executionTimes.map(item => item.collector),
          borderColor: '#1FB8CD',
          backgroundColor: 'rgba(31, 184, 205, 0.1)',
          tension: 0.4
        },
        {
          label: 'Planner Agent',
          data: applicationData.analytics.executionTimes.map(item => item.planner),
          borderColor: '#FFC185',
          backgroundColor: 'rgba(255, 193, 133, 0.1)',
          tension: 0.4
        },
        {
          label: 'Executor Agent',
          data: applicationData.analytics.executionTimes.map(item => item.executor),
          borderColor: '#B4413C',
          backgroundColor: 'rgba(180, 65, 60, 0.1)',
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Execution Time (seconds)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Time of Day'
          }
        }
      },
      plugins: {
        legend: {
          position: 'top',
        }
      }
    }
  });
}

function renderSuccessChart() {
  const ctx = document.getElementById('successChart');
  if (!ctx) return;
  
  const context = ctx.getContext('2d');
  
  if (successChart) {
    successChart.destroy();
  }
  
  successChart = new Chart(context, {
    type: 'bar',
    data: {
      labels: applicationData.analytics.successRates.map(item => item.date.slice(-5)),
      datasets: [
        {
          label: 'Collector',
          data: applicationData.analytics.successRates.map(item => item.collector),
          backgroundColor: '#1FB8CD'
        },
        {
          label: 'Planner',
          data: applicationData.analytics.successRates.map(item => item.planner),
          backgroundColor: '#FFC185'
        },
        {
          label: 'Executor',
          data: applicationData.analytics.successRates.map(item => item.executor),
          backgroundColor: '#B4413C'
        },
        {
          label: 'Reviewer',
          data: applicationData.analytics.successRates.map(item => item.reviewer),
          backgroundColor: '#5D878F'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: 'Success Rate (%)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Date'
          }
        }
      },
      plugins: {
        legend: {
          position: 'top',
        }
      }
    }
  });
}

// Config View
function initConfigView() {
  // Add event listeners for configuration forms
  console.log('Config view initialized');
}

// Logs View
function initLogsView() {
  const clearLogsBtn = document.getElementById('clearLogs');
  const exportLogsBtn = document.getElementById('exportLogs');
  
  if (clearLogsBtn) {
    clearLogsBtn.addEventListener('click', clearLogs);
  }
  
  if (exportLogsBtn) {
    exportLogsBtn.addEventListener('click', exportLogs);
  }
  
  renderLogs();
}

function renderLogs() {
  const logViewer = document.getElementById('logViewer');
  if (!logViewer) return;
  
  const sampleLogs = [
    { timestamp: '2025-09-29 20:47:30', level: 'success', message: 'Executor Agent: Created 3 calendar events successfully' },
    { timestamp: '2025-09-29 20:46:15', level: 'info', message: 'Planner Agent: Starting conflict resolution algorithm' },
    { timestamp: '2025-09-29 20:46:10', level: 'info', message: 'Planner Agent: Detected 2 scheduling conflicts' },
    { timestamp: '2025-09-29 20:45:00', level: 'success', message: 'Collector Agent: Data collection completed - 15 events processed' },
    { timestamp: '2025-09-29 20:44:58', level: 'info', message: 'Collector Agent: Fetching weather data from OpenWeatherMap' },
    { timestamp: '2025-09-29 20:44:55', level: 'info', message: 'Collector Agent: Reading tasks from Notion database' },
    { timestamp: '2025-09-29 20:30:12', level: 'info', message: 'Collector Agent: Weather data updated - Rain expected tomorrow' },
    { timestamp: '2025-09-29 20:15:00', level: 'success', message: 'Collector Agent: Scheduled execution completed' },
    { timestamp: '2025-09-29 20:00:05', level: 'error', message: 'Planner Agent: API rate limit exceeded, retrying in 60 seconds' },
    { timestamp: '2025-09-29 20:00:00', level: 'success', message: 'System: All agents healthy, uptime 15d 7h 23m' }
  ];
  
  logViewer.innerHTML = '';
  
  sampleLogs.forEach(log => {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.innerHTML = `
      <span class="log-timestamp">${log.timestamp}</span>
      <span class="log-level ${log.level}">${log.level.toUpperCase()}</span>
      <span class="log-message">${log.message}</span>
    `;
    logViewer.appendChild(logEntry);
  });
}

function clearLogs() {
  const logViewer = document.getElementById('logViewer');
  if (logViewer) {
    logViewer.innerHTML = '<div class="log-entry"><span class="log-message">Logs cleared</span></div>';
  }
}

function exportLogs() {
  alert('Logs exported to logs_export.txt');
}

// Real-time updates simulation
function startRealTimeUpdates() {
  setInterval(() => {
    // Update uptime
    const uptimeElement = document.getElementById('uptime');
    if (uptimeElement) {
      // This is a simple simulation - in real app, calculate from actual start time
      const parts = uptimeElement.textContent.split(' ');
      let minutes = parseInt(parts[4]);
      minutes++;
      if (minutes >= 60) {
        minutes = 0;
        let hours = parseInt(parts[2]);
        hours++;
        if (hours >= 24) {
          hours = 0;
          let days = parseInt(parts[0]);
          days++;
          parts[0] = days;
        }
        parts[2] = hours;
      }
      parts[4] = minutes;
      uptimeElement.textContent = parts.join(' ');
    }
  }, 60000); // Update every minute
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initNavigation();
  switchView('overview');
  startRealTimeUpdates();
  
  // Handle clicks outside modal
  document.addEventListener('click', (e) => {
    const modal = document.getElementById('taskModal');
    if (e.target === modal) {
      closeTaskModal();
    }
  });
});