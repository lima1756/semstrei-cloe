import React, { useState, useEffect, } from 'react';
import Drawer from '../AppBarDrawer/Drawer'
import { Box, FormControlLabel, Grid, Paper, Radio, RadioGroup, TextField, Typography, } from '@material-ui/core';
import ReactDataGrid from "react-data-grid";
import "./style.css";
import { useSelector, } from 'react-redux';
import axios from 'axios';
import https from 'https';

const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
});
axios.defaults.options = httpsAgent;

export default function Dashboard() {
  const isLogged = useSelector(state => state.logged);
  const [ data, setData ] = useState([]);
  const [ dataRow, setDataRow ] = useState([]);
  const [value, setValue] = React.useState('female');

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const otb = () => {
    axios.get('https://150.136.172.48/api/otb?une=j&submarca=a&categoria=c&mercado=m&current_period=04-OCT-20&breakdown=True',{
        headers: {
            'Authorization': `Bearer ${isLogged.token}`
          }
    })
    .then(function(response){
      console.log(response);
      setData(response.data.table[0]);
      setDataRow(response.data.table);
    }).catch(function(error){
        console.log(error);
    })
  };

  const probandoAndo = () => {
 var d = new Date();
 var n = d.getMonth();
console.log(n);

  };

  useEffect (() =>{ 
    otb();
    probandoAndo(); 
  }, []);

  const columns = [
    {
      key: 'month',
      name: 'Mes',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'year',
      name: 'Año',
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
      key: 'sell',
      name: 'Tgt Venta Precio Lista',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
    },
    {
      key: 'devolution',
      name: 'Tgt Devolución',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: true,
    },
    {
      key: 'buy',
      name: 'Compra',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'place',
      name: 'Por colocar',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'projection',
      name: 'Proyección Stock EOM',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'tgt',
      name: 'Tgt Stock EOM',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'compare',
      name: 'OTB / CTB',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
    {
      key: 'percentage',
      name: '% OTB /CTB',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
    },
  ];

  const rows = [
    { month: "Enero", year: 2020, place: 0},
    { month: "Febrero", year: 2020, place: 0},
    { month: "Marzo", year: 2020, place: 0},
    { month: "Abril", year: 2020, place: 0},
    { month: "Mayo", year: 2020, place: 0},
    { month: "Junio", year: 2020, place: 0},
    { month: "Julio", year: 2020, place: 0},
    { month: "Agosto", year: 2020, place: 0},
    { month: "Septiembre", year: 2020, place: 0},
    { month: "Octubre", year: 2020, place: 0},
    { month: "Noviembre", year: 2020, place: 0},
    { month: "Diciembre", year: 2020, place: 0},
    { month: "Enero", year: 2021, place: 0},
    { month: "Febrero", year: 2021, place: 0},
    { month: "Marzo", year: 2021, place: 0},
    { month: "Abril", year: 2021, place: 0},
    { month: "Mayo", year: 2021, place: 0},
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

  return (
    <>
      <Drawer index={0} />


      <Box style={{ paddingTop: 70, paddingLeft: 280 }}>
      <Paper elevation={3} style={{padding: 15, marginBottom: 20, marginRight:20}}>
      <Typography align="left">Inventario Piso: </Typography>
      <RadioGroup aria-label="gender" name="gender1" value={value} onChange={handleChange}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
        <FormControlLabel value="une" control={<Radio color="default"/>} label="Une" />
        <FormControlLabel value="mercado" control={<Radio color="default"/>} label="Mercado" />
        <FormControlLabel value="categoria" control={<Radio color="default"/>} label="Categoria" />
        <FormControlLabel value="submarca" control={<Radio color="default"/>} label="Submarca" />
        </Grid>

      </Grid>


      </RadioGroup>
        </Paper>
        <div style={{marginRight:20}}>
  {/* <Typography>Inventario Piso: {data.initialStock}</Typography> */}

          <ReactDataGrid
            columns={columns}
            rowGetter={i => rows[i]}
            rowsCount={rows.length}
            onGridRowsUpdated={onGridRowsUpdated}
            enableCellSelect={true}
            minHeight={650}
          />
        </div>
      </Box>
    </>
  )
}