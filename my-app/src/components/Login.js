import React, { useState } from 'react';
import './Login.css';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../service/AuthService';
import axios from 'axios';
const Login = () => {
  const navigate = useNavigate();
  const [adminName, setAdminName] = useState("");
  const [password, setPassword] = useState("");

  // Hàm xử lý đăng nhập
  const handleLogin = async () => {
    if (!adminName || !password) {
      toast.error("Name/Password is required");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: adminName,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        toast.success("Login successful!");
        console.log("Login successful!");

        localStorage.setItem("token", data.token);
        console.log('Login successful, token:', data.token);
        // Chuyển hướng đến trang admin
        navigate('/admin');
      } else {
        toast.error("Invalid admin name or password");
      }
    } catch (error) {
      console.error("Error during login:", error);
      toast.error("An error occurred. Please try again.");
    }
  };

  return (
    <div className="login-container col-12 col-sm-4">
      <div className="title">
        <h2>Log in</h2>
      </div>
      <div className="text">Admin Name</div>
      <input
        type="text"
        placeholder="Admin Name"
        value={adminName}
        onChange={(event) => setAdminName(event.target.value)}
      />
      <div>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
      </div>
      <button
        className={adminName && password ? "active" : ""}
        disabled={!adminName || !password}
        onClick={handleLogin}
      >
        Login
      </button>
    </div>
  );
};

export default Login;
