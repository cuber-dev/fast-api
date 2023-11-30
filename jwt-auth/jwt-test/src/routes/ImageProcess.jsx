import React, { useContext, useEffect, useState, useRef } from 'react';
import { context } from '../App';

function ImageProcess() {
    const { user } = useContext(context);
    
    const [loggedUser, setLoggedUser] = useState(user);
    const [image,setImage] = useState()

    const inputRef = useRef(null);
    const previewContainerRef = useRef(null);
    const previewRef = useRef(null);
    const grayscalePreviewRef = useRef(null)
    const grayscaleContainerRef = useRef(null)

    function uploadImage() {
        const file = inputRef.current.files[0];
        setImage(file)
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                previewRef.current.src = e.target.result;
                previewContainerRef.current.style.display = 'block';
            };

            reader.readAsDataURL(file);
        }
    }

    async function convertToGrayscale() {
        const url = `http://127.0.0.1:8000/grayscale`
        async function getFormData() {  
            const formData = new FormData();
            formData.append('image', image);
            return formData;
          }
        
          async function fetchData() {
            try {
              const formData = await getFormData();
              const response = await fetch(url, {
                method: 'POST',
                headers: {
                  'accept': 'application/json',
                  'Authorization': `Bearer ${user.a_t}`,
                },
                body: formData,
              });
          
              if (!response.ok) {
                throw new Error('Failed to fetch data from the API');
              }
          
              let data = await response.json();
              console.log(data);
              return data;
            } catch (error) {
              console.error('Error fetching data:', error);
              return 'Internal Server Error, please try again later';
            }
          }
          

        function mountGrayscaleImage(data){
            const { grayscale_img } = data;
            if (grayscale_img) {
                grayscalePreviewRef.current.src = grayscale_img;
                grayscaleContainerRef.current.style.display = 'block';
            } 
        }
        const data = await fetchData()
        if(data) mountGrayscaleImage(data);
    }
    function downloadImage() {
        const a = document.createElement('a');
      
        // Convert base64 to Blob
        const byteCharacters = atob(grayscalePreviewRef.current.src.split(',')[1]);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'image/jpeg' });
      
        // Create a blob URL
        const url = URL.createObjectURL(blob);
      
        a.href = url;
        a.download = 'grayscale_image.jpg';
        a.click();
      
        // Clean up the URL
        URL.revokeObjectURL(url);
      }
      
    useEffect(() => {
        if(!user.email && !user.a_t){
            alert('unauthorized , please login first!')
            window.location.href = '/'
            return;
        }
    }, []);

    return (
        <>
            <div className="user-details">
                <h1>User name: {loggedUser.name}</h1>
                <p>You are logged in, now you can use our software.</p>
            </div>
            <div className="upload-container" id="upload-container">
                <h2>Upload Image</h2>
                <input type="file" id="image-input" accept="image/*" ref={inputRef} onChange={uploadImage} style={{ display: 'none' }} />
                <label htmlFor='image-input' className='btn' >Upload Image</label>

                <div id="image-preview-container container" className='image-preview-container' ref={previewContainerRef}>
                    <h3>Image Preview</h3>
                    <img className="image-preview" alt="Image Preview" ref={previewRef} />
                    <br />
                    <button type="button" onClick={convertToGrayscale} className='btn'>
                        Convert to Grayscale
                    </button>
                </div>
                <div className="image-preview-container container" ref={grayscaleContainerRef}>
                    <h3>Converted Image Preview</h3>
                    <img alt="image" className="image-preview" ref={grayscalePreviewRef} />
                    <button className="btn" onClick={downloadImage}>Download Image</button>
                </div>
            </div>
        </>
    );
}

export default ImageProcess;
