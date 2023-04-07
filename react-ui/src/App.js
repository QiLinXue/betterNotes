import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [mdContent, setMdContent] = useState('');
  const iframeRef = useRef(null);

  // Load the default content from default.txt
  useEffect(() => {
    const loadDefaultContent = async () => {
      try {
        const response = await fetch('/static/default.txt');
        const defaultContent = await response.text();
        setMdContent(defaultContent);
      } catch (error) {
        console.error('Error loading default content:', error);
      }
    };

    loadDefaultContent();
  }, []);

  const BACKEND_URL =
  process.env.NODE_ENV === "production"
    ? window.location.origin
    : process.env.REACT_APP_BACKEND_URL || "http://localhost:5000";

  const handleConvert = async () => {
    try {
      const response = await axios.post(`${BACKEND_URL}/convert`, { md_content: mdContent });

      if (iframeRef.current) {
        const iframeWindow = iframeRef.current.contentWindow;
        iframeWindow.document.open();
        iframeWindow.document.write('<!DOCTYPE html><html><head></head><body></body></html>');
        iframeWindow.document.close();
  
        // Use a Blob to set the src attribute of the iframe
        const blob = new Blob([response.data.html_content], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        iframeRef.current.onload = () => {
          URL.revokeObjectURL(url);
          iframeRef.current.onload = null;
        };
        iframeRef.current.src = url;
      }
    } catch (error) {
      console.error('Error converting Markdown to HTML:', error);
    }
  };

  return (
    <div className="App">
      <h1>BetterNotes Live Demo</h1>
      <button onClick={handleConvert}>Convert</button>
      <div className="content-wrapper">
        <div className="textarea-container">
          <textarea
            placeholder="Enter your Markdown here"
            value={mdContent}
            onChange={(e) => setMdContent(e.target.value)}
          />
        </div>
        <div className="iframe-container">
          <iframe
            ref={iframeRef}
            title="Converted HTML"
            width="100%"
            height="500"
            sandbox="allow-same-origin allow-scripts"
            />
        </div>
      </div>

    </div>
  );
}

export default App;