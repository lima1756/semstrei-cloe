import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Link, } from 'react-router-dom';
import {
  AppBar, Avatar, Box, CssBaseline, Divider, Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography
} from '@material-ui/core';
import { useSelector } from 'react-redux';
import EqualizerRoundedIcon from '@material-ui/icons/EqualizerRounded';
import GroupRoundedIcon from '@material-ui/icons/GroupRounded';
import AccountCircleRoundedIcon from '@material-ui/icons/AccountCircleRounded';
import Bar from './AppBar';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerContainer: {
    overflow: 'auto',
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
  large: {
    width: theme.spacing(15),
    height: theme.spacing(15),
  },
  rol: {
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
  },
  topPad: {
    paddingTop: theme.spacing(2),
  },
}));

export default function ClippedDrawer() {
  const classes = useStyles();
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const user = useSelector(state => state.user);

  useEffect(() => {
    if (window.location.pathname === '/dashboard') {
      setSelectedIndex(0);
    } else if (window.location.pathname === '/users') {
      setSelectedIndex(1);
    } else {
      setSelectedIndex(2);
    }
  }, []);

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar position="fixed" className={classes.appBar}>
        <Bar />
      </AppBar>
      <Drawer
        className={classes.drawer}
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <Toolbar />
        <div className={classes.drawerContainer}>
          <Box className={classes.topPad}>
            <Avatar alt="Remy Sharp" src='https://picsum.photos/200/300?random=3' className={classes.large} style={{ margin: 'auto' }} />
            <Typography className={classes.rol}>{user.role === 0 ? 'Administrador' : user.role === 1 ? 'IT' : 'Finanzas'}</Typography>
          </Box>
          <Divider variant='middle' />
          <List component="nav" aria-label="main mailbox folders">
            <ListItem
              button
              selected={selectedIndex === 0}
              component={Link}
              to={'/dashboard'}
            >
              <ListItemIcon>
                <EqualizerRoundedIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItem>
            {
              user.admin ?
                <ListItem
                  button
                  selected={selectedIndex === 1}
                  component={Link}
                  to={'/users'}
                >
                  <ListItemIcon>
                    <GroupRoundedIcon />
                  </ListItemIcon>
                  <ListItemText primary="Usuarios" />
                </ListItem>
                :
                null
            }
            <ListItem
              button
              selected={selectedIndex === 2}
              component={Link}
              to={'/account'}
            >
              <ListItemIcon>
                <AccountCircleRoundedIcon />
              </ListItemIcon>
              <ListItemText primary="Cuenta" />
            </ListItem>
          </List>
          <Divider />
        </div>
      </Drawer>
      <main className={classes.content}>
      </main>
    </div>
  );
}
