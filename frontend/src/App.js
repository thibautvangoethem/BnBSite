import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router';
import SideBar from './SideBar';
import Login from './Login';
import { AuthProvider } from './AuthContext';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import CasinoOutlinedIcon from '@mui/icons-material/CasinoOutlined';
import FaceUnlockOutlinedIcon from '@mui/icons-material/FaceUnlockOutlined';
import CustomRollingInputs from './CustomRollingInputs';
import DiceRollsPopup from './DiceRollsPopup';

const menuItems = [
  { text: 'Home', route: '/', icon: <InboxIcon /> },
  { text: 'Login', route: '/login', icon: <FaceUnlockOutlinedIcon /> },
  { text: 'Rolling', route: '/rolling', icon: <CasinoOutlinedIcon /> },
];

const Home = () => <h2>Home Page</h2>;

const App = () => {
  const [rollsConfig, setRollsConfig] = useState(null);
  const [open, setOpen] = useState(false);

  const handleSerialize = (config) => {
    setRollsConfig(config);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <AuthProvider>
      <Router>
        <div style={{ display: 'flex' }}>
          <SideBar items={menuItems} />
          <div style={{ padding: '20px', width: '100%' }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route
                path="/rolling"
                element={<CustomRollingInputs onSerialize={handleSerialize} />}
              />
            </Routes>
          </div>
        </div>
        <DiceRollsPopup open={open} onClose={handleClose} rollsConfig={rollsConfig} />
      </Router>
    </AuthProvider>
  );
};

export default App;
