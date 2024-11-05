// import React, { useState, useEffect } from "react";
// import axios from "axios";

// const Chatbot: React.FC = () => {
//   const [messages, setMessages] = useState<any[]>([]);
//   const [input, setInput] = useState<string>("");

//   const sendMessage = async () => {
//     if (input.trim() === "") return;

//     // Add user's message to the conversation
//     const newMessages = [...messages, { sender: "user", text: input }];
//     setMessages(newMessages);

//     try {
//       // Gửi tin nhắn tới Rasa server thông qua API
//       const response = await axios.post("http://localhost:5005/webhooks/rest/webhook", {
//         sender: "user",  // ID của người dùng, bạn có thể thay đổi nếu cần
//         message: input,
//       });

//       // Thêm phản hồi từ bot vào cuộc hội thoại
//       const botMessages = response.data.map((message: any) => ({
//         sender: "bot",
//         text: message.text,
//       }));

//       setMessages([...newMessages, ...botMessages]);
//     } catch (error) {
//       console.error("Error sending message to Rasa:", error);
//     }

//     // Clear input field
//     setInput("");
//   };

//   // Xử lý gửi tin nhắn khi người dùng nhấn Enter
//   const handleKeyDown = (event: React.KeyboardEvent) => {
//     if (event.key === "Enter") {
//       sendMessage();
//     }
//   };

//   return (
//     <div style={styles.container}>
//       <div style={styles.chatWindow}>
//         {messages.map((message, index) => (
//           <div key={index} style={message.sender === "user" ? styles.userMessage : styles.botMessage}>
//             {message.text}
//           </div>
//         ))}
//       </div>
//       <div style={styles.inputContainer}>
//         <input
//           type="text"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           onKeyDown={handleKeyDown}
//           placeholder="Nhập tin nhắn..."
//           style={styles.input}
//         />
//         <button onClick={sendMessage} style={styles.button}>Gửi</button>
//       </div>
//     </div>
//   );
// };

// const styles = {
//   container: {
//     display: "flex",
//     flexDirection: "column" as const,
//     height: "500px",
//     width: "400px",
//     border: "1px solid #ccc",
//     borderRadius: "8px",
//   },
//   chatWindow: {
//     flex: 1,
//     padding: "10px",
//     overflowY: "scroll" as const,
//   },
//   inputContainer: {
//     display: "flex",
//     padding: "10px",
//     borderTop: "1px solid #ccc",
//   },
//   input: {
//     flex: 1,
//     padding: "10px",
//     borderRadius: "4px",
//     border: "1px solid #ccc",
//   },
//   button: {
//     marginLeft: "10px",
//     padding: "10px 20px",
//     borderRadius: "4px",
//     border: "none",
//     backgroundColor: "#007bff",
//     color: "white",
//     cursor: "pointer",
//   },
//   userMessage: {
//     textAlign: "right" as const,
//     margin: "5px 0",
//     backgroundColor: "#007bff",
//     color: "white",
//     padding: "10px",
//     borderRadius: "10px",
//   },
//   botMessage: {
//     textAlign: "left" as const,
//     margin: "5px 0",
//     backgroundColor: "#f1f1f1",
//     padding: "10px",
//     borderRadius: "10px",
//   },
// };

import React, { useState } from "react";
import axios from "axios";

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState<string>("");

  const sendMessage = async () => {
    if (input.trim() === "") return;

    // Add user's message to the conversation
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);

    try {
      // Gửi tin nhắn tới Rasa server thông qua API
      const response = await axios.post("http://localhost:5005/webhooks/rest/webhook", {
        sender: "user", // ID của người dùng, bạn có thể thay đổi nếu cần
        message: input,
      });

      // Thêm phản hồi từ bot vào cuộc hội thoại
      const botMessages = response.data.map((message: any) => ({
        sender: "bot",
        text: message.text,
      }));

      setMessages([...newMessages, ...botMessages]);
    } catch (error) {
      console.error("Error sending message to Rasa:", error);
    }

    // Clear input field
    setInput("");
  };

  // Xử lý gửi tin nhắn khi người dùng nhấn Enter
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div style={styles.wrapper}>
      {/* Main Chat Window */}
      <div style={styles.chatWindow}>
        {messages.map((message, index) => (
          <div key={index} style={message.sender === "user" ? styles.userMessage : styles.botMessage}>
            {message.text}
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div style={styles.inputContainer}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Nhập tin nhắn..."
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.button}>
          Gửi
        </button>
      </div>
    </div>
  );
};

// CSS styles
const styles = {
  wrapper: {
    display: "flex",
    flexDirection: "column" as const,
    height: "100vh", // Full height of the viewport
    position: "relative" as const,
  },
  chatWindow: {
    flex: 1,
    padding: "20px",
    overflowY: "auto" as const,
    backgroundColor: "#fff",
    borderRadius: "8px",
    border: "1px solid #ddd",
    marginBottom: "60px", // Để trừ khoảng trống cho input fixed bên dưới
  },
  inputContainer: {
    position: "fixed" as const,
    bottom: "0",
    left: "200px",
    right: "200px",
    display: "flex",
    padding: "20px",
    backgroundColor: "#fff",
    borderTop: "1px solid #ddd",
    boxShadow: "0 -2px 10px rgba(0, 0, 0, 0.1)",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    resize: "none" as const, 
    overflowWrap: "break-word" as const, 
  },
  button: {
    marginLeft: "10px",
    padding: "10px 20px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#007bff",
    color: "white",
    cursor: "pointer",
  },

  userMessage: {
    textAlign: "right" as const,
    margin: "10px auto", 
    backgroundColor: "#e0e0e0",
    color: "black",
    padding: "10px",
    borderRadius: "10px",
    maxWidth: "600px", 
    width: "20%", 
  },
  botMessage: {
    margin: "10px auto", // Căn giữa
    padding: "10px",
    borderRadius: "10px",
    maxWidth: "600px", // Giới hạn chiều rộng
    width: "100%", // Giữ nguyên tỷ lệ chiều rộng
    textAlign: "left" as const,
  },
};

export default Chatbot;
