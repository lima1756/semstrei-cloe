import React, { useState } from 'react';
import { Link, useHistory } from 'react-router-dom';
import {
    Box, Button, Checkbox, FormControlLabel, Grid, makeStyles, TextField, Typography, 
} from '@material-ui/core';
import AppBar from './AppBar';
import Prueba from '../assets/prueba.jpg';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

import axios from 'axios';
import https from 'https';

import auth from '../auth';

const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent
//axios.defaults.headers.common['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDY1MTAyMDAsImlhdCI6MTYwMzkxODIwMCwiaWQiOjF9.ucki8xqRxG9MWLsCu43fszERFSB2x7vuqNyIlHXTsr0';

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
    root: {
        height: "90vh",
    },
    paper: {
        textAlign: 'center',
        color: theme.palette.text.secondary,
        padding: theme.spacing(5),
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: '25ch',
    },
    marginButton: {
        margin: theme.spacing(2),
        width: '50%',
        background: '#000',
    },
    spacingItems: {
        paddingBottom: theme.spacing(3),
    },
}));

export default function Login({props}) {
    const history = useHistory();
    const [open, setOpen] = React.useState(false);
    const [state, setState] = useState({ checkedG: true, });
    const [view, setView] = useState(true);
    const classes = useStyles();

    const login = (username, password, checked) => {
        axios.post('https://150.136.172.48/api/auth/login', {
            email: username,
            password: password,
            keep: checked
        }).then(function (response) {
            console.log(response);
            //console.log('Pasa por aca');
            history.push('/dashboard')
        }).catch(function (error) {
            console.log(error);
            //console.log('Pasa aqui')
            setOpen(true);
        })
    };

    const handleView = () => {
        setView(!view);
    };

    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpen(false);
    };

    const handleLogin = () => {
        // console.log('username: ', document.getElementById("userEmail").value);
        // console.log('password: ', document.getElementById("password").value);
        // console.log(state.checkedG);
        login(document.getElementById("userEmail").value, document.getElementById("password").value, state.checkedG);
        
        // auth.login(() => {
        //     props.history.push("/dashboard");
        // })
    };

    return (
        <div>
            <AppBar />
            <Grid container className={classes.root} direction='row' alignItems='center' justify='center'>
                <Grid item xs={7}>
                    <img src={Prueba} alt="logo" style={{ width: '100%', height: '92.9vh', }} />
                </Grid>
                <Grid item xs={5} >
                    <Box className={classes.paper} style={{ margin: 'auto' }}>
                        {/* <Typography className={classes.spacingItems} align="left">Restablecer la contraseña</Typography>
                        <TextField fullWidth label="Contraseña" type="password" id="newPassword"/>
                        <TextField fullWidth label="Repetir contraseña" type="password" id="passwordRepeat" className={classes.spacingItems}/>
                        <Button component={Link} to={'/login'} variant="contained" color="primary" className={classes.margin}>Confirmar contraseña</Button> */}
                        {
                            view ?
                                <>
                                    <Typography className={classes.spacingItems} align="left">Inicia sesiòn</Typography>
                                    <TextField fullWidth id="userEmail" label="Correo" />
                                    <TextField className={classes.spacingItems} fullWidth id="password" label="Password" type="password" autoComplete="current-password" />
                                    {/* <Button component={Link} to={'/dashboard'} variant="contained" size="large" className={classes.marginButton}><span style={{color:'#fff'}}>Iniciar sesiòn</span></Button> */}
                                    <Button variant="contained" size="large" className={classes.marginButton} onClick={handleLogin}><span style={{ color: '#fff' }}>Iniciar sesiòn</span></Button> 
                                    <FormControlLabel
                                        control={<Checkbox
                                            color='default'
                                            checked={state.checkedG}
                                            onChange={handleChange}
                                            name="checkedG" />
                                        }
                                        label={
                                            <Typography>Recordarme &nbsp; &nbsp; ¿Olvidaste la contraseña? <Link onClick={handleView}>Recuperar contraseña</Link></Typography>
                                        } />
                                    <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
                                        <Alert onClose={handleClose} severity="error">
                                            El usuario o la contraseña son incorrectos.
                                        </Alert>
                                    </Snackbar>
                                </>
                                :
                                <>
                                    <Typography className={classes.spacingItems} align="left">Recuperar contraseña</Typography>
                                    <Typography className={classes.spacingItems} align="left">Si ha olvidado su contraseña, por favor proporcione el correo con el que esta registrado. En breve le llegará un correo con una liga para resetear la contraseña.</Typography>
                                    <TextField fullWidth id="recoverMail" label="Correo" />
                                    <Button variant="contained" className={classes.marginButton} onClick={handleView}><span style={{ color: '#fff' }}>Enviar correo</span></Button>
                                </>
                        }
                    </Box>
                </Grid>
            </Grid>
        </div>
    )
}