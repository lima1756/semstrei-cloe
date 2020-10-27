import React from 'react';
import { Avatar, Box, Button, Card, CardContent, Divider, Grid, TextField, Typography } from '@material-ui/core';
import { makeStyles, } from '@material-ui/core/styles';
import Drawer from './Drawer';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    marginLeft: 280,
    marginTop: 70,
    width: '60%',
    minHeight: 300,
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
  },
  content: {
    flex: '1 0 auto',
  },
  cover: {
    width: 151,
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
  },
  playIcon: {
    height: 38,
    width: 38,
  },
  large: {
    width: theme.spacing(20),
    height: theme.spacing(20),
  },
  textfieldSize: {
    width: '90%'
  },
  cardAccount: {
    display: 'flex',
    marginTop: 70,
    width: '60%',
    minHeight: 300,
  },
  infoPad: {
    paddingTop: theme.spacing(2),
  },
}));

export default function MediaControlCard() {
  const classes = useStyles();

  return (
    <div>
      <Drawer index={2} />
      <Grid container >
        <Grid item xs={6}>
          <Card className={classes.root}>
            <div className={classes.details}>
              <CardContent className={classes.content}>
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
              <Divider variant='middle' />
              <Box className={classes.controls}>
                <Button variant="outlined" style={{ margin: 'auto' }}>Subir Foto</Button>
              </Box>
            </div>
            <CardContent>
              <Avatar alt="Remy Sharp" src='https://picsum.photos/200/300?random=3' className={classes.large} style={{ margin: 'auto' }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6}>
          <Card className={classes.cardAccount}>
            <div className={classes.details}>
              <CardContent className={classes.content}>
                <Typography component="h5" variant="h5" align='left'>
                  Perfil
                </Typography>
                <form noValidate autoComplete="off">
                  <TextField className={classes.textfieldSize} id="name" label="Nombre" />
                  <TextField className={classes.textfieldSize} id="mail" label="Correo" />
                  <TextField className={classes.textfieldSize} id="phone" label="Telefono" />
                </form>
                <Box className={classes.controlsAccount}>
                  <Button variant="outlined" style={{ margin: 'auto' }}>Subir Foto</Button>
                </Box>
              </CardContent>
            </div>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}
