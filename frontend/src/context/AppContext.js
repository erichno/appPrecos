import React, { createContext, useState, useContext, useEffect } from 'react';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [selectedCity, setSelectedCity] = useState(() => {
    const saved = localStorage.getItem('selectedCity');
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (selectedCity) {
      localStorage.setItem('selectedCity', JSON.stringify(selectedCity));
    }
  }, [selectedCity]);

  return (
    <AppContext.Provider value={{ selectedCity, setSelectedCity }}>
      {children}
    </AppContext.Provider>
  );
};
