import React, { useState, useEffect, } from 'react';
import Drawer from '../AppBarDrawer/Drawer'
import { makeStyles } from '@material-ui/core/styles';
import { Box, FormControl, Grid, Paper, InputLabel, MenuItem, Select } from '@material-ui/core';
import ReactDataGrid from "react-data-grid";
import "./style.css";
import { useSelector, } from 'react-redux';
import axios from 'axios';
import https from 'https';

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
});
axios.defaults.options = httpsAgent;

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    width: "100%",
    paddingRight: "1.3em"
  },
}));

export default function Dashboard() {
  const isLogged = useSelector(state => state.logged);
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({ 'categoria': [], 'mercado': [], 'periodo': [], 'submarca': [], 'une': [] })
  const [dataRow, setDataRow] = useState([]);
  const [filterValues, setFilterValues] = useState({
    'categoria': '', 'mercado': '', 'periodo': '', 'submarca': '', 'une': ''
  })
  const [value, setValue] = React.useState('default');
  const classes = useStyles();

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const otb = () => {
    axios.get('https://150.136.172.48/api/otb?current_period=01-DEC-20&breakdown=False', {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
      .then(function (response) {
        setData(response.data.table);
        setDataRow(response.data.table);
      }).catch(function (error) {
        console.log(error);
      })
  };

  const getFilters = () => {
    axios.get('https://150.136.172.48/api/otb/filters', {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
      .then(function (response) {
        setFilters(response.data.filters);
        console.log(response.data.filters);
        console.log(response.data.filters.periodo[0])
        setFilterValues({ ...filterValues, 'periodo': response.data.filters.periodo[0] })

      }).catch(function (error) {
        console.log(error);
      })
  }

  useEffect(() => {
    otb();
    getFilters();
  }, []);

  const columns = [
    {
      key: 'startDateCurrentPeriodOTB',
      name: 'Periodo',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'period_length',
      name: 'Tamaño del periodo',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'startDateProjectionPeriodOTB',
      name: 'Periodo de Proyeccion',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'initialStock',
      name: 'Stock Inicial Precio Lista',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'inventoryOnStores',
      name: 'Inventario en tiendas',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
    },
    {
      key: 'purchases',
      name: 'Compras',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
    },
    {
      key: 'devolution',
      name: 'Devoluciones',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'targetSells',
      name: 'Ventas esperadas',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'targetStock',
      name: 'Stock esperado',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'projectionEomStock',
      name: 'Tgt Stock EOM',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'otb_minus_ctb',
      name: 'OTB / CTB',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'percentage_otb',
      name: 'OTB / CTB (%)',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
  ];

  const onGridRowsUpdated = ({ fromRow, toRow, updated }) => {
    this.setState(state => {
      const rows = rows.slice();
      for (let i = fromRow; i <= toRow; i++) {
        rows[i] = { ...rows[i], ...updated };
      }
      return { rows };
    });
  };

  const handleFilter = (filter) => {
    return (event) => {
      setFilterValues({ ...filterValues, filter: event.target.value })
    }
  }

  return (
    <>
      <Drawer index={0} />


      <Box style={{ paddingTop: 70, paddingLeft: 280 }}>
        <Paper elevation={3} style={{ padding: 15, marginBottom: 20, marginRight: 20 }}>
          <Grid container>

            <Grid item xs={2}>
              <FormControl className={classes.formControl}>
                <InputLabel id="demo-simple-select-label">Categoria</InputLabel>
                <Select
                  onChange={handleFilter('categoria')}
                  value={filterValues.categoria}
                >
                  {
                    filters.categoria.map(i => <MenuItem value={i}>{i}</MenuItem>)
                  }
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={2}>
              <FormControl className={classes.formControl}>
                <InputLabel id="demo-simple-select-label">Mercado</InputLabel>
                <Select
                  onChange={handleFilter('mercado')}
                  value={filterValues.mercado}
                >
                  {
                    filters.mercado.map(i => <MenuItem value={i}>{i}</MenuItem>)
                  }
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={2}>
              <FormControl className={classes.formControl}>
                <InputLabel id="demo-simple-select-label">Periodo</InputLabel>
                <Select
                  onChange={handleFilter('periodo')}
                  value={filterValues.periodo}
                >
                  {
                    filters.periodo.map(i => <MenuItem value={i}>{i}</MenuItem>)
                  }
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={2}>
              <FormControl className={classes.formControl}>
                <InputLabel id="demo-simple-select-label">Submarca</InputLabel>
                <Select
                  onChange={handleFilter('submarca')}
                  value={filterValues.submarca}
                >
                  {
                    filters.submarca.map(i => <MenuItem value={i}>{i}</MenuItem>)
                  }
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={2}>
              <FormControl className={classes.formControl}>
                <InputLabel id="demo-simple-select-label">UNE</InputLabel>
                <Select
                  onChange={handleFilter('une')}
                  value={filterValues.une}
                >
                  {
                    filters.une.map(i => <MenuItem value={i}>{i}</MenuItem>)
                  }
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Paper>
        <div style={{ marginRight: 20 }}>
          {/* <Typography>Inventario Piso: {data.initialStock}</Typography> */}

          <ReactDataGrid
            columns={columns}
            rowGetter={
              i => data[i]
            }
            rowsCount={data.length}
            onGridRowsUpdated={onGridRowsUpdated}
            enableCellSelect={true}
            minHeight={650}
          />
        </div>
      </Box>
    </>
  )
}