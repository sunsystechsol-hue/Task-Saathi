// 🎯 COPY-PASTE TOKENS FOR BROWSER CONSOLE (F12)
// These tokens are pre-generated and ready to use for testing

// ============================================================================
// 👨‍💼 EMPLOYER ACCOUNT - Copy & Paste into Console (F12 → Console tab)
// ============================================================================
// Email: employer@test.com
// Password: testpass123
// Role: EMPLOYER

localStorage.setItem('access_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyMTc3MTU3LCJpYXQiOjE3NjIwOTA3NTcsImp0aSI6Ijc2OGNjZGU4YjJmNTQwODc4MzhiNmNkNjI3ZGFkNzBkIiwidXNlcl9pZCI6ImJlZTMwNjA2LTI4MjctNDQwMS05MThiLTI1MTk5ZWZmMTM5MCJ9.p3S6IWqzw0StWinkzZ9jcbL2Xv0Q7oWdyRSowaoKGvM');
localStorage.setItem('user_role', 'EMPLOYER');
localStorage.setItem('loggedIn', 'true');
localStorage.setItem('user', JSON.stringify({"id": "bee30606-2827-4401-918b-25199eff1390", "email": "employer@test.com", "firstName": "John", "lastName": "Employer", "userRole": "EMPLOYER", "company": {"id": "employer-company-id", "name": "Test Company Ltd."}}));
// Then refresh the page (F5) and you'll be logged in as EMPLOYER

// ============================================================================
// 👩‍💻 EMPLOYEE ACCOUNT - Copy & Paste into Console (F12 → Console tab)
// ============================================================================
// Email: employee@test.com
// Password: testpass123
// Role: EMPLOYEE

localStorage.setItem('access_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyMTc3MTU3LCJpYXQiOjE3NjIwOTA3NTcsImp0aSI6ImQ2ZmJiNDgzNDIyOTRmYTBiZjAyZThjOGNhNDEwODRmIiwidXNlcl9pZCI6ImI4NGYyZTRlLThkYzItNDIwNC05Yzk5LWIzNTUyMTkwOWY2MiJ9.3_Z5ZyqwUpusJO8Kp6yhmXRAh_6iGUd4KVEjsgDEAe4');
localStorage.setItem('user_role', 'EMPLOYEE');
localStorage.setItem('loggedIn', 'true');
localStorage.setItem('user', JSON.stringify({"id": "b84f2e4e-8dc2-4204-9c99-b35521909f62", "email": "employee@test.com", "firstName": "Jane", "lastName": "Employee", "userRole": "EMPLOYEE"}));
// Then refresh the page (F5) and you'll be logged in as EMPLOYEE

// ============================================================================
// TEST THESE API CALLS IN CONSOLE (after logging in)
// ============================================================================

// Get user data
// console.log(getUserData());

// Check if authenticated
// console.log(isAuthenticated());

// Get all tasks
// getTasks().then(r => console.log(r));

// Get tasks assigned to current user (EMPLOYEE only)
// getMyTasks().then(r => console.log(r));

// Get company tasks (EMPLOYER only)
// getCompanyTasks().then(r => console.log(r));

// Get company details (EMPLOYER only)
// getCompanyDetails().then(r => console.log(r));

// Get company employees (EMPLOYER only)
// getCompanyEmployees().then(r => console.log(r));

// Create a task (EMPLOYER only)
// const taskData = {
//   title: "New Test Task",
//   description: "This is a test task",
//   assignedTo: "employee-id-here",
//   createdBy: "your-user-id",
//   companyId: "your-company-id",
//   dueDate: "2025-11-10",
//   priority: "high",
//   status: "pending"
// };
// createTask(taskData).then(r => console.log(r));

// Update task status
// updateTaskStatus("task-id-here", "completed").then(r => console.log(r));

// Logout
// logout();

// ============================================================================
// ENDPOINTS TO TEST
// ============================================================================

// POST http://localhost:8000/register/ - Register new user
// POST http://localhost:8000/login/ - Login user
// GET  http://localhost:8000/api/tasks/ - List all tasks
// GET  http://localhost:8000/api/tasks/my-tasks/ - Get tasks assigned to user
// GET  http://localhost:8000/api/tasks/company-tasks/ - Get company tasks
// POST http://localhost:8000/api/tasks/ - Create new task
// PATCH http://localhost:8000/api/tasks/{id}/ - Update task
// PATCH http://localhost:8000/api/tasks/{id}/update-status/ - Update task status
// DELETE http://localhost:8000/api/tasks/{id}/ - Delete task
// GET  http://localhost:8000/api/companies/my-company/ - Get company details
// GET  http://localhost:8000/users/ - List users

// ============================================================================
// API DOCUMENTATION
// ============================================================================
// Swagger UI: http://localhost:8000/swagger/
// ReDoc: http://localhost:8000/redoc/
