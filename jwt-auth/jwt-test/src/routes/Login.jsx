import React, { useContext, useRef } from 'react';
import { context } from '../App';
import { NavLink } from 'react-router-dom';

function Login() {
    const { setUser } = useContext(context);
    const emailRef = useRef();
    const passwordRef = useRef();
    const imageLinkRef = useRef();

    function login() {
        const email = emailRef.current.value;
        const password = passwordRef.current.value;

        const url = 'http://127.0.0.1:8000/users/login';
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
            .then(data => redirect(data))
            .catch(e => console.log(e));
    }

    function redirect(data) {
        console.log(data);
        if (data.email && data.access_token) {
            setUser(prev => ({ name: data.email, a_t: data.access_token }))
            alert('logged in!')
            setTimeout(() => {
                imageLinkRef.current.click();
            }, 1000);
        }else{
            alert('Invalid credntials!')
            window.location.reload()
        }
    }

    return (
        <>
            <div className="login-container">
                <h2>Login</h2>
                <form id="login-form">
                    <label htmlFor="email">Email:</label>
                    <input type="text" id="email" name="email" ref={emailRef} required />
                    <br />
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" ref={passwordRef} required />
                    <br />
                    <button type="button" onClick={login}>Login</button>
                </form>
            </div>
            <NavLink ref={imageLinkRef} to={'/image'}></NavLink>
        </>
    );
}

export default Login;
