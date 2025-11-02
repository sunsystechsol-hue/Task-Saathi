// Mock authentication for testing
function generateMockToken() {
    // Create a mock JWT token structure (for testing only)
    const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
    const payload = btoa(JSON.stringify({
        user_id: 1,
        email: 'test@example.com',
        exp: Math.floor(Date.now() / 1000) + (60 * 60 * 24), // 24 hours
        iat: Math.floor(Date.now() / 1000)
    }));
    const signature = btoa('mock_signature');
    
    return `${header}.${payload}.${signature}`;
}

// Generate and set mock tokens
function setupMockAuth() {
    const token = generateMockToken();
    const refreshToken = generateMockToken();
    
    localStorage.setItem('token', token);
    localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('user_id', '1');
    localStorage.setItem('loggedIn', 'true');
    
    console.log('Mock authentication set up successfully');
    console.log('Access Token:', token);
    console.log('User ID:', 1);
    
    return {
        token,
        refresh_token: refreshToken,
        user_id: 1
    };
}

// Call this function in the browser console to set up mock authentication:
// setupMockAuth();