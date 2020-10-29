import React, { useEffect} from 'react';
import {
  Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, 
  FormLabel, FormControl, FormControlLabel, Grid, Radio, RadioGroup, TextField,
} from '@material-ui/core';

import axios from 'axios';
import https from 'https'

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent
axios.defaults.headers.common['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDY1MTAyMDAsImlhdCI6MTYwMzkxODIwMCwiaWQiOjF9.ucki8xqRxG9MWLsCu43fszERFSB2x7vuqNyIlHXTsr0';

export default function AlertDialog({ open, handleClose }) {
  const [value, setValueR] = React.useState('');

  const handleChange = (event) => {
    setValueR(event.target.value);
  };

  const handleUserCreation = () => {
    registerUser(document.getElementById("name").value, document.getElementById("mail").value, value);
    setValueR('');
    handleClose();
  };

  const registerUser = (name, mail, role) => {
    axios.post('https://150.136.172.48/api/user', { 
      email: mail, 
      name: name,
      role: role == 'admin' ? 0 : role == 'tech' ? 1 : 2
    }).then(function(response){
      console.log(response);
    }).catch(function(error){
      console.log(error);
    })
  };

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Agregar nuevo usuario"}</DialogTitle>
        <DialogContent>
          <TextField fullWidth id="name" label="Nombre"/>
          <TextField fullWidth id="mail" label="Correo"/>
          <DialogContentText id="alert-dialog-description" >
            <FormControl component="fieldset" id="radioOptions">
              <FormLabel component="legend" style={{paddingTop:25,paddingBottom:15}}>Rol</FormLabel>
              <RadioGroup aria-label="gender" name="gender1" value={value} onChange={handleChange}>
                <Grid container spacing={3}>
                  <Grid item xs={6}>
                    <FormControlLabel value="admin" control={<Radio color="default"/>} label="Administrador" />
                    <FormControlLabel value="tech" control={<Radio color="default"/>} label="IT" />
                  </Grid>
                  <Grid item xs={5}>
                    <FormControlLabel value="finance" control={<Radio color="default"/>} label="Finanzas" />
                    <FormControlLabel value="hr" control={<Radio color="default" />} label="HR" />
                  </Grid>
                </Grid>
              </RadioGroup>
            </FormControl>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleUserCreation} variant="outlined">
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
