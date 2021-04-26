import BarChart from "./BarChart";
import neighborData from '../data/nn_appliances.json'
import './Neighbors.css'

function NeighborChart () {

    return (
        <BarChart
            data={neighborData}
            container_id={"#neighbors-chart"}
            id={'neighbor-chart'}
        />

    );
}

export default NeighborChart;