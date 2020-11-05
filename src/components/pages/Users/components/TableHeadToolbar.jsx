import React from 'react';
import {
    IconButton, lighten, makeStyles, Toolbar, Tooltip, Typography
} from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import clsx from 'clsx';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { useSnackbar } from 'notistack';

const useToolbarStyles = makeStyles((theme) => ({
    root: {
        paddingLeft: theme.spacing(2),
        paddingRight: theme.spacing(1),
    },
    highlight:
        theme.palette.type === 'light'
            ? {
                color: theme.palette.secondary.main,
                backgroundColor: lighten(theme.palette.secondary.light, 0.85),
            }
            : {
                color: theme.palette.text.primary,
                backgroundColor: theme.palette.secondary.dark,
            },
    title: {
        flex: '1 1 100%',
    },
}));

export default function EnhancedTableToolbar(props) {
    const classes = useToolbarStyles();
    const { numSelected, usersId, handleUserUpdate } = props;
    const isLogged = useSelector(state => state.logged);
    const { enqueueSnackbar } = useSnackbar();

    const handleDelete = () => {
        console.log('Token: ', isLogged.token);
        console.log('Users: ', usersId);
        axios.delete('https://150.136.172.48/api/user', {
            users: usersId,
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${isLogged.token}`,
            }
        }).then(function (response) {
            handleUserDelete('success');
            handleUserUpdate();
        }).catch(function (error) {
            handleUserDeleteError('error');
        })
        console.log(usersId);
    };

    // --------------------------- Snackbar success User Added ---------------------- 
    const handleUserDelete = (variant) => { enqueueSnackbar('El usuario se eliminó correctamente.', { variant }) };

    // --------------------------- Snackbar error adding User ---------------------- 
    const handleUserDeleteError = (variant) => { enqueueSnackbar('Ocurrió un error al eliminar el usuario.', { variant }) };

    return (
        <Toolbar
            className={clsx(classes.root, {
                [classes.highlight]: numSelected > 0,
            })}
            style={{ minHeight: 48, background: numSelected > 0 ? '#CBCBCB' : '#ffffff' }}
        >
            {numSelected > 0 ? (
                <Typography className={classes.title} variant="subtitle1" component="div" style={{ color: '#000000' }}>
                    {numSelected} selected
                </Typography>
            ) : (
                    null
                )}

            {numSelected > 0 ? (
                <Tooltip title="Delete">
                    <IconButton aria-label="delete" onClick={handleDelete}>
                        <DeleteIcon />
                    </IconButton>
                </Tooltip>
            ) : (
                    null
                )}
        </Toolbar>
    );
};