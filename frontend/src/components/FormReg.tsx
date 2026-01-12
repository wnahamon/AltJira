import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import './styles/FormLogin.scss'


function FormReg() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [email, setEmail] = useState<string>('');

  const Authentication = async (event:any) => {
    event.preventDefault();
    try {
      await axios.post("http//0.0.0.0:8000/api/reg/", {username, password, email})
      console.log('Успех')
    } catch (error) {
      console.error('Ошибка');
    }
  }

  return (
    <>
        <form onSubmit={Authentication}>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
            <input type="email" value={password} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />    
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />

          <button type="submit">Registration</button>
        </form>
    </>
  )
}

export default FormReg