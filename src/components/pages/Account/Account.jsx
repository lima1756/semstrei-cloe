import React, { useState, useEffect } from 'react';
import { Avatar, Box, Button, Card, CardContent, Divider, Grid, TextField, Typography } from '@material-ui/core';
import { makeStyles, } from '@material-ui/core/styles';
import Drawer from '../AppBarDrawer/Drawer';
import { useSnackbar } from 'notistack';
import axios from 'axios';
import https from 'https';
import { useSelector, useDispatch } from 'react-redux';
import { userinformation } from '../../../redux/actions';

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent;

const useStyles = makeStyles((theme) => ({
  infoCard: {
    display: 'flex',
    width: 500,
    minHeight: 280,
  },
  updateCard: {
    width: 500,
  },
  controls: {
    display: 'flex',
    alignItems: 'center',
    paddingTop: theme.spacing(2),
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(4),
  },
  controlsAccount: {
    display: 'flex',
    alignItems: 'center',
    paddingTop: theme.spacing(5),
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(1),
    position: 'relative',
  },
  large: {
    width: theme.spacing(20),
    height: theme.spacing(20),
  },
  textfieldSize: {
    width: '90%'
  },
  infoPad: {
    paddingTop: theme.spacing(2),
  },
}));

export default function MediaControlCard() {
  const classes = useStyles();
  const [loading, setLoading] = useState(false);
  const { enqueueSnackbar } = useSnackbar();
  const timer = React.useRef();
  const isLogged = useSelector(state => state.logged);
  const user = useSelector(state => state.user);
  const dispatch = useDispatch();

  useEffect(() => {
    return () => {
      clearTimeout(timer.current);
    };
  }, []);

  const updateInfo = (name, mail, phone) => {
    axios.put(`https://150.136.172.48/api/user`, {
      email: mail === '' ? null : mail,
      name: name === '' ? null : name,
      phone_number: phone === '' ? null : phone
    },{
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    }).then(function (response) {
      dispatch(userinformation(user.admin, user.newUser, name === '' ? user.name : name, mail === '' ? user.mail : mail, phone === '' ? user.phone : phone, user.role, user.userId));
      document.getElementById('name').value = null;
      document.getElementById('mail').value = null;
      document.getElementById('phone').value = null;
      handleSuccessUpdate('success');
    }).catch(function (error) {
      handleErrorUpdate('error');
    })
  };

  const handleUpdateClick = () => {
    updateInfo(document.getElementById('name').value, document.getElementById('mail').value, document.getElementById('phone').value);

    if (!loading) {
      setLoading(true);
      timer.current = window.setTimeout(() => {
        setLoading(false);
      }, 2000);
    }
  };

// -----------------------Snackbar de update-------------------------
const handleSuccessUpdate = (variant) => { enqueueSnackbar('La información se actualizó correctamente.', {variant}) };

// -----------------------Snackbar de Error-------------------------
const handleErrorUpdate = (variant) => { enqueueSnackbar('No se pudo actualizar la información, intente más tarde.', {variant}) };

  return (
    <div>
      <Drawer index={2} />
      <Grid container style={{ marginTop: 50, paddingLeft: 280, }} >
        <Grid item xs={12} sm={7} style={{ marginTop: 20 }}>
          <Card className={classes.infoCard}>
            <Grid container spacing={4}>
              <Grid item xs={6}>
                <CardContent>
                  <Typography component="h5" variant="h5">
                    {user.name}
                </Typography>
                  <Typography variant="subtitle1" color="textSecondary" className={classes.infoPad}>
                    {user.mail}
                </Typography>
                  <Typography variant="subtitle1" color="textSecondary" className={classes.infoPad}>
                    {user.phone}
                </Typography>
                </CardContent>
                <Divider variant='middle' style={{ marginTop: 20 }} />
                <Box className={classes.controls}>
                  <Button variant="outlined" style={{ margin: 'auto' }}>Subir Foto</Button>
                </Box>
              </Grid>
              <Grid item xs={5}>
                <CardContent>
                  <Avatar src='https://picsum.photos/200/300?random=3' className={classes.large} />
                </CardContent>
              </Grid>
            </Grid>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} style={{ marginTop: 20, }} >
          <Card className={classes.updateCard}>
            <div>
              <CardContent>
                <Typography component="h5" variant="h5" align='left'>
                  Perfil
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
                    disabled={loading}
                    onClick={handleUpdateClick}>
                    <span style={{ color: '#000000' }}> Actualizar Información </span>
                  </Button>
                </Box>
              </CardContent>
            </div>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}
