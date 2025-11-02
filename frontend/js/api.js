// API Integration for TaskSaathi
const API_BASE_URL = 'http://localhost:8000';
const AUTH_URL = 'http://localhost:8000';

// Authentication functions
async function login(email, password) {
    try {
        const response = await fetch(`${AUTH_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('user_id', data.user_id);
            localStorage.setItem('loggedIn', 'true');
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || 'Login failed' };
        }
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function register(userData) {
    try {
        const response = await fetch(`${AUTH_URL}/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });
        
        const data = await response.json();
        if (response.ok) {
            // Automatically log in the user after successful registration
            const loginResult = await login(userData.email, userData.password);
            if (loginResult.success) {
                return { success: true, data: loginResult.data };
            } else {
                return { success: true, data, message: 'Registration successful. Please log in.' };
            }
        } else {
            const errorMessage = data.email ? 
                `Email error: ${data.email}` : 
                data.detail || data.non_field_errors || 'Registration failed';
            return { success: false, error: errorMessage };
        }
    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, error: 'Network error' };
    }
}

// Task management functions
async function getTasks() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/tasks/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        
        const data = await response.json();
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || 'Failed to fetch tasks' };
        }
    } catch (error) {
        console.error('Get tasks error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function createTask(taskData) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/tasks/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });
        
        const data = await response.json();
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || 'Failed to create task' };
        }
    } catch (error) {
        console.error('Create task error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function updateTask(taskId, taskData) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });
        
        const data = await response.json();
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || 'Failed to update task' };
        }
    } catch (error) {
        console.error('Update task error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function deleteTask(taskId) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            return { success: true };
        } else {
            const data = await response.json();
            return { success: false, error: data.detail || 'Failed to delete task' };
        }
    } catch (error) {
        console.error('Delete task error:', error);
        return { success: false, error: 'Network error' };
    }
}

// Company management functions
async function getCompanyDetails() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/companies/my_company/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        
        const data = await response.json();
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || 'Failed to fetch company details' };
        }
    } catch (error) {
        console.error('Get company details error:', error);
        return { success: false, error: 'Network error' };
    }
}

// Utility functions
function getAuthToken() {
    return localStorage.getItem('token');
}

function isAuthenticated() {
    return !!localStorage.getItem('token');
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
    window.location.href = 'login.html';
}