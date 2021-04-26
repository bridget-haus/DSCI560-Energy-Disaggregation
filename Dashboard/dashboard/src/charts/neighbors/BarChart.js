import * as d3 from "d3";
import React, {useRef, useEffect} from "react";

function BarChart(props) {

    const ref = useRef();
    const data = props.data;

    useEffect(() => {

        const parent = d3.select(props.container_id);
        const width = parent.style("width").slice(0,-2);
        const height = parent.style("height").slice(0,-2);

        const chartWidth = width * props.widthMult;
        const chartHeight = height * props.heightMult;
        const chartMargin = chartWidth * 0.001;

        const container = d3.select(ref.current);

        const svg = container.append("svg")
            .attr("class", "Bar-Chart-Svg")
            .attr('transform', `translate(${chartMargin}, ${0})`)
            .attr('id', props.svg_id)
            .attr('width', chartWidth)
            .attr('height', chartHeight);

        const users = [... new Set(data.map(item =>item.house))]
        const appliances = [... new Set(data.map(item =>item.appliance))]

        const groups = d3.scaleBand()
            .domain(appliances)
            .range([0, chartWidth * 0.8])

        const subGroups = d3.scaleBand()
            .domain(users)
            .range([0, groups.bandwidth()])
            .padding([chartWidth * 0.0005])

        const y = d3.scaleSqrt()
            .range([chartHeight - chartMargin, 0])
            .domain([0, d3.max(data.map(d=>d.usage)) + 10]);

        const color = d3.scaleOrdinal()
            .domain(users)
            .range(d3.schemeSet2)

        const xAxis = d3.axisBottom()
            .scale(groups)
            .tickSize(1);

        const yAxis = d3.axisLeft()
            .scale(y);

        let tooltip = svg.append('g');
        let tooltipText = tooltip.append('text');

        svg.append("g")
            .attr("class", "x axis")
            .attr('fill', 'black')
            .attr("transform", `translate(${0}, ${chartHeight*0.95})`)
            .call(xAxis)


        svg.append("g")
            .attr("class", "y axis")
            .attr('opacity', 0)
            .call(yAxis);

        let slice = svg.selectAll(".slice")
            .data(data)
            .enter().append("g")
            .attr("class", "slice")
            .attr("transform", function(d) { return `translate(${groups(d.appliance)},0)`; })
            .append("rect")
            .attr('class', 'bar')
            .attr("width", subGroups.bandwidth())
            .attr("x", d => subGroups(d.house))
            .transition()
            .duration(400)
            .attr("y", d => y(d.usage))
            .attr("height", d => chartHeight * 0.95 - y(d.usage))
            .attr("fill", d => color(d.house))
            // .on('mouseenter', d => {
            //
            //     let mouse = d3.event.target;
            //     tooltipText
            //         .attr("x", d => subGroups(d.house))
            //         .attr('y', d => y(d.usage))
            //         .text(d => d.usage)
            // })


        svg.append("g")
            .attr("class", "legend")
            .selectAll(".legend")
            .data(users)
            .enter()
            .append("g")
            .attr("class", "legendLine")
            .append("circle")
            .attr("class", "legendDots")
            .attr("fill", d => color(d))
            .attr("cx", chartWidth * 0.8)
            .attr("cy", function(d,i){ return (i + 1) * (chartHeight * 0.15)})
            .attr("r", chartWidth * 0.01)

        svg.selectAll(".legendLine")
            .append("text")
            .text(d => d)
            .attr("x", chartWidth * 0.82)
            .attr("y", function(d,i){ return (i + 1) * (chartHeight * 0.15)})
            .attr("text-anchor", "left")
            .attr("fill", d => color(d))
            .style("alignment-baseline", "middle")
            .attr("font-size", chartHeight * 0.08)

    }, [])


    return (
        <div className="Bar-Chart" id={props.id}
            ref={ref}
        />
    )
}


BarChart.defaultProps = {

    heightMult: 0.8,
    widthMult: 0.7,

}


export default BarChart;