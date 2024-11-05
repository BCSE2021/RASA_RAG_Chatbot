import React, { useEffect } from 'react';
import { AuthService } from '../service/AuthService';
import { useNavigate } from 'react-router-dom';
import Upload from './Upload';
import Delete from './Delete';
import View from './View';

const AdminManage = () => {
  const navigate = useNavigate();
  let timeoutId;

  const handleLogout = () => {
    AuthService.logout();
    navigate('/login');
  };

  const startAutoLogoutTimer = () => {
    timeoutId = setTimeout(() => {
      handleLogout();
    }, 60000); // Auto-logout after 30 seconds
  };

  useEffect(() => {
    // Check if the user is logged in (i.e., check for token)
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login'); // Redirect to login if no token
    }

    startAutoLogoutTimer();

    const handleUserActivity = () => {
      clearTimeout(timeoutId);
      startAutoLogoutTimer();
    };

    const handleBeforeUnload = () => {
      handleLogout(); 
    };

    window.addEventListener('mousemove', handleUserActivity);
    window.addEventListener('keydown', handleUserActivity);
    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('mousemove', handleUserActivity);
      window.removeEventListener('keydown', handleUserActivity);
      window.removeEventListener('beforeunload', handleBeforeUnload);
      clearTimeout(timeoutId);
    };
  }, [navigate]);

  return (
    <div>
      <h1>Admin Management Page</h1>
      <button onClick={handleLogout}>Logout</button>
      <div>
        <h2>File Management</h2>
        <Upload />
        <Delete />
        <View />
      </div>
    </div>
  );
};

export default AdminManage;
