import * as d3 from 'd3';
import React, { useRef, useEffect } from 'react';

function AreaChart(props){

    const ref = useRef();
    //TODO: Use Context
    const data = d3.entries(props.data)
        .filter(d => d.key === 'house_6')
        .map(d => d.value)[0];

    // const width = d3.select(props.container_id).style("width").slice(0,-2);
    // const height = d3.select(props.container_id).style("height").slice(0,-2);
    const parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");

    useEffect(() => {

        const parent = d3.select(props.container_id);
        const width = parent.style("width").slice(0,-2);
        const height = parent.style("height").slice(0,-2);

        const chartWidth = width * props.widthMult;
        const chartHeight = height * props.heightMult;

        const container = d3.select(ref.current);

        const svg = container.append("svg")
            .attr("class", "Area-Chart-Svg")
            .attr('id', props.svg_id)
            .attr('width', width * props.containerMult)
            .attr('height', height * props.containerMult)

        const appliances = data.map(d => d.appliance);
        const values = data.map(d => d.values);

        const color = d3.scaleOrdinal()
            .domain(appliances)
            .range(d3.schemeSet2);

        const x = d3.scaleTime()
            .range([0, chartWidth])
            .domain(d3.extent(values.map(eachList => eachList.map(d => parseDate(d.timestamp)))[0]));

        const y = d3.scaleSqrt()
            .range([chartHeight, 0])
            .domain([10, d3.max(values.map(eachList => d3.max(eachList.map( d=>d.prediction)))) + 10]);

        const xAxis = d3.axisBottom()
            .scale(x)

        const yAxis = d3.axisLeft()
            .scale(y)

        const defaultSelection = [x(d3.timeDay.offset(x.domain()[1], -1)), x.range()[1]];

        const brush = d3.brushX()
            .extent([0, chartWidth])
            .on("brush", brushed)
            // .on("end", brushended);

        let gb = svg.append("g")
            .attr('id', 'gb')
            .call(brush)
            .call(brush.move, defaultSelection);

        function brushed(selection) {
            if (selection) {
                svg.property("value", selection.map(x.invert, x).map(parseDate));
                svg.dispatch("input");
            }
        }

        // function brushended(selection) {
        //     if (!selection) {
        //         gb.call(brush.move, defaultSelection);
        //     }
        // }

        svg.append("g")
            .call(xAxis, x, chartHeight);

        const area = d3.area()
            .x(d => x(parseDate(d.timestamp)))
            .y0(chartHeight)
            .y1(d => y(d.prediction));

        svg.selectAll('.area')
            .data(data)
            .enter()
            .append("g")
            .attr('class', 'area')
            .attr("fill", d => color(d.appliance))
            .attr("opacity", .4)
            .append("path")
            .datum(d => d.values)
            .attr('class', 'path')
            .attr('d', area);


    }, [])


    return (
        <div className="Area-Chart" id={props.id}
             ref={ref}
        />
    );
}

AreaChart.defaultProps = {

    containerMult: 0.9,
    heightMult: 0.7,
    widthMult: 0.8,

}

export default AreaChart;