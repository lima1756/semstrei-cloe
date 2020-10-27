import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    Box, Button, Checkbox, FormControlLabel, Grid, makeStyles, TextField, Typography, withStyles
} from '@material-ui/core';
import grey from '@material-ui/core/colors/grey';
import AppBar from './AppBar';
import Prueba from '../assets/prueba.jpg';

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

export default function Login() {
    const [state, setState] = useState({ checkedG: true, });
    const [view, setView] = useState(true);
    const classes = useStyles();

    const handleView = () => {
        setView(!view);
    };

    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };

    const GrayCheckbox = withStyles({
        root: {
            color: grey[400],
            '&$checked': {
                color: grey[600],
            },
        },
        checked: {},
    })((props) => <Checkbox color="default" {...props} />);

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
                                    <TextField className={classes.spacingItems} fullWidth id="standard-password-input" label="Password" type="password" autoComplete="current-password" />
                                    <Button component={Link} to={'/dashboard'} variant="contained" size="large" className={classes.marginButton}><span style={{color:'#fff'}}>Iniciar sesiòn</span></Button>
                                    <FormControlLabel
                                        control={<GrayCheckbox
                                            checked={state.checkedG}
                                            onChange={handleChange}
                                            name="checkedG" />
                                        }
                                        label={
                                            <Typography>Recordarme &nbsp; &nbsp; ¿Olvidaste la contraseña? <Link onClick={handleView}>Recuperar contraseña</Link></Typography>
                                        } />
                                </>
                                :
                                <>
                                    <Typography className={classes.spacingItems} align="left">Recuperar contraseña</Typography>
                                    <Typography className={classes.spacingItems} align="left">Si ha olvidado su contraseña, por favor proporcione el correo con el que esta registrado. En breve le llegará un correo con una liga para resetear la contraseña.</Typography>
                                    <TextField fullWidth id="recoverMail" label="Correo" />
                                    <Button variant="contained" className={classes.marginButton} onClick={handleView}><span style={{color:'#fff'}}>Enviar correo</span></Button>
                                </>
                        }
                    </Box>
                </Grid>
            </Grid>
        </div>
    )
}