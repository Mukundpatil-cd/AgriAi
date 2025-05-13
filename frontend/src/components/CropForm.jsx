import React, { useState } from 'react';
import axios from 'axios';

// 🟩 Crop Prediction Form
const CropForm = () => {
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: '',
    location: '',
    soil_quality: ''
  });

  const [predictedCrop, setPredictedCrop] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict-crop', formData);
      setPredictedCrop(response.data.crop);
    } catch (error) {
      console.error('Prediction failed:', error);
    }
  };

  return (
    <div>
      <h2>🌾 Crop Prediction Form</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label>{key.toUpperCase()}:</label>
            <input
              type={['location', 'soil_quality'].includes(key) ? 'text' : 'number'}
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
            />
          </div>
        ))}
        <br />
        <button type="submit">Predict Crop</button>
      </form>

      {predictedCrop && (
        <div>
          <h3>✅ Predicted Crop: {predictedCrop}</h3>
        </div>
      )}
    </div>
  );
};

// 🟦 User Data Submission Form
const UserDataForm = () => {
  const [location, setLocation] = useState('');
  const [soilQuality, setSoilQuality] = useState('');
  const [userId, setUserId] = useState('1'); // Default user_id for now

  const handleSubmit = async (e) => {
    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("📨 Submitting data:", formData);
      
        try {
          const response = await axios.post('http://127.0.0.1:8000/predict-crop', formData);
          console.log("✅ Prediction response:", response.data);
          setPredictedCrop(response.data.crop);
        } catch (error) {
          console.error('❌ Prediction failed:', error);
          alert("Prediction failed: " + error.message);
        }
      };
      
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/save-user-data', {
        method: 'POST',
        body: JSON.stringify({
          user_id: parseInt(userId),
          location: location,
          soil_quality: soilQuality
        }),
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await response.json();
      alert(data.message || 'Data submitted');
    } catch (err) {
      alert('Error submitting user data');
      console.error(err);
    }
  };

  return (
    <div>
      <h2>👤 User Data Form</h2>
      <form onSubmit={handleSubmit}>
        <label>User ID:</label>
        <input
          type="number"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          required
        />

        <label>Location:</label>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          required
        />

        <label>Soil Quality:</label>
        <input
          type="text"
          value={soilQuality}
          onChange={(e) => setSoilQuality(e.target.value)}
          required
        />

        <br />
        <button type="submit">Submit User Data</button>
      </form>
    </div>
  );
};

// 🔄 Export both
export { CropForm, UserDataForm };

// ✅ Default export AgriAI Forms page with both forms
const AgriAIFormsPage = () => (
  <div>
    <h1>🌿 AgriAI Forms</h1>
    <UserDataForm />
    <hr />
    <CropForm />
  </div>
);

export default AgriAIFormsPage;
