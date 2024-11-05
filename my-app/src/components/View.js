import React, { useState } from 'react';
import axios from 'axios';

function View() {
  const [metadata, setMetadata] = useState('');
  
  const handlePrintMetadata = async () => {
    try {
      const response = await axios.get('http://localhost:8000/print_metadata');
      setMetadata(response.data.message);
    } catch (error) {
      setMetadata('Error fetching metadata');
    }
  };

  return (
    <div>
      <h2>View Metadata</h2>
      <button onClick={handlePrintMetadata}>Get Metadata</button>
      <pre>{metadata}</pre>
    </div>
  );
}

export default View;
