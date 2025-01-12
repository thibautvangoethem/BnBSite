export const api = async (endpoint, options = {}) => {
    const token = localStorage.getItem('bearerToken'); // Get the token from localStorage
  
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers, // Merge with any custom headers
    };
  
    if (token) {
      headers['Authorization'] = `Bearer ${token}`; // Add the token
    }
  
    const config = {
      ...options,
      headers,
    };
  
    try {
      const response = await fetch(endpoint, config);
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Something went wrong!');
      }
  
      return await response.json();
    } catch (err) {
      console.error('API Error:', err.message);
      throw err; // Re-throw the error for further handling
    }
  };