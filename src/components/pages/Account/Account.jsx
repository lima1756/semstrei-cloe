import React, { useState } from 'react';
import { Avatar, Box, Card, CardContent, Divider, Grid, IconButton, Tooltip, Typography } from '@material-ui/core';
import { makeStyles, } from '@material-ui/core/styles';
import Drawer from '../AppBarDrawer/Drawer';
import { useSnackbar } from 'notistack';
import axios from 'axios';
import https from 'https';
import { useSelector, useDispatch } from 'react-redux';
import { userinformation } from '../../../redux/actions';
import EditRoundedIcon from '@material-ui/icons/EditRounded';
import UpdateAccount from './components/UpdateAccount'

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
  controls: {
    display: 'flex',
    alignItems: 'center',
    paddingTop: theme.spacing(2),
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(4),
  },
  large: {
    width: theme.spacing(20),
    height: theme.spacing(20),
  },
  infoPad: {
    paddingTop: theme.spacing(2),
  },
  center: {
    marginLeft: 'auto',
    marginRight: 'auto',
  }
}));

export default function MediaControlCard() {
  const classes = useStyles();
  const { enqueueSnackbar } = useSnackbar();
  const isLogged = useSelector(state => state.logged);
  const user = useSelector(state => state.user);
  const dispatch = useDispatch();
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const updateInfo = (name, mail, phone) => {
    axios.put(`https://150.136.172.48/api/user`, {
      email: mail === '' ? null : mail,
      name: name === '' ? null : name,
      phone_number: phone === '' ? null : phone
    }, {
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
    let name = document.getElementById('name').value;
    let mail = document.getElementById('mail').value;
    let phone = document.getElementById('phone').value;

    if (name !== '' || mail !== '' || phone !== '') {
      updateInfo(name, mail, phone);
    }
    handleClose();
  };

  // -----------------------Snackbar de update-------------------------
  const handleSuccessUpdate = (variant) => { enqueueSnackbar('La información se actualizó correctamente.', { variant }) };

  // -----------------------Snackbar de Error-------------------------
  const handleErrorUpdate = (variant) => { enqueueSnackbar('No se pudo actualizar la información, intente más tarde.', { variant }) };

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
                  <Tooltip title='Editar información' >
                    <IconButton aria-label="delete" onClick={handleClickOpen} className={classes.center}>
                      <EditRoundedIcon />
                    </IconButton>
                  </Tooltip>
                  <UpdateAccount handleClose={handleClose} handleUpdateClick={handleUpdateClick} open={open} />
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
      </Grid>
    </div>
  );
}