// API Integration for TaskSaathi
const API_BASE_URL = 'http://localhost:8000/api';
const AUTH_URL = 'http://localhost:8000';

// Authentication functions
async function login(email, password) {
    try {
        console.log('=== LOGIN ATTEMPT ===');
        console.log('Email:', email);
        
        const response = await fetch(`${AUTH_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        
        const responseData = await response.json();
        console.log('=== LOGIN RESPONSE ===');
        console.log('Full response:', responseData);
        
        // Handle wrapped response (data.data) or direct response (data)
        const data = responseData.data || responseData;
        console.log('Extracted data:', data);
        console.log('Access token:', data.access);
        console.log('User data:', data.user);
        
        if (response.ok) {
            // Store tokens
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            localStorage.setItem('loggedIn', 'true');
            
            console.log('=== STORING IN LOCALSTORAGE ===');
            console.log('access_token being stored:', data.access);
            console.log('After storing, localStorage.access_token =', localStorage.getItem('access_token'));
            
            // Store user data if available
            if (data.user) {
                localStorage.setItem('user', JSON.stringify(data.user));
                localStorage.setItem('user_id', data.user.id);
                localStorage.setItem('user_role', data.user.userRole);
                console.log('Stored user role:', data.user.userRole);
                console.log('After storing, localStorage.user_role =', localStorage.getItem('user_role'));
            } else {
                console.warn('No user data in login response. Full response:', responseData);
            }
            
            console.log('=== ALL LOCALSTORAGE ===');
            console.log(localStorage);
            
            return { success: true, data };
        } else {
            const errorData = responseData.error || responseData;
            return { success: false, error: errorData.detail || errorData.non_field_errors?.[0] || 'Login failed' };
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
            return { success: true, data };
        } else {
            // Extract error message
            let errorMsg = 'Registration failed';
            if (data.email) errorMsg = data.email[0];
            else if (data.detail) errorMsg = data.detail;
            else if (data.non_field_errors) errorMsg = data.non_field_errors[0];
            return { success: false, error: errorMsg };
        }
    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, error: 'Network error' };
    }
}

// Task management functions
async function getTasks() {
    try {
        const token = localStorage.getItem('access_token');
        console.log('=== getTasks API CALL ===');
        console.log('Token from localStorage:', token);
        console.log('Full Authorization header:', `Bearer ${token}`);
        
        const response = await fetch(`${API_BASE_URL}/tasks/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        
        if (response.ok) {
            return { success: true, data: data.results || data };
        } else {
            return { success: false, error: data.detail || 'Failed to fetch tasks' };
        }
    } catch (error) {
        console.error('Get tasks error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function getMyTasks() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/tasks/my-tasks/`, {
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
        console.error('Get my tasks error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function getCompanyTasks() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/tasks/company-tasks/`, {
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
            return { success: false, error: data.detail || 'Failed to fetch company tasks' };
        }
    } catch (error) {
        console.error('Get company tasks error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function createTask(taskData) {
    try {
        const token = localStorage.getItem('access_token');
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
            let errorMsg = 'Failed to create task';
            if (data.detail) errorMsg = data.detail;
            else if (typeof data === 'object') errorMsg = JSON.stringify(data);
            return { success: false, error: errorMsg };
        }
    } catch (error) {
        console.error('Create task error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function updateTask(taskId, taskData) {
    try {
        const token = localStorage.getItem('access_token');
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

async function updateTaskStatus(taskId, status) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/update-status/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status }),
        });
        
        const data = await response.json();
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data.detail || data.message || 'Failed to update task status' };
        }
    } catch (error) {
        console.error('Update task status error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function deleteTask(taskId) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok || response.status === 204) {
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
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/companies/my-company/`, {
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
            return { success: false, error: data.detail || data.message || 'Failed to fetch company details' };
        }
    } catch (error) {
        console.error('Get company details error:', error);
        return { success: false, error: 'Network error' };
    }
}

// Get all users (employees) in company
async function getCompanyEmployees() {
    try {
        const token = localStorage.getItem('access_token');
        const user = JSON.parse(localStorage.getItem('user'));
        
        if (!user || !user.company) {
            return { success: false, error: 'No company found' };
        }
        
        const response = await fetch(`${AUTH_URL}/users/?userRole=EMPLOYEE`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });
        
        const data = await response.json();
        if (response.ok) {
            return { success: true, data: data.results || data };
        } else {
            return { success: false, error: data.detail || 'Failed to fetch employees' };
        }
    } catch (error) {
        console.error('Get employees error:', error);
        return { success: false, error: 'Network error' };
    }
}

// Utility functions
function getAuthToken() {
    return localStorage.getItem('access_token');
}

function isAuthenticated() {
    return !!localStorage.getItem('access_token') && !!localStorage.getItem('loggedIn');
}

function getUserData() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function getUserRole() {
    return localStorage.getItem('user_role');
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user');
    localStorage.removeItem('user_role');
    localStorage.removeItem('loggedIn');
    window.location.href = 'login.html';
}