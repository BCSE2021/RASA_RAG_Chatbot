import React, { useState } from 'react';
import axios from 'axios';

function Delete() {
  const [filename, setFilename] = useState('');
  const [message, setMessage] = useState('');

  const handleDeleteClick = async () => {
    try {
      const response = await axios.delete('http://localhost:8000/delete_file', {
        data: { value: filename }
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error deleting file');
    }
  };

  return (
    <div>
      <h2>Delete File</h2>
      <input
        type="text"
        placeholder="Enter filename"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
      />
      <button onClick={handleDeleteClick}>Delete</button>
      <p>{message}</p>
    </div>
  );
}

export default Delete;
