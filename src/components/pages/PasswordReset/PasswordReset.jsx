import React from 'react';
import { useHistory } from 'react-router-dom';
import { Box, Button, Grid, makeStyles, TextField, Typography} from '@material-ui/core';
import AppBar from '../AppBarDrawer/AppBar';
import Prueba from '../../../assets/prueba.jpg';
import { useSnackbar} from 'notistack';
import axios from 'axios';
import https from 'https';

const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent

const useStyles = makeStyles((theme) => ({
    root: {
        height: "90vh",
    },
    paper: {
        textAlign: 'center',
        color: theme.palette.text.secondary,
        padding: theme.spacing(5),
    },
    spacingItems: {
        paddingBottom: theme.spacing(3),
    },
    marginButton: {
        margin: theme.spacing(2),
        width: '50%',
        background: '#000',
    },
}));

export default function Login() {
    const history = useHistory();
    const classes = useStyles();
    const { enqueueSnackbar } = useSnackbar();

    const passwordReset = (username, password) => {
        axios.post('https://150.136.172.48/api/auth/login', {
            email: username,
            password: password,
        }).then(function (response) {
            handlePasswordUpdate('success');
            history.push('/login');
        }).catch(function (error) {
            handlePasswordError('error');
        })
    };

    const handlePasswordReset = () => {
        //login(document.getElementById("userEmail").value, document.getElementById("password").value, state.checkedG);
        history.push('/login');
    };

    // ---------------------- Snackbar login success------------------------------
    const handlePasswordUpdate = (variant) => { enqueueSnackbar('La contraseña se ha actualizado.', { variant }) };

    // ------------------- Snackbar user or password error --------------------------
    const handlePasswordError = (variant) => { enqueueSnackbar('Hubo un error al hacer el cambio de contraseña.', { variant }) };

    return (
        <div>
            <AppBar />
            <Grid container className={classes.root} direction='row' alignItems='center' justify='center'>
                <Grid item xs={7}>
                    <img src={Prueba} alt='Imagen Principal' style={{ width: '100%', height: '92.9vh', }} />
                </Grid>
                <Grid item xs={5} >
                    <Box className={classes.paper} style={{ margin: 'auto' }}>
                        <Typography className={classes.spacingItems} align="left">Restablecer la contraseña</Typography>
                        <TextField fullWidth label="Contraseña" type="password" id="newPassword"/>
                        <TextField fullWidth label="Repetir contraseña" type="password" id="passwordRepeat" className={classes.spacingItems}/>
                        <Button variant="contained" size="large" className={classes.marginButton} onClick={handlePasswordReset}><span style={{ color: '#fff' }}>Confirmar contraseña</span></Button>
                    </Box>
                </Grid>
            </Grid>
        </div>
    )
}