import React from 'react';
import Drawer from './Drawer'

export default function Dashboard(){
    return(
        <div>
            <Drawer index={0}/>
            <h1 style={{marginLeft:280, marginTop:70}}>Dashboard</h1>
        </div>
    )
}