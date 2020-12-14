import React from 'react';
import {
  Button, Dialog, DialogActions, DialogContent, DialogTitle, FormLabel,
  FormControl, FormControlLabel, Grid, makeStyles, Radio, RadioGroup, TextField, Tooltip
} from '@material-ui/core';
import axios from 'axios';
import https from 'https';
import { useSnackbar } from 'notistack';
import { useSelector } from 'react-redux';
import Handle401 from '../../../../utils/Handle401';
import { useHistory } from 'react-router-dom';
import { useDispatch } from 'react-redux'

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent;

const useStyles = makeStyles((theme) => ({
  customWidth: {
    maxWidth: 150,
  },
}));

export default function UpdateUserDialog({ user, open, handleClose }) {
  const { enqueueSnackbar } = useSnackbar();
  const isLogged = useSelector(state => state.logged);
  const classes = useStyles();
  const history = useHistory();
  const dispatch = useDispatch();

  const recoverPassword = () => {
    axios.get('https://150.136.172.48/api/recover/request?email=' + user.email)
      .then(function (response) {
        handleEmailSent('success');
      }).catch((r) => Handle401(r, history, dispatch, () => handleEmailError('error')))
    handleClose();
  }

  const updateUser = () => {
    axios.put('https://150.136.172.48/api/user/' + user.user_id, {
      email: document.getElementById("emailUpdate").value,
      phone_number: document.getElementById("phoneUpdate").value,
      name: document.getElementById("nameUpdate").value,
      role: parseInt(document.querySelector('input[name="role"]:checked').value)
    }, {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    }).then(function (response) {
      handleUserUpdated('success');
    }).catch((r) => Handle401(r, history, dispatch, () => handleUserError('error')))
    handleClose();
  };

  // --------------------------- Snackbar success User Added ---------------------- 
  const handleUserUpdated = (variant) => { enqueueSnackbar('El usuario se actualizo correctamente.', { variant }) };

  const handleEmailSent = (variant) => { enqueueSnackbar('Se envio correo a: ' + user.email, { variant }) };

  // --------------------------- Snackbar error adding User ---------------------- 
  const handleUserError = (variant) => { enqueueSnackbar('Ocurrió un error al actualizar el usuario.', { variant }) };

  const handleEmailError = (variant) => { enqueueSnackbar('Hubo un error al enviar correo a: ' + user.email, { variant }) };

  if (user === null) {
    return null
  }
  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description">
        <DialogTitle id="alert-dialog-title">{"Actualizar usuario"}</DialogTitle>
        <DialogContent>
          <TextField fullWidth id="nameUpdate" label="Nombre" defaultValue={user.name} />
          <TextField fullWidth id="emailUpdate" label="Correo" defaultValue={user.email} />
          <TextField fullWidth id="phoneUpdate" label="Telefono" defaultValue={user.phone_number} />
          <FormControl component="fieldset" id="radioOptions">
            <FormLabel component="legend" style={{ paddingTop: 25, paddingBottom: 15 }}>Rol</FormLabel>
            <RadioGroup aria-label="Role" name="role" defaultValue={"" + user.role} >
              <Grid container spacing={3}>
                <Grid item xs={6}>
                  <Tooltip classes={{ tooltip: classes.customWidth }} title='Usuario con poder de crear, modificar y eliminar usuarios' arrow>
                    <FormControlLabel value='0' control={<Radio color="default" />} label="Administrador" />
                  </Tooltip>
                  <Tooltip classes={{ tooltip: classes.customWidth }} title='Usuario de IT, solo podrá consultar las tablas' arrow>
                    <FormControlLabel value='1' control={<Radio color="default" />} label="IT" />
                  </Tooltip>
                </Grid>
                <Grid item xs={5}>
                  <Tooltip classes={{ tooltip: classes.customWidth }} title='Usuario de finanzas, solo podrá consultar las tablas' arrow>
                    <FormControlLabel value='2' control={<Radio color="default" />} label="Finanzas" />
                  </Tooltip>
                </Grid>
              </Grid>
            </RadioGroup>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={recoverPassword} variant="outlined" style={{ position: "absolute", left: "10px" }}>
            Recuperar contraseña
          </Button>
          <Button onClick={updateUser} variant="outlined">
            Actualizar
          </Button>
          <Button onClick={handleClose} variant="outlined" autoFocus>
            Cancelar
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
