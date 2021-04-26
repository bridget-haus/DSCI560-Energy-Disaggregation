import PieChart from "./PieChart";
import applianceData from '../data/nn_appliances.json'
import BarChart from "../neighbors/BarChart";
// import './Appliances.css'

function ApplianceChart () {



    return (
        <PieChart
            data={applianceData}
            container_id={"#app-chart"}
            id={'appliance-chart'}
        />

    );
}

export default ApplianceChart;