import React, { useState } from 'react';
import axios from 'axios';

function Upload() {
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [message, setMessage] = useState('');

  // Hàm xử lý việc chọn file
  const handleFileUpload = (event) => {
    setSelectedFiles(event.target.files);  // Cập nhật selected files
  };

  // Hàm xử lý việc upload file
  const handleUploadClick = async () => {
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('uploadfiles', selectedFiles[i]);  // Đưa file vào form data
    }

    try {
      const response = await axios.post('http://localhost:8000/upload_file', formData); // Gửi request upload file
      setMessage(response.data.message);  // Cập nhật message từ response
    } catch (error) {
      setMessage('Error uploading files');  // Xử lý khi gặp lỗi
    }
  };

  return (
    <div>
      <h2>Upload Files</h2>
      <input type="file" multiple onChange={handleFileUpload} />
      <button onClick={handleUploadClick}>Upload</button>
      <p>{message}</p> {/* Hiển thị thông báo */}
    </div>
  );
}

export default Upload;
