import React, { useEffect, useState } from 'react';
import {
    Avatar, Button, Checkbox, Grid, IconButton, InputBase, makeStyles, Paper, Table, TableBody, 
    TableCell, TableContainer, TablePagination, TableRow, Typography
} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import Dialog from './NewUser';
import Drawer from '../AppBarDrawer/Drawer';
import { useSelector } from 'react-redux';
import { useSnackbar } from 'notistack';
import TableHeader from './components/TableHeader';
import TableHeadToolbar from './components/TableHeadToolbar';
import axios from 'axios';
import https from 'https';

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
});
axios.defaults.options = httpsAgent;

function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
        return -1;
    }
    if (b[orderBy] > a[orderBy]) {
        return 1;
    }
    return 0;
}

function getComparator(order, orderBy) {
    return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
        const order = comparator(a[0], b[0]);
        if (order !== 0) return order;
        return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
}

const useStyles = makeStyles((theme) => ({
    root: {
        marginLeft: 280,
        marginTop:70,
    },
    paper: {
        width: '95%',
    },
    table: {
        minWidth: 750,
    },
    rootSearch: {
        padding: '2px 4px',
        display: 'flex',
        alignItems: 'center',
        width: 400,
    },
    input: {
        marginLeft: theme.spacing(1),
        flex: 1,
    },
    iconButton: {
        padding: 10,
    },
    selected: { 
        '&$selected': {
            backgroundColor: "#E7E7E7",
        },
    },
    hover: {
        "&$selected:hover": {
          backgroundColor: "#F1F1F1",
        },
      },
}));

export default function EnhancedTable() {
    const classes = useStyles();
    const [order, setOrder] = useState('asc');
    const [orderBy, setOrderBy] = useState('email');
    const [selected, setSelected] = useState([]);
    const [userId, setUserId] = useState([]);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [open, setOpen] = useState(false);
    const [users, setUsers] = useState([]);
    const isLogged = useSelector(state => state.logged);
    const { enqueueSnackbar } = useSnackbar();

    const getUsers = () => {
        axios.get('https://150.136.172.48/api/user/all',{
            headers: {
                'Authorization': `Bearer ${isLogged.token}`
              }
        })
        .then(function(response){
          setUsers(response.data.data);
          //console.log('Response: ',response);
        }).catch(function(error){
            handleErrorLoadingUsers('error');
            //console.log(error);
        })
      };
    
      // eslint-disable-next-line
      useEffect (() =>{ getUsers() }, []);

    const handleRequestSort = (event, property) => {
        const isAsc = orderBy === property && order === 'asc';
        setOrder(isAsc ? 'desc' : 'asc');
        setOrderBy(property);
    };

    const handleSelectAllClick = (event) => {
        if (event.target.checked) {
            const newSelecteds = users.map((n) => n.email);
            setSelected(newSelecteds);
            return;
        }
        setSelected([]);
    };

    const handleClick = (event, name, id) => {
        const selectedIndex = selected.indexOf(name);
        const selectedIdIndex = userId.indexOf(id);
        let newSelected = [];
        let idSelected = []

        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, name);
            idSelected = idSelected.concat(userId, id);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
            idSelected = idSelected.concat(userId.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
            idSelected = idSelected.concat(userId.slice(0,-1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
            idSelected = idSelected.concat(
                userId.slice(0, selectedIdIndex),
                userId.slice(selectedIdIndex + 1),
            );
        }

        setSelected(newSelected);
        setUserId(idSelected);        
    };

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const handleClickOpen = () => {
        setOpen(true);
      };
    
      const handleClose = () => {
        getUsers();
        setOpen(false);
      };

      const handleUsersUpdate = () => {
        getUsers();
      };
    
    //-----------------------Snackbar de Error-------------------------
    const handleErrorLoadingUsers = (variant) => { enqueueSnackbar('Ocurrió un error al cargar los usuarios.', {variant}) };

    const isSelected = (name) => selected.indexOf(name) !== -1;

    const emptyRows = rowsPerPage - Math.min(rowsPerPage, users.length - page * rowsPerPage);

    return (
        <div className={classes.root}>
            <Drawer index={1}/>
            <Grid container style={{ marginBottom: 20 }}>
                <Grid item xs={6}>
                    <Paper component="form" className={classes.rootSearch} >
                        <InputBase
                            className={classes.input}
                            placeholder="Buscar Usuario"
                            inputProps={{ 'aria-label': 'search users' }}
                        />
                        <IconButton type="submit" className={classes.iconButton} aria-label="search">
                            <SearchIcon />
                        </IconButton>
                    </Paper>
                </Grid>
                <Grid item xs={6}>
                    <Button variant="contained" style={{ position: 'absolute', background:'#000' }} onClick={handleClickOpen}><span style={{color:'#fff'}}>Agregar Usuario</span></Button>
                    <Dialog open={open} handleClose={handleClose}/> 
                </Grid>
            </Grid>
            <Paper className={classes.paper}>
                <TableHeadToolbar numSelected={selected.length} style={{ marginTop: 45 }} usersId={userId} handleUsersUpdate={handleUsersUpdate}/>
                <TableContainer>
                    <Table
                        className={classes.table}
                        aria-labelledby="tableTitle"
                        size={'medium'}
                        aria-label="enhanced table"
                    >
                        <TableHeader
                            classes={classes}
                            numSelected={selected.length}
                            order={order}
                            orderBy={orderBy}
                            onSelectAllClick={handleSelectAllClick}
                            onRequestSort={handleRequestSort}
                            rowCount={users.length}
                        />
                        <TableBody>
                            {stableSort(users, getComparator(order, orderBy))
                                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                                .map((row, index) => {
                                    const isItemSelected = isSelected(row.email);
                                    const labelId = `enhanced-table-checkbox-${index}`;

                                    return (
                                        <TableRow
                                            hover
                                            onClick={(event) => handleClick(event, row.email, row.user_id)}
                                            role="checkbox"
                                            aria-checked={isItemSelected}
                                            tabIndex={-1}
                                            key={row.email}
                                            selected={isItemSelected}
                                            classes={{
                                                selected: classes.selected, hover: classes.hover,
                                            }}
                                        >
                                            <TableCell padding="checkbox">
                                                <Checkbox
                                                    color='default'
                                                    checked={isItemSelected}
                                                    inputProps={{ 'aria-labelledby': labelId }}
                                                />
                                            </TableCell>
                                            <TableCell component="th" id={labelId} scope="row" padding="none">
                                                <div style={{textAlign:'center', display:'flex'}}>
                                                    <Avatar alt="Remy Sharp" src={row.image} />
                                                    <Typography style={{textAlign:'center', verticalAlign:'middle', lineHeight:3, paddingLeft:10}}>{row.name}</Typography>
                                                </div>
                                            </TableCell>
                                            <TableCell align="right">{row.email}</TableCell>
                                            <TableCell align="right">{row.role === 0 ? 'Administrador' : row.role === 1 ? 'TI' : 'Finanzas'}</TableCell>
                                            <TableCell align="right">{row.phone_number}</TableCell>
                                            <TableCell align="right">{row.registration_date.substring(0,17)}</TableCell>
                                        </TableRow>
                                    );
                                })}
                            {emptyRows > 0 && (
                                <TableRow style={{ height: (53) * emptyRows }}>
                                    <TableCell colSpan={6} />
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
                <TablePagination
                    rowsPerPageOptions={[10, 25]}
                    component="div"
                    count={users.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onChangePage={handleChangePage}
                    onChangeRowsPerPage={handleChangeRowsPerPage}
                />
            </Paper>
        </div>
    );
}
