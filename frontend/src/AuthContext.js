import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [bearerToken, setBearerToken] = useState(null);

  return (
    <AuthContext.Provider value={{ bearerToken, setBearerToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
