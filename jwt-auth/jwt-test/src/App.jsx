import './App.css'
import  { Routes, Route} from 'react-router-dom'
import ImageProcess from './routes/ImageProcess';
import Login from './routes/Login';
import React, { useState } from 'react';

export const context = React.createContext()

function App() {
  const [user,setUser] = useState({
    name : '', a_t : ''
  })
  return ( <>
      <context.Provider value={{user,setUser}}>
        <Routes>
          <Route path={'/'} element={<Login />} />
          <Route path={'/image'} element={<ImageProcess />} />
        </Routes>
      </context.Provider>
</> );
}

export default App
