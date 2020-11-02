import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Checkbox, FormControlLabel, makeStyles, TextField, Typography} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    marginButton: {
        margin: theme.spacing(2),
        width: '50%',
        background: '#000',
    },
    spacingItems: {
        paddingBottom: theme.spacing(3),
    },
}));

export default function LoginForm({handleView, handleLogin, handleChange, state}) {
    const classes = useStyles();

    return (
        <>
            <Typography className={classes.spacingItems} align="left">Inicia sesiòn</Typography>
            <TextField fullWidth id="userEmail" label="Correo" />
            <TextField className={classes.spacingItems} fullWidth id="password" label="Password" type="password" autoComplete="current-password" />
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
        </>
    )
};