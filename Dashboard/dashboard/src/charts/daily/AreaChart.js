import * as d3 from 'd3';
import React, { useRef, useEffect } from 'react';

function AreaChart(props){

    const ref = useRef();
    const data = props.data;

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
            // .attr('viewbox', `0 0 ${chartWidth} ${chartHeight}`);

        const appliances = [... new Set(data.map(d => d.appliance))]

        const color = d3.scaleOrdinal()
            .domain(appliances)
            .range(d3.schemeAccent);

        const x = d3.scaleTime()
            .range([0, chartWidth])
            .domain(d3.extent(data, function(d) { return parseDate(d.date); }));

        const y = d3.scaleLinear()
            .range([chartHeight, 0])
            .domain([0, d3.max(data.map(d=>d.usage)) + 10]);

        const xAxis = d3.axisBottom()
            .scale(x)

        const yAxis = d3.axisLeft()
            .scale(y)

        const area = d3.area()
            .curve(d3.curveMonotoneX)
            .x(function(d) { return x(parseDate(d.date)); })
            .y0(y(0))
            .y1(function(d) { return y(d.usage); });

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + chartHeight + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)

        let series = svg.selectAll('.series')
            .data(props.data)
            .enter()
            .append('g')
            .attr('class', 'series')

        let paths = series.selectAll('.path')
            .data(d => d.value)
            .enter()
            .append('path')
            .attr('id', d => console.log(x(d)))
            .attr('class', 'path')
            .attr('d', area)

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