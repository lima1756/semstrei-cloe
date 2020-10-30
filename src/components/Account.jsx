import React, { useState, useEffect } from 'react';
import { Avatar, Box, Button, Card, CardContent, Divider, Grid, TextField, Typography } from '@material-ui/core';
import { makeStyles, } from '@material-ui/core/styles';
import Drawer from './Drawer';
import CircularProgress from '@material-ui/core/CircularProgress';

import axios from 'axios';
import https from 'https';
import clsx from 'clsx';
import { green } from '@material-ui/core/colors';

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
})
axios.defaults.options = httpsAgent
axios.defaults.headers.common['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDY2ODQyMTgsImlhdCI6MTYwNDA5MjIxOCwiaWQiOjIwNn0.kkXFxmFVmq1G13OLLv3jpHLXC1E8Kfn1hJL6YEM16fc';
//marginTop:70
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
  buttonSuccess: {
    backgroundColor: green[500],
    '&:hover': {
      backgroundColor: green[700],
    },
  },
  buttonProgress: {
    color: green[500],
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: 2,
    marginLeft: -12,
  },
}));

export default function MediaControlCard() {
  const classes = useStyles();
  const [update, setUpdate] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const timer = React.useRef();

  const buttonClassname = clsx({
    [classes.buttonSuccess]: success,
  });

  useEffect(() => {
    return () => {
      clearTimeout(timer.current);
    };
  }, []);

  const updateInfo = (name, mail, phone) => {
    axios.put('https://150.136.172.48/api/user/21', {
      email: mail === '' ? null : mail,
      name: name === '' ? null : name,
      phone_number: phone === '' ? null : phone
    }).then(function (response) {
      setUpdate(true);
    }).catch(function (error) {
      console.log(error);
    })
  };

  const handleUpdateClick = () => {
    updateInfo(document.getElementById('name').value, document.getElementById('mail').value, document.getElementById('phone').value);

    if (!loading) {
      setSuccess(false);
      setLoading(true);
      timer.current = window.setTimeout(() => {
        setSuccess(true);
        setLoading(false);
      }, 2000);
    }
  };

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
                    Eduardo Alonso Herrera
                </Typography>
                  <Typography variant="subtitle1" color="textSecondary" className={classes.infoPad}>
                    eduardo.alonsoh@gmail.com
                </Typography>
                  <Typography variant="subtitle1" color="textSecondary" className={classes.infoPad}>
                    Guadalajara, Mexico
                </Typography>
                  <Typography variant="subtitle1" color="textSecondary" className={classes.infoPad}>
                    (11) 1122334455
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
                    className={buttonClassname}
                    variant="outlined"
                    style={{ margin: 'auto' }}
                    disabled={loading}
                    onClick={handleUpdateClick}>
                    <span style={{ color: success ? '#ffffff' : '#000000' }}> Actualizar Información </span>
                  </Button>
                  {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
                </Box>
              </CardContent>
            </div>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}
