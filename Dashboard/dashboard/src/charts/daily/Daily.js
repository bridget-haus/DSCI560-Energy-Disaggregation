import './Daily.css'
// import {AreaChart} from "react-charts-d3";
import AreaChart from './AreaChart';
import dailyData from './daily-usage.json'

function DailyChart () {

    return (

        <AreaChart
            data={dailyData}
            container_id={"#main-chart"}
            svg_id={"daily-chart"}
        />

    );
}

export default DailyChart;

