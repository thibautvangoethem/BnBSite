import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router';
import SideBar from './SideBar';
import Login from './Login';
import { AuthProvider } from './AuthContext';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import CasinoOutlinedIcon from '@mui/icons-material/CasinoOutlined';
import FaceUnlockOutlinedIcon from '@mui/icons-material/FaceUnlockOutlined';

const menuItems = [
  { text: 'Home', route: '/', icon: <InboxIcon /> },
  { text: 'Login', route: '/Login', icon: <FaceUnlockOutlinedIcon /> },
  { text: 'Rolling', route: '/rolling', icon: <CasinoOutlinedIcon/> },
];

const Home = () => <h2>Home Page</h2>;
// const Login = () => <><h2>Login Page</h2><Login/></>;
const Rolling = () => <h2>Rolling in the deep</h2>;

function App() {
  return (
    <AuthProvider>
    <Router>
      <div style={{ display: 'flex' }}>
        <SideBar items={menuItems} />
        <div style={{ padding: '20px', width: '100%' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/rolling" element={<Rolling />} />
          </Routes>
        </div>
      </div>
    </Router>
    </AuthProvider>
  );
}

export default App;
