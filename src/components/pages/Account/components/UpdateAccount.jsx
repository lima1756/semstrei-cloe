import React from 'react';
import { Box, Button, Card, CardContent, Dialog, makeStyles, TextField, Typography } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    updateCard: {
        width: 500,
    },
    controlsAccount: {
        display: 'flex',
        alignItems: 'center',
        paddingTop: theme.spacing(5),
        paddingLeft: theme.spacing(1),
        paddingBottom: theme.spacing(1),
        position: 'relative',
    },
    textfieldSize: {
        width: '90%'
    },
}));

export default function UpdateAccount({ handleClose, handleUpdateClick, open }) {
    const classes = useStyles();

    return (
        <div>
            <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
                <Card className={classes.updateCard}>
                    <div>
                        <CardContent>
                            <Typography component="h5" variant="h5" align='left'>
                                Actualiza tus Datos
                            </Typography>
                            <form noValidate autoComplete="off">
                                <TextField className={classes.textfieldSize} id="name" label="Nombre" />
                                <TextField className={classes.textfieldSize} id="mail" label="Correo" />
                                <TextField className={classes.textfieldSize} id="phone" label="Telefono" />
                            </form>
                            <Box className={classes.controlsAccount}>
                                <Button
                                    variant="outlined"
                                    style={{ margin: 'auto' }}
                                    onClick={handleUpdateClick}>
                                    <span style={{ color: '#000000' }}> Actualizar Información </span>
                                </Button>
                            </Box>
                        </CardContent>
                    </div>
                </Card>
            </Dialog>
        </div>
    )
}
