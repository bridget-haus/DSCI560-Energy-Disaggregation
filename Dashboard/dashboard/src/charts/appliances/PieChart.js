import * as d3 from "d3";
import React, {useRef, useEffect} from "react";

function PieChart(props) {

    const ref = useRef();

    //TODO: Change to use context
    const data = props.data.filter(d => d.house === 'house_6');

    useEffect(() => {

        const container = d3.select(ref.current);

        const svg = container.append("svg")
            .attr("class", "Pie-Chart-Svg");

        const width = svg.style("width").slice(0,-2);
        const height = svg.style("height").slice(0,-2);
        const chartWidth = width * props.widthMult;
        const chartHeight = height * props.heightMult;

        svg.attr("viewbox", `0 0 ${width} ${height}`)

        const appliances = [... new Set(data.map(item =>item.appliance))]

        const color = d3.scaleOrdinal()
            .domain(appliances)
            .range(d3.schemeSet2)

        function update(data) {

            let radius = Math.min(chartWidth, chartHeight) / 2
            // Compute the position of each group on the pie:
            let piece = d3.pie()
                .value(function(d) {return d.usage; })
                .sort(function(a, b) {return d3.ascending(a.key, b.key);} ) // This make sure that group order remains the same in the pie chart

            // map to data
            let pie = svg.append('g')
                .attr('transform', `translate(${chartWidth/3}, ${chartHeight/2})`)
                .selectAll("path")
                .data(piece(data))

            // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
            pie
                .enter()
                .append('path')
                .merge(pie)
                .transition()
                .duration(1000)
                .attr('d', d3.arc()
                    .innerRadius(0)
                    .outerRadius(radius)
                )
                .attr('fill', function(d){ return(color(d.data.appliance)) })
                .attr("stroke", "white")
                .style("stroke-width", "2px")
                .style("opacity", 1)

            svg.append("g")
                .attr("class", "legend")
                .selectAll(".legend")
                .data(data)
                .enter()
                .append("g")
                .attr("class", "legendLine")
                .append("circle")
                .attr("class", "legendDots")
                .attr("fill", d => color(d.appliance))
                .attr("cx", chartWidth * 0.8)
                .attr("cy", function(d,i){ return (i + 1) * (chartHeight * 0.15)})
                .attr("r", chartHeight * 0.03)

            svg.selectAll(".legendLine")
                .append("text")
                .text(d => d.appliance)
                .attr("x", chartWidth * 0.9)
                .attr("y", function(d,i){ return (i + 1) * (chartHeight * 0.15)})
                .attr("text-anchor", "left")
                .attr("fill", d => color(d.appliance))
                .style("alignment-baseline", "middle")
                .attr("font-size", chartHeight * 0.1)
            // remove the group that is not present anymore
            pie
                .exit()
                .remove()

        };

        update(data);


    }, [])


    return (
        <div className="Pie-Chart" id={props.id}
             ref={ref}
        />
    )
}


PieChart.defaultProps = {

    heightMult: 0.9,
    widthMult: 0.8,

}


export default PieChart;