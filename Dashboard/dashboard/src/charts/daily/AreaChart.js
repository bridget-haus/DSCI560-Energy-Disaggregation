import * as d3 from 'd3';
import React, { useRef, useEffect } from 'react';

function AreaChart(props){

    const ref = useRef();

    const areaDefaultOpacity = 0.4
    const data = d3.entries(props.data)
        .filter(d => d.key === 'house_6')
        .map(d => d.value)[0];

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
            .attr('height', height * props.containerMult);

        const appliances = data.map(d => d.appliance);
        const values = data.map(d => d.values);

        const color = d3.scaleOrdinal()
            .domain(appliances)
            .range(d3.schemeSet2);

        const x = d3.scaleTime()
            .range([0, chartWidth * 5])
            .domain(d3.extent(values.map(eachList => eachList.map(d => parseDate(d.timestamp)))[0]));

        const y = d3.scaleSqrt()
            .range([chartHeight, 0])
            .domain([10, d3.max(values.map(eachList => d3.max(eachList.map( d=>d.prediction)))) + 10]);

        const xAxis = d3.axisBottom()
            .scale(x)
            .ticks(d3.timeMinute.every(60))

        const yAxis = d3.axisLeft()
            .scale(y)
            .ticks(0)
        
        const xaxis = svg.append("g")
            .call(xAxis, x, chartHeight)
            .attr('class', 'xaxis')
            .attr('transform', `translate (${0}, ${chartHeight})`);

        const area = d3.area()
            .x(d => x(parseDate(d.timestamp)))
            .y0(chartHeight)
            .y1(d => y(d.prediction));

        // Set the zoom and Pan features: how much you can zoom, on which part, and what to do when there is a zoom
        var zoom = d3.zoom()
            .scaleExtent([0, 10])  // This control how much you can unzoom (x0.5) and zoom (x20)
            .extent([[0, 0], [chartWidth, chartHeight]])
            .on("zoom", () => {
                const scaleX = d3.event.transform.rescaleX(x);
                xaxis.call(xAxis.scale(scaleX));
                const newArea = d3.area()
                    .x(d => scaleX(parseDate(d.timestamp)))
                    .y0(chartHeight)
                    .y1(d => y(d.prediction));
                usage.attr('d', newArea);
            });

        // This add an invisible rect on top of the chart area. This rect can recover pointer events: necessary to understand when the user zoom

        const tooltip = svg.append('g')
            .attr('class', 'tooltip')

        let tooltipRect = tooltip.append('rect')
            .attr('opacity', 0);
        let tooltipText = tooltip.append('text')
            .attr('opacity', 0);

        const usage = svg.selectAll('.area')
            .data(data)
            .enter()
            .append("g")
            .attr('class', 'area')
            .attr('id', d => d.appliance)
            .attr('fill', d => color(d.appliance))
            .attr("opacity", areaDefaultOpacity)
            .on('mousemove', (d, i) => {

                let coord = d3.mouse(d3.event.target);
                let [xCoord, yCoord] = coord;
                const mouseDate = x.invert(xCoord);

                let bisect = d3.bisector(v => parseDate(v.timestamp)).right;
                let xIndex = bisect(d.values, mouseDate, 1);
                const mousePrediction = d.values[xIndex].prediction;

                d3.select('#'+d.appliance)
                    .attr('opacity', 0.6)
                    .attr('stroke', '#ffffff')
                    .attr('stroke-width', '.2em')

                tooltip.raise()
                    .classed("active", true);

                tooltipRect
                    .raise()
                    .attr("rx", 6)
                    .attr("ry", 6)
                    .attr('fill', '#CCCCCC')
                    .attr('opacity', .7)

                let predictionText = d3.format(".2s")(mousePrediction)
                tooltipText
                    .raise()
                    .attr('alignment-baseline', 'mathematical')
                    .attr('opacity', 1)
                    .attr('x', coord[0])
                    .attr('y',y(mousePrediction))
                    .text(`${d.appliance}: ${predictionText}w`)

                let bbox = tooltipText.node().getBBox()
                tooltipRect
                    .attr('width', bbox.width + 20)
                    .attr('height', 25)
                    .attr('x', bbox.x - 10)
                    .attr('y',bbox.y);
            })
            .on('mouseout', d => {

                d3.select('#'+d.appliance)
                    .attr("opacity", areaDefaultOpacity)
                    .attr('stroke-width', '0')
                    .lower();

                tooltipText.attr('opacity', 0)
                tooltipRect.attr('opacity', 0)

            })
            .append("path")
            .datum(d => d.values)
            .attr('class', 'path')
            .attr('d', area);

        svg.call(zoom);

    }, [])


    return (
        <div className="Area-Chart" id={props.id}
             ref={ref}
        />
    );
}

AreaChart.defaultProps = {

    containerMult: 0.9,
    heightMult: 0.8,
    widthMult: 0.8,

}

export default AreaChart;