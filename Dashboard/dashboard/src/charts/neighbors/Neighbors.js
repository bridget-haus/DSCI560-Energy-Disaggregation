import BarChart from "./BarChart";
import neighborData from './data-neighbor.json'
import './Neighbors.css'
// import {BarChart} from 'react-charts-d3'

function NeighborChart () {

    // const data = neighborData;
    const data = [
        { key: 'Main', values: [ { x: 'A', y: 23 }, { x: 'B', y: 8 } ] },
        { key: 'Lighting', values: [ { x: 'A', y: 15 }, { x: 'B', y: 37 } ] },
        { key: 'Washer/Dryer', values: [ { x: 'A', y: 36 }, { x: 'B', y: 9 } ] },
    ];

    return (
        <BarChart
            data={neighborData}
            container_id={"sub-charts"}
            id={'neighbor-chart'}
        />

    );
}

export default NeighborChart;