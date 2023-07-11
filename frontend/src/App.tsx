import React, { useState } from 'react';

function App() {
  const [prompts, setPrompts] = useState<string[]>([]);
  const [images, setImages] = useState<string[]>([]);

  const handleGenerateClick = async () => {
    const response = await fetch('http://localhost:8000/generate_broll', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompts: ['Prompt 1', 'Prompt 2', 'Prompt 3'],
      }),
    });

    const data = await response.json();
    setPrompts(data.prompts);
    setImages(data.images);
  };

  return (
    <div>
      <h1>B-Roll Generator</h1>
      <button onClick={handleGenerateClick}>Generate B-Roll</button>
      <div>
        {images.map((image, index) => (
          <div key={index}>
            <h3>Prompt: {prompts[index]}</h3>
            <img src={`data:image/png;base64, ${image}`} alt={`B-Roll ${index + 1}`} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
