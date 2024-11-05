// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
// import './App.css';

// // Import các component của bạn
// import Chatbot from "./components/Chatbot.tsx";
// import Upload from './components/Upload.js';
// import Delete from './components/Delete.js';
// import View from './components/View.js';
// import AppRoutes from './routes/AppRoutes.js';


// // Trang Admin Dashboard
// function AdminDashboard() {
//   return (
//     <div>
//       <h1>Admin Dashboard</h1>
//       <Upload />
//       <Delete />
//       <View/>
//     </div>
//   );
// }

// // Trang Chatbot
// function ChatbotPage() {
//   return (
//     <div>
//       <h1>VJU Chatbot</h1>
//       <Chatbot />
//     </div>
//   );
// }

// function App() {
//   return (
//     <Router>
//       <nav>
//         {/* Tạo các liên kết để điều hướng giữa các trang */}
//         <ul>
//           <li>
//             <Link to="/chatbot">Chatbot</Link>
//           </li>
//           <li>
//             <Link to="/admin">Admin Dashboard</Link>
//           </li>
//         </ul>
//       </nav>
//       <AppRoutes/>
//       <Routes>
//         <Route path="/" element={<ChatbotPage />} />
//         <Route path="/Chatbot" element={<ChatbotPage />} />
//       </Routes>
      
//     </Router>
//   );
// }

// export default App;

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Import các component của bạn
import Chatbot from "./components/Chatbot.tsx";
import MiniChatbot from './components/MiniChatbot.tsx';
import Upload from './components/Upload.js';
import Delete from './components/Delete.js';
import View from './components/View.js';
import Login from './components/Login.js';
import AdminManage from './components/AdminManage.js';
import ProtectedRoute from './components/ProtectedRoute';  // Import ProtectedRoute

function ChatbotPage() {
  return (
    <div>
      <Chatbot/>
    </div>
  );
}

function HomePage() {
  const [isChatVisible, setChatVisible] = useState(false);

  const handleToggleChat = () => {
    setChatVisible(!isChatVisible);
  };

  const handleCloseChat = () => {
    setChatVisible(false);
  };

  return (
    <div>
      <h1>Welcome to VJU Chatbot Application</h1>
      <p>This is the homepage of the chatbot application.</p>

      {/* Nút "+" ở góc dưới bên phải */}
      <button
        style={styles.floatingButton}
        onClick={handleToggleChat}
      >
        {isChatVisible ? '-' : '+'}
      </button>

      {/* Hiển thị hoặc ẩn Chatbot */}
      {isChatVisible && (
        <div>
          <button style={styles.closeButton} onClick={handleCloseChat}>×</button>
          <MiniChatbot />
        </div>
      )}
    </div>
  );
}



function App() {
  return (
    <Router>
      {/* Navigation Bar */}
      <nav style={styles.navbar}>
        <ul style={styles.navList}>
          <div style={styles.leftNav}>
            <li style={styles.navItem}>
              <Link to="/" style={styles.navLink}>Home</Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/chatbot" style={styles.navLink}>Chatbot</Link>
            </li>
          </div>
          <div style={styles.rightNav}>
            <li style={styles.navItem}>
              <Link to="/login" style={styles.navLink}>Login</Link>
            </li>
          </div>
        </ul>
      </nav>

      {/* Định tuyến các trang */}
      <Routes>
        <Route path="/" element={<HomePage />} />        {/* Trang Home */}
        <Route path="/chatbot" element={<ChatbotPage />} />  {/* Trang Chatbot */}
        <Route path="/login" element={<Login />} /> 
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <AdminManage />
            </ProtectedRoute>
          }
        />  {/* Trang quản lý Admin với bảo vệ */}
      </Routes>
    </Router>
  );
}

// Các styles đơn giản cho Navigation Bar và Floating Button
const styles = {
  navbar: {
    backgroundColor: "#333", // Màu xám đậm cho thanh nav
    padding: "10px",
    display: "flex",
    justifyContent: "space-between", // Đặt khoảng cách giữa hai nhóm item
    alignItems: "center",
  },
  navList: {
    listStyleType: "none",
    display: "flex",
    width: "100%", // Đảm bảo sử dụng toàn bộ chiều rộng
    margin: 0,
    padding: 0,
    justifyContent: "space-between", // Đặt không gian giữa các phần bên trái và phải
  },
  leftNav: {
    display: "flex",
  },
  rightNav: {
    display: "flex",
    justifyContent: "flex-end",
  },
  navItem: {
    margin: "0 15px",
  },
  navLink: {
    color: "white", // Màu chữ trắng
    textDecoration: "none",
    fontSize: "18px",
    fontWeight: "bold",
    transition: "color 0.3s", // Thêm hiệu ứng chuyển đổi màu
  },
  floatingButton: {
    position: "fixed",
    bottom: "30px",
    right: "30px",
    backgroundColor: "#ffcc00",
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    border: "none",
    fontSize: "24px",
    cursor: "pointer",
    zIndex: 1001, // Ensure button stays on top
  },
};

export default App;

// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
// import './App.css';

// // Import các component của bạn
// import Chatbot from "./components/Chatbot.tsx";
// import Upload from './components/Upload.js';
// import Delete from './components/Delete.js';
// import View from './components/View.js';
// import AppRoutes from './routes/AppRoutes.js';
// import Login from './components/Login.js';

// // Trang Admin Dashboard (Login)
// function AdminDashboard() {
//   return (
//     <div>
//       <h1>Admin Dashboard</h1>
//       <Upload />
//       <Delete />
//       <View />
//     </div>
//   );
// }

// // Trang Chatbot
// function ChatbotPage() {
//   return (
//     <div>
//       <h1>VJU Chatbot</h1>
//       <Chatbot />
//     </div>
//   );
// }

// // Trang Home
// function HomePage() {
//   return (
//     <div>
//       <h1>Welcome to VJU Chatbot Application</h1>
//       <p>This is the homepage of the chatbot application.</p>
//     </div>
//   );
// }

// // Component chính App
// function App() {
//   return (
//     <Router>
//       {/* Navigation Bar */}
//       <nav style={styles.navbar}>
//         <ul style={styles.navList}>
//           <div style={styles.leftNav}>
//             <li style={styles.navItem}>
//               <Link to="/" style={styles.navLink}>Home</Link>
//             </li>
//             <li style={styles.navItem}>
//               <Link to="/chatbot" style={styles.navLink}>Chatbot</Link>
//             </li>
//           </div>
//           <div style={styles.rightNav}>
//             <li style={styles.navItem}>
//               <Link to="/login" style={styles.navLink}>Login</Link>
//             </li>
//           </div>
//         </ul>
//       </nav>

//       {/* Định tuyến các trang */}
//       <Routes>
//         <Route path="/" element={<HomePage />} />        {/* Trang Home */}
//         <Route path="/chatbot" element={<ChatbotPage />} />  {/* Trang Chatbot */}
//         <Route path="/login" element={<Login />} /> {/* Trang Admin (Login) */}
//       </Routes>
//     </Router>
//   );
// }

// // Các styles đơn giản cho Navigation Bar
// const styles = {
//   navbar: {
//     backgroundColor: "#333", // Màu xám đậm cho thanh nav
//     padding: "10px",
//     display: "flex",
//     justifyContent: "space-between", // Đặt khoảng cách giữa hai nhóm item
//     alignItems: "center",
//   },
//   navList: {
//     listStyleType: "none",
//     display: "flex",
//     width: "100%", // Đảm bảo sử dụng toàn bộ chiều rộng
//     margin: 0,
//     padding: 0,
//     justifyContent: "space-between", // Đặt không gian giữa các phần bên trái và phải
//   },
//   leftNav: {
//     display: "flex",
//   },
//   rightNav: {
//     display: "flex",
//     justifyContent: "flex-end",
//   },
//   navItem: {
//     margin: "0 15px",
//   },
//   navLink: {
//     color: "white", // Màu chữ trắng
//     textDecoration: "none",
//     fontSize: "18px",
//     fontWeight: "bold",
//     transition: "color 0.3s", // Thêm hiệu ứng chuyển đổi màu
//   },
//   navLinkHover: {
//     color: "#ffcc00", // Màu vàng khi hover
//   },
// };

// export default App;


