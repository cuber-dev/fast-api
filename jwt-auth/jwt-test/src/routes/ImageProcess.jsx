import React, { useEffect, useState, useRef } from 'react';
import Cookies from 'universal-cookie';

function ImageProcess({ requestAuth }) {
    const cookies = new Cookies();
    const [loggedUser, setLoggedUser] = useState(() => {
      const authenticated_user = sessionStorage.getItem("authenticated_user")
      if(authenticated_user) return JSON.parse(authenticated_user)
      
      requestAuth("img-grayscale")
      setTimeout(() => {
          window.location.reload()
      }, 1000);
      return null
    });
    const [uploadedImage,setUploadedImage] = useState()

    const inputRef = useRef(null);
    const previewContainerRef = useRef(null);
    const previewRef = useRef(null);
    const grayscalePreviewRef = useRef(null)
    const grayscaleContainerRef = useRef(null)

    function uploadImage() {
        const file = inputRef.current.files[0];
        setUploadedImage(file)
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                previewRef.current.src = e.target.result;
                previewContainerRef.current.classList.remove('disabled');
            };

            reader.readAsDataURL(file);
        }
    }
   
    async function convertToGrayscale() {
        const url = `http://127.0.0.1:8000/grayscale/${uploadedImage.name}`
        async function getFormData() {  
            const formData = new FormData();
            formData.append('image', uploadedImage);
            console.log(uploadedImage)
            return formData;
          }
        
          async function fetchData() {
            try {
              const formData = await getFormData();
              const response = await fetch(url, {
                method: 'POST',
                headers: {
                  'accept': 'application/json',
                  'Authorization': `Bearer ${loggedUser.jwt_token}`,
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
                grayscaleContainerRef.current.classList.remove('disabled');
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
        a.download = `grayscale_${uploadedImage.name}`;
        a.click();
      
        // Clean up the URL
        URL.revokeObjectURL(url);
      }
    useEffect(() => {
        if(!loggedUser){
          document.body.classList.add('disabled');
          requestAuth("img-grayscale")
          
          setTimeout(() => {
            const authenticated_user = sessionStorage.getItem("authenticated_user")
            if(authenticated_user) setLoggedUser(JSON.parse(authenticated_user))
            document.body.classList.remove('disabled');
          }, 1000);
        }
    },[loggedUser])
    return (
        <>
            <div className="user-details" style={
              loggedUser ? { backgroundColor: "#f0fff1" } : { backgroundColor : "#fff0f0" } 
            }>
                <h1>Email: {loggedUser ? loggedUser.email : "Not Athenticated!"}</h1>
                <p>{loggedUser ? `You are logged in as ${loggedUser.email}. 
                  Now you can upload your image and convert it to grayscale. 
                  After converting the image to grayscale, you can download it.`
                  : (
                  "Please wait, until we authenticate you."
                ) }</p>
            </div>
            <div className="upload-container" id="upload-container">
                <h2>Convert Image to Grayscale Image.</h2>
                <input type="file" id="image-input" accept="image/*" ref={inputRef} onChange={uploadImage}  />
                <label htmlFor='image-input' className='upload-btn btn' >Upload Image</label>

                <div className="inline-container">
                <div id="image-preview-container" className='image-preview-container  container disabled' ref={previewContainerRef}>
                    <h3>Uploaded Image Preview</h3>
                    <img className="image-preview" alt="Image Preview" ref={previewRef} />
                    
                    <button type="button" onClick={convertToGrayscale} className='btn'>
                        Convert to Grayscale
                    </button>
                </div>
                <div className="image-preview-container container disabled" ref={grayscaleContainerRef}>
                    <h3>Converted Image Preview</h3>
                    <img alt="image-preview" className="image-preview" ref={grayscalePreviewRef} />
                    
                    <button className="btn" onClick={downloadImage}>Download Image</button>
                </div>
                </div>
            </div>
        </>
    );
}

export default ImageProcess;
