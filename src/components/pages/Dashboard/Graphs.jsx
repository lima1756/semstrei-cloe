import React from 'react';
import Drawer from '../AppBarDrawer/Drawer';
import { Line } from 'react-chartjs-2';
import { Box, Paper } from '@material-ui/core';

export default function Graphs() {
    const data = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        datasets: [
            {
                label: 'Ventas Cloe 2020 (M)',
                data: [3, 5, 8, 2, 5, 1, 9, 5, 4, 3, 6, 5],
                borderColor: ['rgba(255,206,86,0.2)'],
                backgroundColor: ['rgba(255,206,86,0.2)'],
                pointBackgroundColor: 'rgba(255,206,86,0.2)',
                pointBorderColor: 'rgba(255,206,86,0.2)',
            },
            {
                label: 'Datos IA (M)',
                data: [1, 8, 7, 6, 3, 9, 5, 1, 2, 4, 7, 2],
                borderColor: ['rgba(54,162,235,0.2)'],
                backgroundColor: ['rgba(54,162,235,0.2)'],
                pointBackgroundColor: 'rgba(54,162,235,0.2)',
                pointBorderColor: 'rgba(54,162,235,0.2)',
            }
        ]
    };

    const data2 = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        datasets: [
            {
                label: 'Ventas Cloe 2020 (M)',
                data: [0, 5, 9, 7, 6, 3, 6, 2, 3, 1, 4, 5],
                borderColor: ['rgba(255,206,86,0.2)'],
                backgroundColor: ['rgba(255,206,86,0.2)'],
                pointBackgroundColor: 'rgba(255,206,86,0.2)',
                pointBorderColor: 'rgba(255,206,86,0.2)',
            },
            {
                label: 'Datos IA (M)',
                data: [9, 7, 6, 9, 2, 4, 1, 3, 6, 8, 5, 5],
                borderColor: ['rgba(54,162,235,0.2)'],
                backgroundColor: ['rgba(54,162,235,0.2)'],
                pointBackgroundColor: 'rgba(54,162,235,0.2)',
                pointBorderColor: 'rgba(54,162,235,0.2)',
            }
        ]
    };

    const data3 = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        datasets: [
            {
                label: 'Ventas Cloe 2020 (M)',
                data: [1, 3, 2, 1, 3, 7, 6, 8, 9, 1, 2, 3],
                borderColor: ['rgba(255,206,86,0.2)'],
                backgroundColor: ['rgba(255,206,86,0.2)'],
                pointBackgroundColor: 'rgba(255,206,86,0.2)',
                pointBorderColor: 'rgba(255,206,86,0.2)',
            },
            {
                label: 'Datos IA (M)',
                data: [7, 9, 0, 1, 4, 3, 5, 6, 8, 9, 1, 4],
                borderColor: ['rgba(54,162,235,0.2)'],
                backgroundColor: ['rgba(54,162,235,0.2)'],
                pointBackgroundColor: 'rgba(54,162,235,0.2)',
                pointBorderColor: 'rgba(54,162,235,0.2)',
            }
        ]
    };

    const data4 = {
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        datasets: [
            {
                label: 'Ventas Cloe 2020 (M)',
                data: [8, 7, 5, 9, 3, 4, 2, 1, 2, 3, 4, 6],
                borderColor: ['rgba(255,206,86,0.2)'],
                backgroundColor: ['rgba(255,206,86,0.2)'],
                pointBackgroundColor: 'rgba(255,206,86,0.2)',
                pointBorderColor: 'rgba(255,206,86,0.2)',
            },
            {
                label: 'Datos IA (M)',
                data: [5, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7],
                borderColor: ['rgba(54,162,235,0.2)'],
                backgroundColor: ['rgba(54,162,235,0.2)'],
                pointBackgroundColor: 'rgba(54,162,235,0.2)',
                pointBorderColor: 'rgba(54,162,235,0.2)',
            }
        ]
    }

    const options = {
        title: {
            display: true,
            text: 'Comparación Une',
        },
        scales: {
            yAxes: [
                {
                    ticks: {
                        min: 0,
                        max: 10,
                        stepSize: 1,
                    }
                }
            ]
        }
    }

    const options2 = {
        title: {
            display: true,
            text: 'Comparación Submarca',
        },
        scales: {
            yAxes: [
                {
                    ticks: {
                        min: 0,
                        max: 10,
                        stepSize: 1,
                    }
                }
            ]
        }
    }

    const options3 = {
        title: {
            display: true,
            text: 'Comparación Categoria',
        },
        scales: {
            yAxes: [
                {
                    ticks: {
                        min: 0,
                        max: 10,
                        stepSize: 1,
                    }
                }
            ]
        }
    }

    const options4 = {
        title: {
            display: true,
            text: 'Comparación mercado',
        },
        scales: {
            yAxes: [
                {
                    ticks: {
                        min: 0,
                        max: 10,
                        stepSize: 1,
                    }
                }
            ]
        }
    }

    return (
        <div>
            <Drawer />
            <div style={{ paddingTop: 70, paddingLeft: 300 }}>
                <Box style={{ width: '100%' }}>
                    <Paper elevation={3} style={{ width: '95%' }}>
                        <div style={{ paddingLeft: 30, width: '95%' }}>
                            <Line data={data} options={options} />
                        </div>
                    </Paper>
                </Box>
                <Box style={{ width: '100%', marginTop: 50 }}>
                    <Paper elevation={3} style={{ width: '95%' }}>
                        <div style={{ paddingLeft: 30, width: '95%' }}>
                            <Line data={data2} options={options2} />
                        </div>
                    </Paper>
                </Box>
                <Box style={{ width: '100%', marginTop: 50 }}>
                    <Paper elevation={3} style={{ width: '95%' }}>
                        <div style={{ paddingLeft: 30, width: '95%' }}>
                            <Line data={data3} options={options3} />
                        </div>

                    </Paper>
                </Box>
                <Box style={{ width: '100%', marginTop: 50, marginBottom: 50 }}>
                    <Paper elevation={3} style={{ width: '95%' }}>
                        <div style={{ paddingLeft: 30, width: '95%' }}>
                            <Line data={data4} options={options4} />
                        </div>
                    </Paper>
                </Box>
            </div>
        </div>
    )
}