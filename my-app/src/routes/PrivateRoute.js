import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthService } from '../service/AuthService';

const PrivateRoute = ({ redirectPath = '/login' }) => {
  const isAuthenticated = AuthService.isAuthenticated();
  
  return isAuthenticated ? <Outlet /> : <Navigate to={redirectPath} />;
};

export default PrivateRoute;