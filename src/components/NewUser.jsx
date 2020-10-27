import React from 'react';
import {
  Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, 
  FormLabel, FormControl, FormControlLabel, Grid, Radio, RadioGroup, TextField,
} from '@material-ui/core';

export default function AlertDialog({ open, handleClose }) {
  const [value, setValue] = React.useState('female');

  const handleChange = (event) => {
    setValue(event.target.value);
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
          <TextField fullWidth id="standard-required" label="Correo"/>
          <DialogContentText id="alert-dialog-description" >
            <FormControl component="fieldset">
              <FormLabel component="legend" style={{paddingTop:25,paddingBottom:15}}>Rol</FormLabel>
              <RadioGroup aria-label="gender" name="gender1" value={value} onChange={handleChange}>
                <Grid container spacing={3}>
                  <Grid item xs={6}>
                    <FormControlLabel value="admin" control={<Radio />} label="Administrador" />
                    <FormControlLabel value="tech" control={<Radio />} label="IT" />
                  </Grid>
                  <Grid item xs={5}>
                    <FormControlLabel value="finance" control={<Radio />} label="Finanzas" />
                    <FormControlLabel value="hr" control={<Radio />} label="HR" />
                  </Grid>
                </Grid>
              </RadioGroup>
            </FormControl>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} variant="outlined">
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
