import React, { useState } from 'react';
import axios from 'axios';

function Crop() {
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });

  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      console.log("Form Data:", formData);
      const response = await axios.post('http://127.0.0.1:8000/predict-crop', formData);

      console.log("API Response:", response.data);
      setPrediction(response.data.prediction);  // ✅ Fixed this line
    } catch (error) {
      console.error('Prediction failed:', error);
      setPrediction('Error occurred during prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Crop Prediction</h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
        {Object.keys(formData).map((key) => (
          <div key={key} className="col-span-2">
            <input
              type="number"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              placeholder={key.toUpperCase()}
              className="border p-2 rounded w-full"
              required
            />
          </div>
        ))}
        <div className="col-span-2">
          <button 
            type="submit" 
            className="w-full bg-green-600 text-white p-2 rounded"
          >
            {loading ? 'Predicting...' : 'Predict Crop'}
          </button>
        </div>
      </form>

      {prediction && (
        <div className="mt-4 bg-green-100 p-4 rounded">
          <strong>Recommended Crop:</strong> {prediction}
        </div>
      )}
    </div>
  );
}

export default Crop;
