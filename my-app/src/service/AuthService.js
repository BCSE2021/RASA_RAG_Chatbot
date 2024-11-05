export const AuthService = {
    login: async (username, password) => {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });
  
      if (response.ok) {
        const data = await response.json();
        // Lưu token vào localStorage
        localStorage.setItem("token", data.token);
        return true;
      } else {
        return false;
      }
    },
  
    getToken: () => {
      return localStorage.getItem("token");
    },
  
    isAuthenticated: () => {
      // Kiểm tra xem có token không
      return !!localStorage.getItem("token");
    },
  
    logout: () => {
      // Xóa token
      localStorage.removeItem("token");
    },
  };