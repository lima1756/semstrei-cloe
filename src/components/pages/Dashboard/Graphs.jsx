import React from 'react';
import Drawer from '../AppBarDrawer/Drawer';
import { Chart } from 'react-charts';
import { Box } from '@material-ui/core';

export default function Graphs() {

    const data = React.useMemo(
        () => [
            [[1, 1], [2, 10], [3, 10]],
            [[1, 8], [2, 6], [3, 0]],
            [[1, 3], [2, 10], [3, 9]]
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

    return (
        <div>
            <Drawer />

            <Box style={{ paddingTop: 70, paddingLeft: 280 }}>
                <h1>Hola Mundo de Graficas!</h1>
                <div
                    style={{
                        width: '400px',
                        height: '300px'
                    }}
                >
                    <Chart data={data} axes={axes} />
                </div>
            </Box>
        </div>
    )
}