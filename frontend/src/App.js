import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router';
import SideBar from './SideBar';
import Login from './subComponents/login/Login';
import { AuthProvider } from './subComponents/login/AuthContext';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import CasinoOutlinedIcon from '@mui/icons-material/CasinoOutlined';
import FaceUnlockOutlinedIcon from '@mui/icons-material/FaceUnlockOutlined';
import CustomRollingInputs from './subComponents/customRolling/CustomRollingInputs'; //dat geeft nen error hier op dat iets in folder "CustomRolling"  (grote C) all included is, maar dat bestaat niet??
import QuickLootMenu from './subComponents/quickLoot/QuickLootMenu';
import GunRoll from './subComponents/quickLoot/gun/GunRoll';
import HomePage from './subComponents/homePage/HomePage';
import CottageIcon from '@mui/icons-material/Cottage';
import AutoModeIcon from '@mui/icons-material/AutoMode';
import DiceRollsPopup from './rolling/DiceRollsPopup';
import { v4 as uuidv4 } from 'uuid';

const menuItems = [
  { text: 'Home', route: '/', icon: <CottageIcon /> },
  { text: 'Login', route: '/login', icon: <FaceUnlockOutlinedIcon /> },
  { text: 'Free Rolling', route: '/rolling', icon: <CasinoOutlinedIcon /> },
  { text: 'Quick Loot', route: '/quickloot', icon: <AutoModeIcon /> },
];

const App = () => {
  const [rollModal, setRollModal] = useState(null);
  const [open, setOpen] = useState(false);

  const handleSerialize = (config) => {
    console.log("serialize");
    setRollModal(config);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleRerollAll = () => {
    console.log("Rerolling all dice...");

    // Create a new rollsConfig object to ensure a re-render
    const newRollModal = { ...rollModal };
    newRollModal.rolls.uuid = uuidv4();

    setRollModal({ ...newRollModal });
  };
  return (
    <AuthProvider>
      <Router>
        <div style={{ display: 'flex' }}>
          <SideBar items={menuItems} />
          <div style={{ padding: '20px', width: '100%' }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<Login />} />
              <Route
                path="/rolling"
                element={<CustomRollingInputs onSerialize={handleSerialize} />}
              />
              <Route path="/quickloot" element={<QuickLootMenu onSerialize={handleSerialize} />} />
              <Route path="/quickloot/gun" element={<GunRoll />} />
              {/* <Route path="/quickloot/shield" element={<CardPage2 />} />
              <Route path="/quickloot/classmod" element={<CardPage3 />} />
              <Route path="/quickloot/grenade" element={<CardPage3 />} />
              <Route path="/quickloot/potion" element={<CardPage3 />} />  */}
            </Routes>
          </div>
        </div>
        {rollModal !== null && (
          <DiceRollsPopup
            open={open}
            onClose={handleClose}
            rollsModal={rollModal}
            onRerollAll={handleRerollAll}
          />
        )}
      </Router>
    </AuthProvider>
  );
};

export default App;
