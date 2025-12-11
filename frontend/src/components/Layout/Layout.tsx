import React from 'react'
import Bar from '../Bar'
import { Outlet } from 'react-router-dom'
import './Layout.scss'

function Layout() {
  return (
    <main className='main'>
        <Bar/>
        <Outlet/>
    </main>
    )
  
}

export default Layout