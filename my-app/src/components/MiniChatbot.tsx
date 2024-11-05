import React, { useState, useEffect } from "react";
import axios from "axios";

const MiniChatbot: React.FC = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState<string>("");

  // Khi component được mount, khôi phục lịch sử từ localStorage
  useEffect(() => {
    const storedMessages = localStorage.getItem('chatMessages');
    if (storedMessages) {
      setMessages(JSON.parse(storedMessages));
    }

    // Lắng nghe sự kiện trước khi đóng trang và xóa dữ liệu từ localStorage
    const handleBeforeUnload = () => {
      localStorage.removeItem('chatMessages'); // Xóa lịch sử cuộc trò chuyện
    };

    // Thêm sự kiện khi component được mount
    window.addEventListener('beforeunload', handleBeforeUnload);

    // Cleanup event listener khi component bị hủy bỏ
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  // Hàm để lưu lịch sử tin nhắn vào localStorage
  const saveMessagesToLocalStorage = (updatedMessages: any[]) => {
    localStorage.setItem('chatMessages', JSON.stringify(updatedMessages));
  };

  const sendMessage = async () => {
    if (input.trim() === "") return;

    // Thêm tin nhắn của người dùng vào cuộc trò chuyện
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    
    // Lưu tin nhắn vào localStorage
    saveMessagesToLocalStorage(newMessages);

    try {
      // Gửi tin nhắn tới Rasa server thông qua API
      const response = await axios.post("http://localhost:5005/webhooks/rest/webhook", {
        sender: "user",  // ID của người dùng, bạn có thể thay đổi nếu cần
        message: input,
      });

      // Thêm phản hồi từ bot vào cuộc hội thoại
      const botMessages = response.data.map((message: any) => ({
        sender: "bot",
        text: message.text,
      }));

      const updatedMessages = [...newMessages, ...botMessages];
      setMessages(updatedMessages);

      // Lưu lại toàn bộ tin nhắn (bao gồm cả bot) vào localStorage
      saveMessagesToLocalStorage(updatedMessages);
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
    <div style={styles.container}>
      <div style={styles.chatWindow}>
        {messages.map((message, index) => (
          <div key={index} style={message.sender === "user" ? styles.userMessage : styles.botMessage}>
            {message.text}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Nhập tin nhắn..."
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.button}>Gửi</button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    position: "fixed" as const,
    bottom: "80px",
    right: "20px",
    display: "flex",
    flexDirection: "column" as const,
    height: "500px",
    width: "400px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    backgroundColor: "white",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
  },
  chatWindow: {
    flex: 1,
    padding: "10px",
    overflowY: "scroll" as const,
  },
  inputContainer: {
    display: "flex",
    padding: "10px",
    borderTop: "1px solid #ccc",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "25px",
    border: "1px solid #ccc",
    resize: "none" as const,  // Vô hiệu hóa resize
    overflowWrap: "break-word" as const,  // Tự động xuống dòng
  },
  button: {
    marginLeft: "10px",
    padding: "10px 20px",
    borderRadius: "4px",
    border: "none",
    backgroundColor: "#007bff",
    color: "white",
    cursor: "pointer",
  },
  userMessage: {
    textAlign: "right" as const,
    margin: "5px 0",
    backgroundColor: "#007bff",
    color: "white",
    padding: "10px",
    borderRadius: "10px",
  },
  botMessage: {
    textAlign: "left" as const,
    margin: "5px 0",
    backgroundColor: "#f1f1f1",
    padding: "10px",
    borderRadius: "10px",
  },
};

export default MiniChatbot;
