import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CropForm from './components/CropForm';
import Navbar from './components/Navbar';
import DiseaseUpload from './pages/Disease';
import ChatBot from './components/ChatBot';
import Home from './pages/Home';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/crop" element={<CropForm />} />
            <Route path="/disease" element={<DiseaseUpload />} />
            <Route path="/chat" element={<ChatBot />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
