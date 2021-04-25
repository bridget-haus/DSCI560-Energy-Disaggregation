import PieChart from "./PieChart";
import applianceData from '../data/nn_appliances.json'
import BarChart from "../neighbors/BarChart";
// import './Appliances.css'

function ApplianceChart () {



    return (
        <PieChart
            data={applianceData}
            container_id={"sub-charts"}
            id={'appliance-chart'}
        />

    );
}

export default ApplianceChart;