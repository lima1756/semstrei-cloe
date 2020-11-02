import React from 'react';
import {Button, makeStyles, TextField, Typography} from '@material-ui/core';

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

export default function RecoverPassword({ handleMailSend }) {
    const classes = useStyles();

    return (
        <>
            <Typography className={classes.spacingItems} align="left">Recuperar contraseña</Typography>
            <Typography className={classes.spacingItems} align="left">Si ha olvidado su contraseña, por favor proporcione el correo con el que esta registrado. En breve le llegará un correo con una liga para resetear la contraseña.</Typography>
            <TextField fullWidth id="recoverMail" label="Correo" />
            <Button variant="contained" className={classes.marginButton} onClick={handleMailSend}><span style={{ color: '#fff' }}>Enviar correo</span></Button>
        </>
    )
}