import React from 'react';
import { Redirect } from 'react-router-dom';
import { useSelector } from 'react-redux'

export default function ProtectedRoute({Component}){
    const isLogged = useSelector(state => state.logged);
            return(
        <>
        {
            isLogged.logged ?
                <Component />
            :
            <Redirect to={{ pathname: '/login' }} />
        }
        </>
    )
}