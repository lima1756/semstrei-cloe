import React, { useState, useEffect } from 'react';
import Drawer from '../AppBarDrawer/Drawer'
import { makeStyles } from '@material-ui/core/styles';
import {
  Box, Button, FormControl, IconButton, Grid, Paper, InputLabel, TextField,
  MenuItem, Select, FormControlLabel, Checkbox, Tooltip
} from '@material-ui/core';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import ReactDataGrid from "react-data-grid";
import "./style.css";
import { useSelector, } from 'react-redux';
import axios from 'axios';
import https from 'https';
import EditRoundedIcon from '@material-ui/icons/EditRounded';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import FileDownload from 'js-file-download';

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
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
}));

export default function Dashboard() {
  const isLogged = useSelector(state => state.logged);
  const [data, setData] = useState([]);
  const [filters, setFilters] = useState({ 'categoria': [], 'mercado': [], 'periodo': [], 'submarca': [], 'une': [] })
  const [breakdown, setBreakdown] = useState([]);
  const [showBreakdown, setShowBreakdown] = useState(false);
  const [inventory, setInventory] = useState();
  const [periodSize, setPeriodSize] = useState("");
  const [filterValues, setFilterValues] = useState({
    'categoria': '', 'mercado': '', 'periodo': '', 'submarca': '', 'une': ''
  })
  const [value, setValue] = React.useState('default');
  const [backdrop, setBackdrop] = useState(false)
  const classes = useStyles();
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const CellValue = ({ value }) => {
    const color = value > -1 ? "black" : "red";
    return <div style={{ color }}>{value}</div>;
  };

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const genUrl = () => {
    let url = 'https://150.136.172.48/api/otb?breakdown=' + (showBreakdown ? "True" : "false") +
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
    return url
  }

  const otb = (periodo) => {
    setBackdrop(true)
    const url = genUrl();
    axios.get(url, {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
      .then(function (response) {
        setData(response.data.table);
        setBreakdown(response.data.breakdown);
        setInventory(response.data.table[0].initialStock);
        setPeriodSize(response.data.table[0].period_length);
        setBackdrop(false)
      }).catch(function (error) {
        setBackdrop(false)
      })
  };

  const downloadPDF = () => {
    setBackdrop(true)
    const url = genUrl() + "&pdf=True";
    axios.get(url, {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
      .then(function (response) {
        setBackdrop(false)
        FileDownload(response.data, 'reporte.pdf')
      }).catch(function (error) {
        setBackdrop(false)
      })
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

  useEffect(() => {
    setBackdrop(true)
    getFilters((periodo) => { otb(periodo) });
  }, []);

  useEffect(() => {
    setBackdrop(true)
    otb()
  }, [showBreakdown])

  const columns = [
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
      formatter: CellValue
    },
    {
      key: 'inventoryOnStores',
      name: 'Inventario PISO',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
      formatter: CellValue
    },
    {
      key: 'targetSells',
      name: 'Tgt Venta Precio Lista',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
      formatter: CellValue
    },
    {
      key: 'devolution',
      name: 'Tgt Devolucion',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
      formatter: CellValue
    },
    {
      key: 'purchases',
      name: 'Compra',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
      formatter: CellValue
    },
    {
      key: 'projectionEomStock',
      name: 'Proyección Stock EOM',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'targetStock',
      name: 'Tgt Stock EOM',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
      formatter: CellValue
    },
    {
      key: 'otb_minus_ctb',
      name: 'OTB / CTB',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'percentage_otb',
      name: 'OTB / CTB (%)',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
  ];

  const onGridRowsUpdated = ({ fromRow, toRow, updated }) => {
    console.log(updated)
    let jsonDataTable = JSON.parse(JSON.stringify(data))
    for (let i = fromRow; i <= toRow; i++) {
      Object.keys(updated).forEach((key) => {
        jsonDataTable[i][key] = parseInt(updated[key])
      })
    }
    fastOTB(jsonDataTable)
  };

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


  return (
    <>
      <Drawer index={0} />


      <Box style={{ paddingTop: 70, paddingLeft: 280 }}>
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
              <Button variant="contained" style={{ background: '#000' }} onClick={() => { otb() }} >
                <span style={{ color: '#fff' }}>Filtrar</span>
              </Button>
            </Grid>

          </Grid>
          <Grid container>
            <Grid item xs={4} style={{ textAlign: 'left' }}>
              <p>Tamaño de los periodos pre-calculados: <b>{periodSize}</b></p>
            </Grid>
            <Grid item xs={4} style={{ textAlign: 'left' }}>
              Inventario inicial: <b>{inventory}</b>
              <IconButton aria-label="delete" onClick={handleClickOpen}>
                <EditRoundedIcon />
              </IconButton>
            </Grid>
            <Grid item xs={2} style={{ marginLeft: "auto", marginRight: "auto" }}>
              <Tooltip classes={{ tooltip: classes.customWidth }} title={(filterValues.categoria === "" && filterValues.mercado === "" && filterValues.une === "" && filterValues.submarca === "" && !showBreakdown) ? "Esta accion tomara un tiempo en cargar, porfavor seleccione por lo menos un filtro si desea algo especifico." : ""} arrow>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={showBreakdown}
                      onChange={(event) => { setBackdrop(true); setTimeout(() => { setShowBreakdown(!showBreakdown) }, 250); }}
                      name="Desglozar"
                      color="default"
                    />
                  }
                  label="Desglozar"
                />
              </Tooltip>
            </Grid>
            <Grid item xs={2} >
              <Button variant="contained" style={{ background: '#000' }} >
                <span style={{ color: '#fff' }} onClick={downloadPDF}>Descargar</span>
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
          />
          {
            showBreakdown && breakdown &&
            breakdown.map((item, index) => {
              return <div style={{ marginTop: "1.3em" }}>
                <h3>{item[0].une} - {item[0].submarca} - {item[0].categoria} - {item[0].mercado}</h3>
                <ReactDataGrid
                  columns={columns}
                  rowGetter={
                    i => item[i]
                  }
                  rowsCount={data.length}
                  onGridRowsUpdated={onGridRowsUpdated}
                  enableCellSelect={true}
                />
              </div>
            })
          }
        </div>
        <Backdrop className={classes.backdrop} open={backdrop} >
          <CircularProgress color="inherit" />
        </Backdrop>
      </Box>
    </>
  )
}