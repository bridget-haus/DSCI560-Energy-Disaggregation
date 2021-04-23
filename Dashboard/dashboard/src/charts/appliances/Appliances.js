import {PieChart} from 'react-charts-d3';

function ApplianceChart () {

    const data = [
        { label: 'Washer/Dryer', value: 23 },
        { label: 'Lighting', value: 15 },
    ];

    return (
        <PieChart
            data={data}
        />

    );
}

export default ApplianceChart;