import React, { useState } from 'react';
import {
  Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle,
  FormLabel, FormControl, FormControlLabel, Grid, makeStyles, Radio, RadioGroup, TextField, Tooltip
} from '@material-ui/core';
import axios from 'axios';
import https from 'https';
import { useSnackbar } from 'notistack';
import { useSelector } from 'react-redux';
import Handle401 from '../../../utils/Handle401';

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent;

const useStyles = makeStyles((theme) => ({
  customWidth: {
    maxWidth: 150,
  },
}));

export default function AlertDialog({ open, handleClose }) {
  const [value, setValueR] = useState('');
  const { enqueueSnackbar } = useSnackbar();
  const isLogged = useSelector(state => state.logged);
  const classes = useStyles();

  const handleChange = (event) => {
    setValueR(event.target.value);
  };

  const createUser = () => {
    registerUser(document.getElementById("name").value, document.getElementById("mail").value, value);
    setValueR('');
    handleClose();
  };

  const registerUser = (name, mail, role) => {
    axios.post('https://150.136.172.48/api/user', {
      email: mail,
      name: name,
      role: role === 'admin' ? 0 : role === 'tech' ? 1 : 2
    }, {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    }).then(function (response) {
      handleUserCreated('success');
    }).catch((r) => Handle401(r, () => handleUserError('error')))
  };

  // --------------------------- Snackbar success User Added ---------------------- 
  const handleUserCreated = (variant) => { enqueueSnackbar('El usuario se agregó correctamente.', { variant }) };

  // --------------------------- Snackbar error adding User ---------------------- 
  const handleUserError = (variant) => { enqueueSnackbar('Ocurrió un error al agregar el usuario.', { variant }) };

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description">
        <DialogTitle id="alert-dialog-title">{"Agregar nuevo usuario"}</DialogTitle>
        <DialogContent>
          <TextField fullWidth id="name" label="Nombre" />
          <TextField fullWidth id="mail" label="Correo" />
          <DialogContentText id="alert-dialog-description" >
            <FormControl component="fieldset" id="radioOptions">
              <FormLabel component="legend" style={{ paddingTop: 25, paddingBottom: 15 }}>Rol</FormLabel>
              <RadioGroup aria-label="gender" name="gender1" value={value} onChange={handleChange}>
                <Grid container spacing={3}>
                  <Grid item xs={6}>
                    <Tooltip classes={{ tooltip: classes.customWidth }} title='Usuario con poder de crear, modificar y eliminar usuarios' arrow>
                      <FormControlLabel value="admin" control={<Radio color="default" />} label="Administrador" />
                    </Tooltip>
                    <Tooltip classes={{ tooltip: classes.customWidth }} title='Usuario de IT, solo podrá consultar las tablas' arrow>
                      <FormControlLabel value="tech" control={<Radio color="default" />} label="IT" />
                    </Tooltip>
                  </Grid>
                  <Grid item xs={5}>
                    <Tooltip classes={{ tooltip: classes.customWidth }} title='Usuario de finanzas, solo podrá consultar las tablas' arrow>
                      <FormControlLabel value="finance" control={<Radio color="default" />} label="Finanzas" />
                    </Tooltip>
                  </Grid>
                </Grid>
              </RadioGroup>
            </FormControl>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={createUser} variant="outlined">
            Agregar
          </Button>
          <Button onClick={handleClose} variant="outlined" autoFocus>
            Cancelar
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
