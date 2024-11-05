import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token");

  if (!token) {
    // Chuyển hướng về trang login nếu token không tồn tại
    return <Navigate to="/login" />;
  }

  return children;
};

export default ProtectedRoute;
