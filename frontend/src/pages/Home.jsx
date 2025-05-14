import React from 'react';

const Home = () => {
  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🌿 Welcome to AgriAI</h1>
      <p className="mb-4">
        AgriAI is an intelligent agricultural assistant that helps farmers make better decisions.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 border rounded hover:shadow-md bg-green-50">
          <h2 className="font-bold">🌾 Crop Prediction</h2>
          <p>Get recommendations for the best crops to grow based on soil conditions.</p>
        </div>
        <div className="p-4 border rounded hover:shadow-md bg-green-50">
          <h2 className="font-bold">🔍 Disease Detection</h2>
          <p>Upload plant images to detect diseases and get treatment recommendations.</p>
        </div>
        <div className="p-4 border rounded hover:shadow-md bg-green-50">
          <h2 className="font-bold">💬 AI Chat Assistant</h2>
          <p>Ask questions and get expert agricultural advice.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;