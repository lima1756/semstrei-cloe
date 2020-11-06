import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { Box, Grid, makeStyles, } from '@material-ui/core';
import AppBar from '../AppBarDrawer/AppBar';
import Prueba from '../../../assets/prueba.jpg';
import { useSnackbar} from 'notistack';
import { useDispatch } from 'react-redux';
import { userinformation, signin } from '../../../redux/actions';
import axios from 'axios';
import https from 'https';
import LoginForm from './components/LoginForm';
import RecoverPassword from './components/RecoverPassword';

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
}));

export default function Login() {
    const history = useHistory();
    const [state, setState] = useState({ checkedG: true, });
    const [view, setView] = useState(true);
    const classes = useStyles();
    const { enqueueSnackbar } = useSnackbar();
    const dispatch = useDispatch();

    const login = (username, password, checked) => {
        axios.post('https://150.136.172.48/api/auth/login', {
            email: username,
            password: password,
            keep: checked
        }).then(function (response) {
            handleSuccessLogin('success');
            let status = response.data.status === 'success' ? true : false;
            dispatch(signin(status, response.data.auth_token));
            dispatch(userinformation(response.data.user.admin,response.data.user.new_user,response.data.user.name,response.data.user.email,response.data.user.phone_number,response.data.user.role,response.data.user.user_id));
            history.push('/dashboard/resultTables');
        }).catch(function (error) {
            handleErrorLogin('error');
        })
    };

    const handleView = () => {
        setView(!view);
    };

    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };

    const handleMailSend = () => {
        handleMailSent('success');
        setView(!view);
    };

    const handleLogin = () => {
        login(document.getElementById("userEmail").value, document.getElementById("password").value, state.checkedG);
        //history.push('/dashboard');
    };

    // ---------------------- Snackbar login success------------------------------
    const handleSuccessLogin = (variant) => { enqueueSnackbar('Sesión iniciada correctamente.', { variant }) };

    // ------------------- Snackbar user or password error --------------------------
    const handleErrorLogin = (variant) => { enqueueSnackbar('El usuario o la contraseña son incorrectos.', { variant }) };
    
    // ------------------------------- Snackbar mail sent --------------------------------
    const handleMailSent = (variant) => { enqueueSnackbar('El correo ha sido enviado.', { variant }) };

    return (
        <div>
            <AppBar />
            <Grid container className={classes.root} direction='row' alignItems='center' justify='center'>
                <Grid item xs={7}>
                    <img src={Prueba} alt='Imagen Principal' style={{ width: '100%', height: '92.9vh', }} />
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
                                    <LoginForm handleView={handleView} handleLogin={handleLogin} handleChange={handleChange} state={state}/>
                                </>
                                :
                                <>
                                    <RecoverPassword handleMailSend={handleMailSend}/>
                                </>
                        }
                    </Box>
                </Grid>
            </Grid>
        </div>
    )
}