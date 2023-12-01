import './App.css'
import  { Routes, Route, NavLink} from 'react-router-dom'
import ImageProcess from './routes/ImageProcess';
import Login from './routes/Login';
import React, { useEffect, useRef, useState } from 'react';
import Cookies from 'universal-cookie'

function App() {

  const imageLinkRef = useRef();
  const cookies = new Cookies();

  const checkUserJWTToken = async (from) => {
    const test_user = cookies.get('test_user');
    if(!test_user){
      console.log("no test user found in cookies")
      if(window.location.pathname == '/img-grayscale') window.location.href = '/';
      return;
    }
    
    const test_jwt = test_user.jwt_token;
    console.log(test_user);

    if (test_jwt) {
      const url = `http://127.0.0.1:8000/validate-t/${test_jwt}`;

      try {
        const res = await fetch(url);
        const data = await res.json();
        console.log(data);
        if (data.is_valid_jwt) {
          setTimeout(() => {
            if(from === "img-grayscale") alert('Now you are Authenticated!');
            else alert('you are already Authenticated!');

            sessionStorage.setItem("authenticated_user",JSON.stringify(test_user))
            imageLinkRef.current.click();
            return;
          }, 1000);
          return true;
        }else{
          sessionStorage.removeItem("authenticated_user")
          cookies.remove("test_user")
          alert('Unauthorized, please login first!');
          if(window.location.pathname == '/img-grayscale') window.location.href = '/';
          return false;
        }
      } catch (e) {
        console.log(e);
        return false;
      }
    }
  };

  useEffect(() => {
    (async () => {
      await checkUserJWTToken();
    })();
  }, []);

  return (
    <>
        <Routes>
          <Route path={'/'} element={<Login />} />
          <Route path={'/img-grayscale'} element={<ImageProcess requestAuth={checkUserJWTToken} />} />
        </Routes>
      <NavLink ref={imageLinkRef} to={'/img-grayscale'}></NavLink>

    </>
  );
}

export default App;