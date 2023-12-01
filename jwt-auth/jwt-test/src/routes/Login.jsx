import React, { useContext, useEffect, useRef } from 'react';
import { NavLink } from 'react-router-dom';
import Cookies from 'universal-cookie';

function Login() {
    const emailRef = useRef();
    const passwordRef = useRef();
    const imageLinkRef = useRef();
    const cookies = new Cookies();
    function login() {
        const email = emailRef.current.value;
        const password = passwordRef.current.value;

        const url = 'http://127.0.0.1:8000/login';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify({
                email,
                password
            }),
        })
            .then(res => res.json())
            .then(data => handleJWT(data))
            .catch(e => console.log(e));
    }

    function handleJWT(data) {
        console.log(data);
        if (data.email && data.jwt_token) {
            cookies.set("test_user",JSON.stringify({ email : data.email, jwt_token: data.jwt_token }), { path: '/' });
            sessionStorage.setItem("authenticated_user",JSON.stringify({ email : data.email, jwt_token: data.jwt_token }),)
            
            alert('logged in!');
            setTimeout(() => {
                imageLinkRef.current.click();
            }, 1000);
        } else {
            alert('Invalid credentials!');
            sessionStorage.removeItem("authenticated_user")
            cookies.remove("test_user")
            window.location.reload();
        }
    }
    
    return (
        <>
            <div className="login-container">
                <h2>Login</h2>
                <form id="login-form">
                    <label htmlFor="email">Email:</label>
                    <input type="text" id="email" name="email" ref={emailRef} required />
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" ref={passwordRef} required />
                    <button type="button" onClick={login}>Login</button>
                </form>
            </div>
            <NavLink ref={imageLinkRef} to={'/img-grayscale'}></NavLink>
        </>
    );
}

export default Login;
