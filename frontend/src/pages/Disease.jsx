import React, { useState } from 'react';
import axios from 'axios';
import imageCompression from 'browser-image-compression';  // Import image compression library

const DiseaseUpload = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png'];
  const MAX_SIZE = 5 * 1024 * 1024;  // 5MB
  const handleImageChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
      alert('Invalid file type. Only JPG, JPEG, PNG are allowed.');
      setSelectedImage(null);
      setPreview(null);
      return;
    }

    // Validate file size
    if (file.size > MAX_SIZE) {
      alert('File is too large. Maximum allowed size is 5MB.');
      setSelectedImage(null);
      setPreview(null);
      return;
    }

    try {
      // For smaller images, we can use them directly without compression
      if (file.size <= 1 * 1024 * 1024) { // If less than 1MB
        setSelectedImage(file);
        setPreview(URL.createObjectURL(file));
      } else {
        // Image compression options
        const options = {
          maxSizeMB: 1,  // Max size of 1MB after compression
          maxWidthOrHeight: 500,  // Max width or height of 500px
          useWebWorker: true,  // Use Web Worker for compression
          fileType: `image/${fileExtension === 'jpg' ? 'jpeg' : fileExtension}` // Preserve file type
        };
        
        console.log("Compressing image...");
        const compressedFile = await imageCompression(file, options);
        console.log("Original file:", file);
        console.log("Compressed file:", compressedFile);
        
        // Create a new File object with the correct extension
        const newFile = new File(
          [compressedFile], 
          file.name, // Keep original filename
          { type: compressedFile.type }
        );
        
        setSelectedImage(newFile);
        setPreview(URL.createObjectURL(newFile));
      }
    } catch (error) {
      console.error('Error while processing image:', error);
      // Use original file as fallback
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
    }

    setResult(null);  // Reset result on new image
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
      console.log("Sending file:", selectedImage.name, "Type:", selectedImage.type, "Size:", selectedImage.size);
      
      const response = await axios.post('http://127.0.0.1:8000/predict-disease', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      console.log("Response:", response.data);
      setResult(response.data);
    } catch (error) {
      console.error('Prediction failed:', error);
      let errorMessage = 'Error occurred during prediction.';
      
      // Get more specific error message if available
      if (error.response && error.response.data) {
        errorMessage = error.response.data.detail || error.response.data.error || errorMessage;
      }
      
      setResult({ error: errorMessage });
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
        className="mb-4 w-full"  // Full width input for mobile optimization
      />
      
      {preview && (
        <img
          src={preview}
          alt="Preview"
          className="mb-4 rounded-lg shadow w-full object-cover h-64"  // Responsive image preview
        />
      )}

      <button
        onClick={handleSubmit}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 w-full"  // Full width button for mobile
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Submit'}
      </button>

      {result && !result.error && (
        <div className="mt-6 bg-gray-100 p-4 rounded-lg shadow text-sm">
          <p><strong>Disease:</strong> {result.predicted_class}</p>
          <p><strong>Confidence:</strong> {result.confidence.toFixed(2)}%</p>
          <p><strong>Treatment:</strong> {result.treatment}</p>
        </div>
      )}

      {result?.error && (
        <div className="mt-4 text-red-600 text-center font-semibold">
          {result.error}
        </div>
      )}
    </div>
  );
};

export default DiseaseUpload;
