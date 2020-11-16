import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Link, } from 'react-router-dom';
import {
  AppBar, Avatar, Box, Collapse, CssBaseline, Divider, Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography
} from '@material-ui/core';
import { useSelector, useDispatch } from 'react-redux';
import { isopen } from '../../../redux/actions';
import EqualizerRoundedIcon from '@material-ui/icons/EqualizerRounded';
import GroupRoundedIcon from '@material-ui/icons/GroupRounded';
import AccountCircleRoundedIcon from '@material-ui/icons/AccountCircleRounded';
import Bar from './AppBar';
import DashboardRoundedIcon from '@material-ui/icons/DashboardRounded';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import TableChartRoundedIcon from '@material-ui/icons/TableChartRounded';

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
  nested: {
    paddingLeft: theme.spacing(4),
  },
}));

export default function ClippedDrawer() {
  const classes = useStyles();
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const user = useSelector(state => state.user);
  const openDrawer = useSelector(state => state.openDrawer);
  const [open, setOpen] = useState(true);
  const dispatch = useDispatch();

  const handleClick = () => {
    setOpen(!open);
    dispatch(isopen(!openDrawer.menuDrawer));
  };

  useEffect(() => {
    if (window.location.pathname === '/dashboard/resultTables') {
      setSelectedIndex(0);
    } else if (window.location.pathname === '/users') {
      setSelectedIndex(1);
    } else if(window.location.pathname === '/account') {
      setSelectedIndex(2);
    }else if(window.location.pathname === '/dashboard/graphs'){
      setSelectedIndex(3);
    }else if(window.location.pathname === '/dashboard/controlTables'){
      setSelectedIndex(4);
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
            onClick={handleClick}>
              <ListItemIcon>
                <DashboardRoundedIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
              {openDrawer.menuDrawer ? <ExpandLess /> : <ExpandMore />}
            </ListItem>
            <Collapse in={openDrawer.menuDrawer} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                <ListItem 
                button 
                className={classes.nested}
                selected={selectedIndex === 0}
                component={Link}
                to={'/dashboard/resultTables'}>
                  <ListItemIcon>
                    <TableChartRoundedIcon />
                  </ListItemIcon>
                  <ListItemText primary="Tbls. de resultado" />
                </ListItem>
                <ListItem 
                button 
                className={classes.nested}
                selected={selectedIndex === 3}
                component={Link}
                to={'/dashboard/graphs'}>
                  <ListItemIcon>
                    <EqualizerRoundedIcon />
                  </ListItemIcon>
                  <ListItemText primary="Graficas" />
                </ListItem>
                <ListItem 
                button 
                className={classes.nested}
                selected={selectedIndex === 4}
                component={Link}
                to={'/dashboard/controlTables'}>
                  <ListItemIcon>
                    <TableChartRoundedIcon />
                  </ListItemIcon>
                  <ListItemText primary="Tbls. de control" />
                </ListItem>
              </List>
            </Collapse>
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
              <ListItemText primary="Mi cuenta" />
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
