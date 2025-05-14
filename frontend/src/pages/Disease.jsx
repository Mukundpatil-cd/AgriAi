import React, { useState } from 'react';
import axios from 'axios';

const DiseaseUpload = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setSelectedImage(file);
    setPreview(URL.createObjectURL(file));
    setResult('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedImage) {
      alert('Please upload an image.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:8000/predict-disease', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResult(`Prediction: ${response.data.predicted_class}`);
    } catch (error) {
      console.error('Prediction failed:', error);
      setResult('Error occurred during prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-4 bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-bold mb-4">Disease Detection</h2>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="mb-4"
      />
      
      {preview && (
        <img
          src={preview}
          alt="Preview"
          className="mb-4 rounded-lg shadow"
        />
      )}

      <button
        onClick={handleSubmit}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Submit'}
      </button>

      {result && (
        <div className="mt-4 text-lg font-semibold text-center text-blue-700">
          {result}
        </div>
      )}
    </div>
  );
};

export default DiseaseUpload;
