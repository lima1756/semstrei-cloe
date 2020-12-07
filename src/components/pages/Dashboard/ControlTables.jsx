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


export default function ControlTables(){
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
  
    const otb = (periodo) => {
      setBackdrop(true)
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
        key: 'une',
        name: 'Une',
        resizable: true,
        sortable: false,
        filterable: false,
        editable: false,
      },
      {
        key: 'submarca',
        name: 'Submarca',
        resizable: true,
        sortable: false,
        filterable: false,
        editable: false,
        formatter: CellValue
      },
      {
        key: 'periodo',
        name: 'Periodo',
        resizable: true,
        sortable: false,
        filterable: false,
        editable: true,
        formatter: CellValue
      },
      {
        key: 'cantidad',
        name: 'Cantidad',
        resizable: true,
        sortable: false,
        filterable: false,
        editable: true,
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
          <Backdrop className={classes.backdrop} open={backdrop} onClick={() => { setBackdrop(false) }}>
            <CircularProgress color="inherit" />
          </Backdrop>
        </Box>
      </>
    )
}