import React from 'react';
import Drawer from '../AppBarDrawer/Drawer'
import { Chart } from 'react-charts';
import { Button, Grid } from '@material-ui/core';
import ResizableBox from "./ResizableBox";
import "./style.css";

export default function Dashboard() {
  const series = React.useMemo(
    () => ({
      type: "bubble",
      showPoints: false
    }),
    []
  );

  const data = React.useMemo(
    () => [
      {
        label: 'Series 1',
        data: [[0, 1], [1, 2], [2, 4], [3, 2], [4, 7]]
      },
      {
        label: 'Series 2',
        data: [[0, 3], [1, 1], [2, 5], [3, 6], [4, 4]]
      }
    ],
    []
  )

  const axes = React.useMemo(
    () => [
      { primary: true, type: 'linear', position: 'bottom' },
      { type: 'linear', position: 'left' }
    ],
    []
  )

  const dataSecond = React.useMemo(
    () => [
      [[1, 10], [2, 10], [3, 10]],
      [[1, 10], [2, 10], [3, 10]],
      [[1, 10], [2, 10], [3, 10]]
    ],
    []
  )

  const axesSecond = React.useMemo(
    () => [
      { primary: true, type: 'linear', position: 'bottom' },
      { type: 'linear', position: 'left' }
    ],
    []
  )

  return (
    <>
      <Drawer index={0} />

      <Grid container style={{ marginTop: 70, paddingLeft: 280, }}>
        <Grid item xs={12} sm={6}>
          <div
            style={{
              width: '400px',
              height: '300px'
            }}
          >
            <Chart data={dataSecond} axes={axesSecond} />
          </div>
        </Grid>
        <Grid item xs={12} sm={6}>
          <div
            style={{
              width: '400px',
              height: '300px',
            }}
          >
            <Chart data={data} axes={axes} />
          </div>
        </Grid>
        <Grid container style={{ paddingLeft: 280 }}>
          <Grid item xs={12} sm={6}>
            <ResizableBox>
              <Chart
                data={data}
                series={series}
                axes={axes}
                grouping="single"
                tooltip
              />
            </ResizableBox>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button style={{ marginTop: 250 }} variant='outlined'>Descargar Archivos</Button>
          </Grid>
        </Grid>

      </Grid>
    </>
  )
}