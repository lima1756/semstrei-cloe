import React, { useState, useEffect } from 'react';
import Drawer from '../AppBarDrawer/Drawer';
import { Line } from 'react-chartjs-2';
import { makeStyles } from '@material-ui/core/styles';
import {
  Box, Button, FormControl, Grid, Paper, InputLabel, TextField, MenuItem, Select
} from '@material-ui/core';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import axios from 'axios';
import { useSelector, } from 'react-redux';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    width: "100%",
    paddingRight: "1.3em"
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
}));

export default function Graphs() {
  const isLogged = useSelector(state => state.logged);
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({ 'categoria': [], 'mercado': [], 'periodo': [], 'submarca': [], 'une': [] })
  const [inventory, setInventory] = useState();
  const [filterValues, setFilterValues] = useState({
    'categoria': '', 'mercado': '', 'periodo': '', 'submarca': '', 'une': ''
  })
  const [backdrop, setBackdrop] = useState(false)
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const [maxValue, setMaxValue] = useState(0);
  const [outputArrayData, setOutputArrayData] = useState([]);
  const [months, setMonths] = useState([]);

  const otb = (periodo) => {
    setBackdrop(true)
    let url = 'https://150.136.172.48/api/otb?breakdown=false' +
      '&current_period=' + (periodo != null ? periodo : filterValues.periodo)
    if (filterValues.categoria !== '') {
      url += "&categoria=" + filterValues.categoria
    }
    if (filterValues.mercado !== '') {
      url += "&mercado=" + filterValues.mercado
    }
    if (filterValues.periodo !== '') {
      url += "&periodo=" + filterValues.periodo
    }
    if (filterValues.submarca !== '') {
      url += "&submarca=" + filterValues.submarca
    }
    if (filterValues.une !== '') {
      url += "&une=" + filterValues.une
    }
    axios.get(url, {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
      .then(function (response) {
        setData(response.data.table);
        setInventory(response.data.table[0].initialStock);
        setBackdrop(false)
        get_data_for_graphics(response.data.table);
      }).catch(function (error) {
        setBackdrop(false)
      })
  };

  useEffect(() => {
    setBackdrop(true)
    getFilters((periodo) => {
      otb(periodo);
    });
  }, []);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const get_data_for_graphics = (dataT) => {
    //This function gets the array of data from an specific 
    // column from otb.
    console.log("Funcionaaa", dataT);
    let output_array_data = [];
    let monthsArray = [];
    for (let t = 0; t < dataT.length; t++) {
      console.log("Holi", dataT[t]);
      output_array_data.push(dataT[t]["initialStock"]);
      monthsArray.push(dataT[t]["startDateProjectionPeriodOTB"].substring(3, dataT[t]["startDateProjectionPeriodOTB"].length));
    }
    //console.log(get_data_for_graphics(jsonOTB, "percentage_otb"))
    setMaxValue(Math.max(...output_array_data) * 1.2);
    setMonths(monthsArray);
    setOutputArrayData(output_array_data);

  }

  const getFilters = (callback) => {
    axios.get('https://150.136.172.48/api/otb/filters', {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
      .then(function (response) {
        setFilters(response.data.filters);
        setFilterValues({ ...filterValues, 'periodo': response.data.filters.periodo[0] })
        if (callback) {
          callback(response.data.filters.periodo[0])
        }
      }).catch(function (error) {
      })
  }

  console.log("Info", data);
  console.log("Maximomomomom", maxValue);
  console.log("oooot", outputArrayData);

  const handleFilter = (filter) => {
    return (event) => {
      let newFilter = {}
      newFilter[filter] = event.target.value;
      setFilterValues({ ...filterValues, ...newFilter })
    }
  }

  const handleChangeStock = () => {
    const new_data = parseInt(document.getElementById("changingStock").value)
    let jsonDataTable = JSON.parse(JSON.stringify(data))
    setInventory(new_data)
    fastOTB(jsonDataTable, new_data)
    setOpen(false);
  };

  const fastOTB = (jsonDataTable, startStock) => {
    // This function calculates the OTB for just one given table of the OTB
    //Inputs:
    // jsonDataTable: Json with the data of the OTB table to calculate.
    if (startStock == null) {
      startStock = inventory;
    }
    let stock_inicial, inventario_piso, target_venta, devolucion, compras, proyeccion_stock_eom, target_stock_eom, otb_minus_ctb, percentage_otb;
    for (let t = 0; t < jsonDataTable.length; t++) {
      if (t === 0) {
        jsonDataTable[t]["initialStock"] = startStock;
        stock_inicial = jsonDataTable[t]["initialStock"];
      } else {
        stock_inicial = proyeccion_stock_eom; // last projection stock is current initial stock.
      }
      inventario_piso = jsonDataTable[t]["inventoryOnStores"];
      target_venta = jsonDataTable[t]["targetSells"];
      devolucion = jsonDataTable[t]["devolution"];
      compras = jsonDataTable[t]["purchases"];

      proyeccion_stock_eom = (stock_inicial + devolucion + compras + inventario_piso) - target_venta;
      target_stock_eom = jsonDataTable[t]["targetStock"];
      otb_minus_ctb = target_stock_eom - proyeccion_stock_eom;
      if (target_stock_eom !== 0) {
        percentage_otb = 100 * otb_minus_ctb / target_stock_eom;
      } else {
        percentage_otb = 0;
      }

      jsonDataTable[t]["initialStock"] = stock_inicial;
      jsonDataTable[t]["projectionEomStock"] = proyeccion_stock_eom;
      jsonDataTable[t]["otb_minus_ctb"] = otb_minus_ctb;
      jsonDataTable[t]["percentage_otb"] = percentage_otb;
    }
    setData(jsonDataTable)
  }

  const data1 = {
    labels: months,
    datasets: [
      {
        label: 'Datos por mes',
        data: outputArrayData,
        borderColor: ['rgba(54,162,235,0.2)'],
        backgroundColor: ['rgba(54,162,235,0.2)'],
        pointBackgroundColor: 'rgba(54,162,235,0.2)',
        pointBorderColor: 'rgba(54,162,235,0.2)',
      },
    ]
  };

  const options = {
    title: {
      display: true,
      text: 'Proyección de inventario Eom (Miles de pesos)',
    },
    scales: {
      yAxes: [
        {
          ticks: {
            min: 0,
            max: maxValue,
            stepSize: maxValue / 8,
          }
        }
      ]
    }
  }

  return (
    <div>
      <Drawer />
      <div style={{ paddingTop: 70, paddingLeft: 300 }}>
        <Box style={{ paddingRight: 60 }}>
          <Paper elevation={3} style={{ padding: 15, marginBottom: 20, marginRight: 20 }}>
            <Grid container alignItems="center">
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
                  <InputLabel id="demo-simple-select-label">UNE</InputLabel>
                  <Select
                    onChange={handleFilter('une')}
                    value={filterValues.une}
                  >
                    <MenuItem value=''>Seleccionar</MenuItem>
                    {
                      filters.une.map(i => <MenuItem value={i}>{i}</MenuItem>)
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
                    <MenuItem value=''>Seleccionar</MenuItem>
                    {
                      filters.submarca.map(i => <MenuItem value={i}>{i}</MenuItem>)
                    }
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={2}>
                <FormControl className={classes.formControl}>
                  <InputLabel id="demo-simple-select-label">Categoria</InputLabel>
                  <Select
                    onChange={handleFilter('categoria')}
                    value={filterValues.categoria}
                  >
                    <MenuItem value=''>Seleccionar</MenuItem>
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
                    <MenuItem value=''>Seleccionar</MenuItem>
                    {
                      filters.mercado.map(i => <MenuItem value={i}>{i}</MenuItem>)
                    }
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={2}>
                <Button variant="contained" style={{ background: '#000' }} onClick={() => { otb() }} disabled={
                  filterValues.categoria === "" && filterValues.mercado === "" && filterValues.une === "" && filterValues.submarca === ""
                }>
                  <span style={{ color: '#fff' }}>Filtrar</span>
                </Button>
              </Grid>
            </Grid>
            <Dialog
              open={open}
              onClose={handleClose}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description"
            >
              <DialogTitle id="alert-dialog-title">{"Modificar valor del inventario en Piso"}</DialogTitle>
              <DialogContent>
                <DialogContentText id="alert-dialog-description">
                  Este cambio afectará diversos valores en la tabla actual.
          </DialogContentText>
                <TextField id="changingStock" label="Inventario Piso" />
              </DialogContent>
              <DialogActions>
                <Button variant="outlined" onClick={handleChangeStock}>
                  <span style={{ color: '#000000' }}> Confirmar </span>

                </Button>
                <Button variant="outlined" onClick={handleClose}>
                  <span style={{ color: '#000000' }}> Cancelar </span>

                </Button>
              </DialogActions>
            </Dialog>
          </Paper>
        </Box>
        <Box style={{ width: '100%' }}>
          <Paper elevation={3} style={{ width: '95%' }}>
            <div style={{ paddingLeft: 30, width: '95%' }}>
              <Line data={data1} options={options} />
            </div>
          </Paper>
        </Box>
      </div>
      <Backdrop className={classes.backdrop} open={backdrop} >
        <CircularProgress color="inherit" />
      </Backdrop>
    </div>
  )
}