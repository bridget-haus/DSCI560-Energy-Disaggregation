import * as d3 from "d3";
import React, {useRef, useEffect} from "react";

function BarChart(props) {

    const ref = useRef();
    const data = props.data;

    useEffect(() => {

        const container = d3.select(ref.current);

        const svg = container.append("svg")
            .attr("class", "Bar-Chart-Svg");

        const width = svg.style("width").slice(0,-2);
        const height = svg.style("height").slice(0,-2);
        const chartWidth = width * props.widthMult;
        const chartHeight = height * props.heightMult;

        svg.attr("viewbox", `0 0 ${width} ${height}`)

        const users = [... new Set(data.map(item =>item.user))]
        const appliances = [... new Set(data.map(item =>item.appliance))]

        const groups = d3.scaleBand()
            .domain(appliances)
            .range([0, chartWidth])

        const subGroups = d3.scaleBand()
            .domain(users)
            .range([0, groups.bandwidth()])
            .padding([chartWidth * 0.001])

        const y = d3.scaleLinear()
            .range([chartHeight, 0])
            .domain([0, d3.max(data.map(d=>d.usage)) + 10]);

        const color = d3.scaleOrdinal()
            .domain(users)
            .range(d3.schemeSet2)

        const xAxis = d3.axisBottom()
            .scale(groups)
            .tickSize(1);

        const yAxis = d3.axisLeft()
            .scale(y);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", `translate(${0}, ${chartHeight})`)
            .call(xAxis);

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
            .attr("width", subGroups.bandwidth())
            .attr("x", d => subGroups(d.user))
            .transition()
            .duration(400)
            .attr("y", d => y(d.usage))
            .attr("height", d => chartHeight - y(d.usage))
            .style("fill", d => color(d.user))

            // .on("mouseover", function(d) {
            //     d3.select(this).style("fill", d3.rgb(color(d.usage)).darker(2));
            // });

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
            .attr("cx", chartWidth)
            .attr("cy", function(d,i){ return (i + 1) * (chartHeight * 0.15)})
            .attr("r", chartHeight * 0.03)

        svg.selectAll(".legendLine")
            .append("text")
            .text(d => d)
            .attr("x", chartWidth + chartHeight * 0.07)
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

    heightMult: 0.9,
    widthMult: 0.8,

}


export default BarChart;