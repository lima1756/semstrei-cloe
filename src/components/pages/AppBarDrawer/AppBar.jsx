import React from 'react';
import {
  AppBar, Button, Toolbar, Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { userinformation, signin } from '../../../redux/actions';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
//import logo from '../assets/cloeLogo.webp';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  title: {
    flexGrow: 1,
  },
}));

export default function ElevateAppBar(props) {
  const classes = useStyles();
  const history = useHistory();
  const isLogged = useSelector(state => state.logged);
  const dispatch = useDispatch();

  const handleCloseAccount = () => {
    axios.post('https://150.136.172.48/api/auth/logout', {}, {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
    dispatch(signin(false, ''));
    dispatch(userinformation(false, false, '', '', '', -1, -1));
    history.push('/login');
  };

  return (
    <div className={classes.root}>
      <AppBar position="static" style={{ background: '#000' }}>
        <Toolbar>
          <Typography className={classes.title} variant="h6" align='left'>
            Cloe
            </Typography>
          {
            isLogged.logged ?
              <Button color="inherit" variant='outlined' onClick={handleCloseAccount}>Cerrar sesión</Button>
              :
              null
          }
        </Toolbar>
      </AppBar>
    </div>
  );
}
