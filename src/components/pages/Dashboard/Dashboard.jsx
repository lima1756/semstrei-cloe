import React, { useState, useEffect, } from 'react';
import Drawer from '../AppBarDrawer/Drawer'
import { Box, Button, FormControlLabel, Grid, IconButton, Paper, Radio, RadioGroup, TextField, Typography, } from '@material-ui/core';
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

export default function Dashboard() {
  const isLogged = useSelector(state => state.logged);
  const [data, setData] = useState([]);
  const [dataRow, setDataRow] = useState([]);
  const [value, setValue] = useState('default');
  const [stockDef, setStockDef] = useState(87226);
  const [stockUne, setStockUne] = useState(39180);
  const [stockCat, setStockCat] = useState(48046);
  const [stockMerc, setStockMerc] = useState(37504);
  const [stockSub, setStockSub] = useState(14748);
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

  const otb = () => {
    axios.get('https://150.136.172.48/api/otb?une=j&submarca=a&categoria=c&mercado=m&current_period=04-OCT-20&breakdown=True', {
      headers: {
        'Authorization': `Bearer ${isLogged.token}`
      }
    })
      .then(function (response) {
        console.log(response);
        setData(response.data.table[0]);
        setDataRow(response.data.table);
      }).catch(function (error) {
        console.log(error);
      })
  };

  useEffect(() => {
    otb();
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
      formatter: CellValue
    },
    {
      key: 'sell',
      name: 'Tgt Venta Precio Lista',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'devolution',
      name: 'Tgt Devolución',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'buy',
      name: 'Compra',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'place',
      name: 'Por colocar',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'projection',
      name: 'Proyección Stock EOM',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'tgt',
      name: 'Tgt Stock EOM',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'compare',
      name: 'OTB / CTB',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
    {
      key: 'percentage',
      name: 'OTB /CTB (%)',
      resizable: true,
      sortable: false,
      filterable: false,
      editable: false,
      formatter: CellValue
    },
  ];

  const rowsDefault = {
    initialStockValue: 87226,
    table: [
      { month: "Enero", year: 2020, initialStock: 341853 + parseInt(stockDef), sell: 50367, devolution: 6193, buy: 9769, place: 0, projection: 4421, tgt: 143, compare: -4278, percentage: -2992 },
      { month: "Febrero", year: 2020, initialStock: 394675  + parseInt(stockDef), sell: 71776, devolution: 5252, buy: 59945, place: 0, projection: 388094 - parseInt((stockDef * .58) + stockDef), tgt: 130574, compare: -257520, percentage: -197 },
      { month: "Marzo", year: 2020, initialStock: 388094, sell: 89225, devolution: 4409, buy: 106651 + parseInt(stockDef), place: 0, projection: 409929, tgt: 127238 + parseInt(stockDef), compare: -282692, percentage: -222 },
      { month: "Abril", year: 2020, initialStock: 409929 - parseInt((stockDef * .58) + stockDef), sell: 84873, devolution: 4270, buy: 48750, place: 0, projection: 378076 - parseInt((stockDef * .58) + stockDef), tgt: 79625, compare: -298451, percentage: -375 },
      { month: "Mayo", year: 2020, initialStock: 378076, sell: 84777, devolution: 4339, buy: 47005 - parseInt((stockDef * .58) + stockDef), place: 0, projection: 344643, tgt: 79956, compare: -264687, percentage: -331 },
      { month: "Junio", year: 2020, initialStock: 344643, sell: 74473, devolution: 4842, buy: 85122, place: 0, projection: 360134 - parseInt((stockDef * .58) + stockDef), tgt: 126411, compare: -233724, percentage: -185 },
      { month: "Julio", year: 2020, initialStock: 360134, sell: 85439, devolution: 4974 - parseInt((stockDef * .58) + stockDef), buy: 39283, place: 0, projection: 318953, tgt: 122800, compare: -196153, percentage: -160 },
      { month: "Agosto", year: 2020, initialStock: 318953, sell: 83109, devolution: 3970, buy: 39323 - parseInt((stockDef * .58) + stockDef), place: 0, projection: 279137, tgt: 128089, compare: -151048, percentage: -118 },
      { month: "Septiembre", year: 2020, initialStock: 279137, sell: 80624 + parseInt(stockDef), devolution: 4754, buy: 0, place: 0, projection: 203266, tgt: 134113, compare: -69154, percentage: -52 },
      { month: "Octubre", year: 2020, initialStock: 203266, sell: 90161, devolution: 4077, buy: 0, place: 0, projection: 117182 + parseInt(stockDef), tgt: 139670, compare: 22488, percentage: 16 },
      { month: "Noviembre", year: 2020, initialStock: 117182, sell: 88656, devolution: 3512, buy: 0, place: 0, projection: 32038, tgt: 142948, compare: 110910 - parseInt((stockDef * .58) + stockDef), percentage: 78 },
      { month: "Diciembre", year: 2020, initialStock: 32038 - parseInt((stockDef * .58) + stockDef), sell: 97571, devolution: 4242, buy: 0, place: 0, projection: -61291, tgt: 143910, compare: 205202 + parseInt(stockDef), percentage: 143 },
      { month: "Enero", year: 2021, initialStock: -61291, sell: 93026, devolution: 4509, buy: 0, place: 0, projection: -149809, tgt: 153642, compare: 303451, percentage: 198 },
      { month: "Febrero", year: 2021, initialStock: -149809, sell: 98854, devolution: 3976, buy: 0, place: 0, projection: -244687, tgt: 142368, compare: 387055, percentage: 272 },
      { month: "Marzo", year: 2021, initialStock: -244687, sell: 106002, devolution: 5035, buy: 0, place: 0, projection: -345654 - parseInt((stockDef * .58) + stockDef), tgt: 127114, compare: 472769, percentage: 372 },
      { month: "Abril", year: 2021, initialStock: -345654 - parseInt((stockDef * .58) + stockDef), sell: 83821 + parseInt(stockDef), devolution: 5093, buy: 0, place: 0, projection: -424382, tgt: 126108, compare: 550490, percentage: 437 },
      { month: "Mayo", year: 2021, initialStock: -368331 + parseInt(stockDef), sell: 85665, devolution: 4372, buy: 0, place: 0, projection: -449624, tgt: 125930 - parseInt((stockDef * .58) + stockDef), compare: 575554 + parseInt(stockDef), percentage: 457 },
    ]
  };

  const rowsUne = {
    initialStockValue: 39180,
    table: [
      { month: "Enero", year: 2020, initialStock: 288106 + parseInt(stockUne), sell: 40263, devolution: 0, buy: 9530 + parseInt(stockUne), place: 0, projection: 296553 - parseInt((stockUne * .85) + stockUne), tgt: 105793 + parseInt(stockUne), compare: -190760, percentage: -180 + parseInt(stockUne) },
      { month: "Febrero", year: 2020, initialStock: 296553 - parseInt((stockUne * .85) + stockUne), sell: 62287, devolution: 0, buy: 54465, place: 0, projection: 288731, tgt: 105604, compare: -183127, percentage: -173 },
      { month: "Marzo", year: 2020, initialStock: 288731, sell: 78770, devolution: 0, buy: 101419, place: 0, projection: 311380 + parseInt(stockUne), tgt: 93392 + parseInt(stockUne), compare: -217988, percentage: -233 },
      { month: "Abril", year: 2020, initialStock: 311380, sell: 62035, devolution: 0, buy: 45856 - parseInt((stockUne * .85) + stockUne), place: 0, projection: 295202 - parseInt((stockUne * .85) + stockUne), tgt: 63552, compare: -231650, percentage: -363 + parseInt(stockUne) },
      { month: "Mayo", year: 2020, initialStock: 295202, sell: 62488, devolution: 0, buy: 45966, place: 0, projection: 278679, tgt: 70906, compare: -207774 - parseInt((stockUne * .85) + stockUne), percentage: -293 },
      { month: "Junio", year: 2020, initialStock: 278679 - parseInt((stockUne * .85) + stockUne), sell: 64616 + parseInt(stockUne), devolution: 0, buy: 74384 + parseInt(stockUne), place: 0, projection: 288448, tgt: 113524 + parseInt(stockUne), compare: -174924, percentage: -154 },
      { month: "Julio", year: 2020, initialStock: 288448, sell: 77195, devolution: 0, buy: 37046, place: 0, projection: 248298, tgt: 107891, compare: -140407, percentage: -130 },
      { month: "Agosto", year: 2020, initialStock: 248298, sell: 74170, devolution: 0, buy: 38624, place: 0, projection: 212752, tgt: 110490, compare: -102262, percentage: -93 },
      { month: "Septiembre", year: 2020, initialStock: 212752, sell: 69684, devolution: 0, buy: 0, place: 0, projection: 143068 - parseInt((stockUne * .85) + stockUne), tgt: 116509, compare: -26559, percentage: -23 },
      { month: "Octubre", year: 2020, initialStock: 143068 - parseInt((stockUne * .85) + stockUne), sell: 77636, devolution: 0, buy: 0, place: 0, projection: 65432, tgt: 122583, compare: 57151, percentage: 47 + parseInt(stockUne) },
      { month: "Noviembre", year: 2020, initialStock: 65432, sell: 77709, devolution: 0, buy: 0, place: 0, projection: -12277, tgt: 126795, compare: 139072, percentage: 110 },
      { month: "Diciembre", year: 2020, initialStock: -12277, sell: 85735, devolution: 0, buy: 0, place: 0, projection: -98012, tgt: 129600, compare: 227612 - parseInt((stockUne * .85) + stockUne), percentage: 176 },
      { month: "Enero", year: 2021, initialStock: -98012 + parseInt(stockUne), sell: 83325 - parseInt((stockUne * .85) + stockUne), devolution: 0, buy: 0, place: 0, projection: -181337, tgt: 139616, compare: 320952, percentage: 230 },
      { month: "Febrero", year: 2021, initialStock: -181337, sell: 89475, devolution: 0, buy: 0, place: 0, projection: -270812, tgt: 120659, compare: 391471, percentage: 324 },
      { month: "Marzo", year: 2021, initialStock: -270812 - parseInt((stockUne * .85) + stockUne), sell: 96679, devolution: 0, buy: 0, place: 0, projection: -367491, tgt: 99465, compare: 466956, percentage: 469 - parseInt((stockUne * .85) + stockUne) },
      { month: "Abril", year: 2021, initialStock: -367491, sell: 64200, devolution: 0, buy: 0, place: 0, projection: -431691 + parseInt(stockUne), tgt: 104766 - parseInt((stockUne * .85) + stockUne), compare: 536457, percentage: 512 },
      { month: "Mayo", year: 2021, initialStock: -375640 + parseInt(stockUne), sell: 68420, devolution: 0, buy: 0, place: 0, projection: -444061 + parseInt(stockUne), tgt: 111677, compare: 555737, percentage: 498 },
    ]
  };

  const rowsCat = {
    initialStockValue: 48046,
    table: [
      { month: "Enero", year: 2020, initialStock: 341853 +parseInt(stockCat), sell: 50367 +parseInt(stockCat), devolution: 6193, buy: 239, place: 0, projection: 98121 +parseInt(stockCat), tgt: 14958, compare: -83163, percentage: -556 },
      { month: "Febrero", year: 2020, initialStock: 394675, sell: 71776, devolution: 5252 - parseInt((stockCat * .85) + stockCat), buy: 5479, place: 0, projection: 99363, tgt: 24970, compare: -74393 +parseInt(stockCat), percentage: -298 +parseInt(stockCat) },
      { month: "Marzo", year: 2020, initialStock: 388094 +parseInt(stockCat), sell: 89225 +parseInt(stockCat), devolution: 4409, buy: 5231, place: 0, projection: 98549 +parseInt(stockCat), tgt: 33846 +parseInt(stockCat), compare: -64703, percentage: -191 },
      { month: "Abril", year: 2020, initialStock: 409929 - parseInt((stockCat * .85) + stockCat), sell: 84873, devolution: 4270 +parseInt(stockCat), buy: 2894 +parseInt(stockCat), place: 0, projection: 82874 - parseInt((stockCat * .85) + stockCat), tgt: 16073, compare: -66801, percentage: -416 +parseInt(stockCat) },
      { month: "Mayo", year: 2020, initialStock: 378076, sell: 84777, devolution: 4339, buy: 1039, place: 0, projection: 65963 +parseInt(stockCat), tgt: 9050, compare: -56913 +parseInt(stockCat), percentage: -629 },
      { month: "Junio", year: 2020, initialStock: 344643, sell: 74473, devolution: 4842, buy: 10738, place: 0, projection: 71687 - parseInt((stockCat * .85) + stockCat), tgt: 12886 +parseInt(stockCat), compare: -58800 - parseInt((stockCat * .85) + stockCat), percentage: -456 },
      { month: "Julio", year: 2020, initialStock: 360134 - parseInt((stockCat * .85) + stockCat), sell: 85439 +parseInt(stockCat), devolution: 4974, buy: 2237 - parseInt((stockCat * .85) + stockCat), place: 0, projection: 70655 +parseInt(stockCat), tgt: 14909, compare: -55746, percentage: -374 +parseInt(stockCat) },
      { month: "Agosto", year: 2020, initialStock: 318953 +parseInt(stockCat), sell: 83109, devolution: 3970, buy: 698, place: 0, projection: 66384, tgt: 17599, compare: -48786, percentage: -277 },
      { month: "Septiembre", year: 2020, initialStock: 279137, sell: 80624, devolution: 4754, buy: 0, place: 0, projection: 60198, tgt: 17604 - parseInt((stockCat * .85) + stockCat), compare: -42595, percentage: -142 },
      { month: "Octubre", year: 2020, initialStock: 203266, sell: 90161, devolution: 4077, buy: 0, place: 0, projection: 51750, tgt: 17087, compare: -34663, percentage: -203 },
      { month: "Noviembre", year: 2020, initialStock: 117182, sell: 88656, devolution: 3512, buy: 0, place: 0, projection: 44315, tgt: 16153 - parseInt((stockCat * .85) + stockCat), compare: -28162, percentage: -174 - parseInt((stockCat * .85) + stockCat) },
      { month: "Diciembre", year: 2020, initialStock: 32038 +parseInt(stockCat), sell: 97571 +parseInt(stockCat), devolution: 4242 +parseInt(stockCat), buy: 0, place: 0, projection: 36721, tgt: 14310, compare: -22410 +parseInt(stockCat), percentage: -157 },
      { month: "Enero", year: 2021, initialStock: -61291, sell: 93026, devolution: 4509 - parseInt((stockCat * .85) + stockCat), buy: 0, place: 0, projection: 31528, tgt: 14027, compare: -17501, percentage: -125 },
      { month: "Febrero", year: 2021, initialStock: -149809, sell: 98854, devolution: 3976 - parseInt((stockCat * .85) + stockCat), buy: 0, place: 0, projection: 26125 +parseInt(stockCat), tgt: 21708 +parseInt(stockCat), compare: -4417, percentage: -20 },
      { month: "Marzo", year: 2021, initialStock: -244687 - parseInt((stockCat * .85) + stockCat), sell: 106002 - parseInt((stockCat * .85) + stockCat), devolution: 5035, buy: 0, place: 0, projection: 21837, tgt: 27649 - parseInt((stockCat * .85) + stockCat), compare: 5812, percentage: 21 +parseInt(stockCat) },
      { month: "Abril", year: 2021, initialStock: -345654, sell: 83821, devolution: 5093 +parseInt(stockCat), buy: 0, place: 0, projection: 7309, tgt: 21342, compare: 14033, percentage: 66 - parseInt((stockCat * .85) + stockCat) },
      { month: "Mayo", year: 2021, initialStock: -368331 +parseInt(stockCat), sell: 85665 +parseInt(stockCat), devolution: 4372 +parseInt(stockCat), buy: 0 - parseInt((stockCat * .85) + stockCat), place: 0, projection: 5563, tgt: 14254 - parseInt((stockCat * .85) + stockCat), compare: 19817 - parseInt((stockCat * .85) + stockCat), percentage: 139 +parseInt(stockCat) },
    ]
  };

  const rowsMercado = {
    initialStockValue: 37504,
    table: [
      { month: "Enero", year: 2020, initialStock: 53747 + parseInt(stockMerc), sell: 10104 - parseInt((stockMerc * .85) + stockMerc -500), devolution: 6193, buy: 9769, place: 0, projection: 4421, tgt: 143, compare: -4278 + parseInt(stockMerc), percentage: -2992 },
      { month: "Febrero", year: 2020, initialStock: 98121, sell: 9489, devolution: 5252 + parseInt(stockMerc), buy: 59945 - parseInt((stockMerc * .85) + stockMerc -500), place: 0, projection: 388094 - parseInt((stockMerc * .85) + stockMerc -500), tgt: 130574 - parseInt((stockMerc * .85) + stockMerc -500), compare: -257520 + parseInt(stockMerc), percentage: -197 },
      { month: "Marzo", year: 2020, initialStock: 99363, sell: 10455, devolution: 4409, buy: 106651, place: 0, projection: 409929, tgt: 127238 + parseInt(stockMerc), compare: -282692, percentage: -222 - parseInt((stockMerc * .85) + stockMerc -500) },
      { month: "Abril", year: 2020, initialStock: 98549 + parseInt(stockMerc), sell: 22839 + parseInt(stockMerc), devolution: 4270 - parseInt((stockMerc * .85) + stockMerc -500), buy: 48750, place: 0, projection: 378076, tgt: 79625, compare: -298451 - parseInt((stockMerc * .85) + stockMerc -500), percentage: -375 },
      { month: "Mayo", year: 2020, initialStock: 82874, sell: 22289, devolution: 4339 - parseInt((stockMerc * .85) + stockMerc -500), buy: 47005, place: 0, projection: 344643, tgt: 79956, compare: -264687, percentage: -331 + parseInt(stockMerc) },
      { month: "Junio", year: 2020, initialStock: 65963, sell: 9857, devolution: 4842, buy: 85122 + parseInt(stockMerc), place: 0, projection: 360134 + parseInt(stockMerc), tgt: 126411 + parseInt(stockMerc), compare: -233724 + parseInt(stockMerc), percentage: -185 + parseInt(stockMerc) },
      { month: "Julio", year: 2020, initialStock: 71687 - parseInt((stockMerc * .85) + stockMerc -500), sell: 8243 + parseInt(stockMerc), devolution: 4974 + parseInt(stockMerc), buy: 39283, place: 0, projection: 318953, tgt: 122800, compare: -196153, percentage: -160 },
      { month: "Agosto", year: 2020, initialStock: 70655, sell: 8939 - parseInt((stockMerc * .85) + stockMerc -500), devolution: 3970, buy: 39323 + parseInt(stockMerc), place: 0, projection: 279137, tgt: 128089, compare: -151048 - parseInt((stockMerc * .85) + stockMerc -500), percentage: -118 },
      { month: "Septiembre", year: 2020, initialStock: 66384 + parseInt(stockMerc), sell: 10940, devolution: 4754, buy: 0, place: 0, projection: 203266, tgt: 134113 + parseInt(stockMerc), compare: -69154 + parseInt(stockMerc), percentage: -52 },
      { month: "Octubre", year: 2020, initialStock: 60198, sell: 12525, devolution: 4077 - parseInt((stockMerc * .85) + stockMerc -500), buy: 0, place: 0, projection: 117182 + parseInt(stockMerc), tgt: 139670, compare: 22488, percentage: 16 },
      { month: "Noviembre", year: 2020, initialStock: 51750 - parseInt((stockMerc * .85) + stockMerc -500), sell: 10947, devolution: 3512 - parseInt((stockMerc * .85) + stockMerc -500), buy: 0, place: 0, projection: 32038, tgt: 142948, compare: 110910 + parseInt(stockMerc), percentage: 78 },
      { month: "Diciembre", year: 2020, initialStock: 44315, sell: 11836, devolution: 4242 + parseInt(stockMerc), buy: 0 + parseInt(stockMerc), place: 0, projection: -61291, tgt: 143910 - parseInt((stockMerc * .85) + stockMerc -500), compare: 205202, percentage: 143 },
      { month: "Enero", year: 2021, initialStock: 36721 - parseInt((stockMerc * .85) + stockMerc -500), sell: 9701, devolution: 4509, buy: 0, place: 0, projection: -149809 + parseInt(stockMerc), tgt: 153642, compare: 303451, percentage: 198 + parseInt(stockMerc) },
      { month: "Febrero", year: 2021, initialStock: 31528 + parseInt(stockMerc), sell: 9379, devolution: 3976, buy: 0, place: 0, projection: -244687, tgt: 142368, compare: 387055, percentage: 272 + parseInt(stockMerc) },
      { month: "Marzo", year: 2021, initialStock: 26125, sell: 9323, devolution: 5035, buy: 0 + parseInt(stockMerc), place: 0, projection: -345654, tgt: 127114 - parseInt((stockMerc * .85) + stockMerc -500), compare: 472769, percentage: 372 + parseInt(stockMerc) },
      { month: "Abril", year: 2021, initialStock: 21837 - parseInt((stockMerc * .85) + stockMerc -500), sell: 19621 + parseInt(stockMerc), devolution: 5093, buy: 0, place: 0 - parseInt((stockMerc * .85) + stockMerc -500), projection: -424382, tgt: 126108, compare: 550490, percentage: 437 - parseInt((stockMerc * .85) + stockMerc -500) },
      { month: "Mayo", year: 2021, initialStock: 7309, sell: 17244, devolution: 4372, buy: 0, place: 0, projection: -449624 + parseInt(stockMerc), tgt: 125930, compare: 575554, percentage: 457 - parseInt((stockMerc * .85) + stockMerc -500) },
    ]
  };

  const rowsSub = {
    initialStockValue: 14748,
    table: [
      { month: "Enero", year: 2020, initialStock: 341853 + parseInt(stockSub), sell: 902365, devolution: 9625, buy: 9769, place: 0, projection: 4421, tgt: 14 - parseInt(stockSub) - 23, compare: -4278, percentage: -2992 - parseInt(stockSub) - 2 },
      { month: "Febrero", year: 2020, initialStock: 394675 - parseInt(stockSub) - 2, sell: 71776, devolution: 5252, buy: 59945, place: 0, projection: 388094, tgt: 130574, compare: -25752 - parseInt(stockSub) - 20, percentage: -197 },
      { month: "Marzo", year: 2020, initialStock: 388094, sell: 89225, devolution: 4409, buy: 106651 - parseInt(stockSub) - 2, place: 0, projection: 409929 + parseInt(stockSub), tgt: 127238 + parseInt(stockSub), compare: -282692 + parseInt(stockSub), percentage: -222 },
      { month: "Abril", year: 2020, initialStock: 409929 - parseInt(stockSub) - 2, sell: 84873, devolution: 4270 + parseInt(stockSub), buy: 48750 - parseInt(stockSub) - 2, place: 0, projection: 378076, tgt: 79625, compare: -757575, percentage: -375 },
      { month: "Mayo", year: 2020, initialStock: 378076 + parseInt(stockSub), sell: 84777, devolution: 4339, buy: 47005, place: 0, projection: 54353, tgt: 79956 + parseInt(stockSub), compare: -264687, percentage: -331 },
      { month: "Junio", year: 2020, initialStock: 344643, sell: 74473 - parseInt(stockSub) - 2, devolution: 4245 - parseInt(stockSub) - 2, buy: 85122 + parseInt(stockSub), place: 0, projection: 360134, tgt: 126411 - parseInt(stockSub) - 2, compare: -85422, percentage: -185 },
      { month: "Julio", year: 2020, initialStock: 360134, sell: 85439 + parseInt(stockSub), devolution: 53543, buy: 39283, place: 0, projection: 318953, tgt: 12800, compare: -196153, percentage: -160 - parseInt(stockSub) - 2 },
      { month: "Agosto", year: 2020, initialStock: 318953, sell: 83109, devolution: 3970, buy: 39323 - parseInt(stockSub) - 2, place: 0, projection: 279137, tgt: 128089, compare: -151048, percentage: -118 },
      { month: "Septiembre", year: 2020, initialStock: 279137, sell: 80624, devolution: 4754 + parseInt(stockSub), buy: 0, place: 0, projection: 203266 + parseInt(stockSub), tgt: 134113 + parseInt(stockSub), compare: -69154, percentage: -52 },
      { month: "Octubre", year: 2020, initialStock: 203266 - parseInt(stockSub) - 2, sell: 90161, devolution: 4077, buy: 0, place: 0, projection: 353533 - parseInt(stockSub) - 2, tgt: 139670, compare: 22488, percentage: 16 },
      { month: "Noviembre", year: 2020, initialStock: 117182 + parseInt(stockSub), sell: 88656, devolution: 34533, buy: 0, place: 0, projection: 5353, tgt: 142948, compare: 110910, percentage: 78 - parseInt(stockSub) - 2 },
      { month: "Diciembre", year: 2020, initialStock: 32038, sell: 97571, devolution: 4242 + parseInt(stockSub), buy: 0, place: 0, projection: -3533, tgt: 143910, compare: 75575, percentage: 143 },
      { month: "Enero", year: 2021, initialStock: -61291 - parseInt(stockSub) - 2, sell: 93026, devolution: 4509, buy: 0, place: 0, projection: -149809 + parseInt(stockSub), tgt: 153642 - parseInt(stockSub) - 2, compare: 303451, percentage: 198 },
      { month: "Febrero", year: 2021, initialStock: -149809 + parseInt(stockSub), sell: 98854, devolution: 3976, buy: 0, place: 0, projection: -244687, tgt: 142368, compare: 387055, percentage: 272 },
      { month: "Marzo", year: 2021, initialStock: -244687, sell: 106002 - parseInt(stockSub) - 2, devolution: 5035 + parseInt(stockSub), buy: 0, place: 0, projection: -345654 + parseInt(stockSub), tgt: 127114, compare: 242422, percentage: 372 },
      { month: "Abril", year: 2021, initialStock: -345654 + parseInt(stockSub), sell: 83821 + parseInt(stockSub), devolution: 2121 - parseInt(stockSub) - 2, buy: 0, place: 0, projection: -3535535 + parseInt(stockSub), tgt: 126108, compare: 550490, percentage: 437 },
      { month: "Mayo", year: 2021, initialStock: -368331 - parseInt(stockSub) - 2, sell: 85665, devolution: 4372, buy: 0, place: 0, projection: -449624, tgt: 125930, compare: 575554, percentage: 457 },
    ]
  };

  const onGridRowsUpdated = ({ fromRow, toRow, updated }) => {
    this.setState(state => {
      const rows = rows.slice();
      for (let i = fromRow; i <= toRow; i++) {
        rows[i] = { ...rows[i], ...updated };
      }
      return { rows };
    });
  };

  const handleChangeStock = () => {
    console.log(document.getElementById("changingStock").value);
    if (value == "default") {
      setStockDef(document.getElementById("changingStock").value);
    } else if (value == "une") {
      setStockUne(document.getElementById("changingStock").value);
    } else if (value == "mercado") {
      setStockMerc(document.getElementById("changingStock").value);
    } else if (value == "categoria") {
      setStockCat(document.getElementById("changingStock").value);
    } else {
      setStockSub(document.getElementById("changingStock").value);
    }
    setOpen(false);
  };

  return (
    <>
      <Drawer index={0} />


      <Box style={{ paddingTop: 70, paddingLeft: 280 }}>
        <Paper elevation={3} style={{ padding: 15, marginBottom: 20, marginRight: 20 }}>
          <Grid container spacing={3}>
            <Grid item xs={11}>
              <Typography align="left">Inventario Piso:
  {
                  value == "default" ?
                    stockDef
                    : value == "une" ?
                      stockUne
                      : value == "mercado" ?
                        stockMerc
                        : value == "categoria" ?
                          stockCat
                          :
                          stockSub
                }
              </Typography>
            </Grid>
            <Grid item xs={1}>
              <IconButton aria-label="delete" onClick={handleClickOpen}>
                <EditRoundedIcon />
              </IconButton>
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
          <RadioGroup aria-label="gender" name="gender1" value={value} onChange={handleChange}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <FormControlLabel value="default" control={<Radio color="default" />} label="Default" />
                <FormControlLabel value="une" control={<Radio color="default" />} label="Une" />
                <FormControlLabel value="mercado" control={<Radio color="default" />} label="Mercado" />
                <FormControlLabel value="categoria" control={<Radio color="default" />} label="Categoria" />
                <FormControlLabel value="submarca" control={<Radio color="default" />} label="Submarca" />
              </Grid>

            </Grid>


          </RadioGroup>
        </Paper>
        <div style={{ marginRight: 20 }}>
          {/* <Typography>Inventario Piso: {data.initialStock}</Typography> */}

          <ReactDataGrid
            columns={columns}
            rowGetter={
              value == "default" ?
                i => rowsDefault.table[i]
                : value == "une" ?
                  i => rowsUne.table[i]
                  : value == "mercado" ?
                    i => rowsMercado.table[i]
                    : value == "categoria" ?
                      i => rowsCat.table[i]
                      :
                      i => rowsSub.table[i]
            }
            rowsCount={
              value == "default" ?
                rowsDefault.table.length
                : value == "une" ?
                  rowsUne.table.length
                  : value == "mercado" ?
                    rowsMercado.table.length
                    : value == "categoria" ?
                      rowsCat.table.length
                      :
                      rowsSub.table.length
            }
            onGridRowsUpdated={onGridRowsUpdated}

            enableCellSelect={true}
            minHeight={650}
          />
        </div>
      </Box>
    </>
  )
}