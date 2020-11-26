import React from 'react';
import { Redirect } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'
import axios from 'axios';
import https from 'https';
import { signin } from '../../../redux/actions';


const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent

export default function EntryPoint() {
    const isLogged = useSelector(state => state.logged);
    const dispatch = useDispatch();

    if (isLogged.logged) {
        axios.post('https://150.136.172.48/api/auth/refresh', {}, {
            headers: {
                'Authorization': `Bearer ${isLogged.token}`
            }
        }).then(function (response) {
            let status = response.data.status === 'success' ? true : false;
            dispatch(signin(status, response.data.auth_token));
        }).catch(function (error) {
            if (error.response && error.response.status === 401) {
                dispatch(signin(false, ''));
            }
        })
        return <Redirect to={{ pathname: '/dashboard/resultTables' }} />
    }
    else {
        return <Redirect to={{ pathname: '/login' }} />
    }
}