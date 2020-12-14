import React from 'react';
import {
    IconButton, lighten, makeStyles, Toolbar, Tooltip, Typography
} from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit'
import BlockIcon from '@material-ui/icons/Block'
import CheckCircleIcon from '@material-ui/icons/CheckCircle'
import clsx from 'clsx';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { useSnackbar } from 'notistack';
import Handle401 from '../../../../utils/Handle401';
import { useHistory } from 'react-router-dom';
import { useDispatch } from 'react-redux'

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
    const { numSelected, usersId, handleUserUpdate, updateUserDialog } = props;
    const isLogged = useSelector(state => state.logged);
    const { enqueueSnackbar } = useSnackbar();
    const history = useHistory();
    const dispatch = useDispatch();

    const handleDelete = () => {
        axios.delete('https://150.136.172.48/api/user', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${isLogged.token}`,
            },
            data: {
                users: usersId,
            }
        }).then(function (response) {
            handleUserDelete('success');
            handleUserUpdate();
        }).catch((r) => Handle401(r, history, dispatch, () => handleUserDeleteError('error')))
    };

    const handleEnable = () => {
        axios.put('https://150.136.172.48/api/user/enable', {
            users: usersId,
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${isLogged.token}`,
            }
        }).then(function (response) {
            handleUserEnable('success');
            handleUserUpdate();
        }).catch((r) => Handle401(r, history, dispatch, () => handleUserEnableError('error')))
    };

    const handleDisable = () => {
        axios.put('https://150.136.172.48/api/user/disable', {
            users: usersId,
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${isLogged.token}`,
            }
        }).then(function (response) {
            handleUserDisable('success');
            handleUserUpdate();
        }).catch((r) => Handle401(r, history, dispatch, () => handleUserDisableError('error')))
    };

    // --------------------------- Snackbar success User Added ---------------------- 
    const handleUserDelete = (variant) => { enqueueSnackbar('El usuario se eliminó correctamente.', { variant }) };

    const handleUserEnable = (variant) => { enqueueSnackbar('El usuario se activo correctamente.', { variant }) };

    const handleUserDisable = (variant) => { enqueueSnackbar('El usuario se desactivo correctamente.', { variant }) };

    // --------------------------- Snackbar error adding User ---------------------- 
    const handleUserDeleteError = (variant) => { enqueueSnackbar('Ocurrió un error al eliminar el usuario.', { variant }) };

    const handleUserEnableError = (variant) => { enqueueSnackbar('Ocurrió un error al activar el usuario.', { variant }) };

    const handleUserDisableError = (variant) => { enqueueSnackbar('Ocurrió un error al desactivar el usuario.', { variant }) };

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

            {numSelected > 0 &&
                <>
                    <Tooltip title={numSelected > 1 ? 'Eliminar usuarios' : 'Eliminar usuario'}>
                        <IconButton aria-label="delete" onClick={handleDelete}>
                            <DeleteIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title={numSelected > 1 ? 'Deshabilitar usuarios' : 'Deshabilitar usuario'}>
                        <IconButton aria-label="delete" onClick={handleDisable}>
                            <BlockIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title={numSelected > 1 ? 'Habilitar usuarios' : 'Habilitar usuario'}>
                        <IconButton aria-label="delete" onClick={handleEnable}>
                            <CheckCircleIcon />
                        </IconButton>
                    </Tooltip>
                </>
            }
            {numSelected === 1 &&
                <Tooltip title='Editar usuario'>
                    <IconButton aria-label="delete" onClick={updateUserDialog}>
                        <EditIcon />
                    </IconButton>
                </Tooltip>
            }
        </Toolbar>
    );
};