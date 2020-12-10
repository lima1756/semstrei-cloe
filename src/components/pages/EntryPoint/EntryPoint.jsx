import React from 'react';
import { Redirect } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'
import { makeStyles } from '@material-ui/core/styles';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import axios from 'axios';
import https from 'https';
import { useHistory } from 'react-router-dom';
import { signin } from '../../../redux/actions';


const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent

const useStyles = makeStyles((theme) => ({
    backdrop: {
        zIndex: theme.zIndex.drawer + 1,
        color: '#fff',
    },
}));

export default function EntryPoint() {
    const classes = useStyles();
    const history = useHistory();
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
            history.push('/dashboard/resultTables');
        }).catch(function (error) {
            if (error.response && error.response.status === 401) {
                dispatch(signin(false, ''));
            }
            history.push('/login');
        })
        return <Backdrop className={classes.backdrop} open={true} >
            <CircularProgress color="inherit" />
        </Backdrop>
    }
    else {
        return <Redirect to={{ pathname: '/login' }} />
    }
}