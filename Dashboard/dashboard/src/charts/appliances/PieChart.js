import * as d3 from "d3";
import React, {useRef, useEffect} from "react";

function PieChart(props) {

    const ref = useRef();

    //TODO: Change to use context
    const data = props.data.filter(d => d.house === 'house_6');

    useEffect(() => {

        const parent = d3.select(props.container_id);
        const width = parent.style("width").slice(0,-2);
        const height = parent.style("height").slice(0,-2);

        const chartWidth = width * props.widthMult;
        const chartHeight = height * props.heightMult;

        const container = d3.select(ref.current);

        const svg = container.append("svg")
            .attr("class", "Pie-Chart-Svg")
            .attr('id', props.svg_id)
            .attr('width', width)
            .attr('height', chartHeight);


        const appliances = [... new Set(data.map(item =>item.appliance))]

        const color = d3.scaleOrdinal()
            .domain(appliances)
            .range(d3.schemeSet2)

        function update(data) {

            let radius = Math.min(chartWidth, chartHeight) / 2.5
            // Compute the position of each group on the pie:
            let piece = d3.pie()
                .value(function(d) {return d.usage; })
                .sort(function(a, b) {return d3.ascending(a.key, b.key);} ) // This make sure that group order remains the same in the pie chart

            // map to data
            let pie = svg.append('g')
                .attr('transform', `translate(${chartWidth/2}, ${chartHeight/2.5})`)
                .selectAll("path")
                .data(piece(data))

            let text;
            // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
            pie
                .enter()
                .append('path')
                .attr('class', 'pie-piece')
                .merge(pie)
                .transition()
                .duration(1000)
                .attr('d', d3.arc()
                    .innerRadius(0)
                    .outerRadius(radius)
                )
                .attr('fill', function(d){ return(color(d.data.appliance)) })
                .attr("stroke", "white")
                .attr("opacity", 0.8);

            d3.selectAll('.pie-piece')
                .on("mouseover", function(d) {

                    let mouse = d3.event.target;
                    text = pie.append("text")
                        .attr("x", mouse.x)
                        .attr("y", mouse.y)
                        .style("text-anchor", "middle")
                        .style("fill", "blue")
                        .attr("class", "on")
                        .text(d.data.usage);
                })

                .on("mouseout", function(d) {
                    text.remove();
                });

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
                .attr("cx", chartWidth * 0.75)
                .attr("cy", function(d,i){ return (i + 1) * (chartHeight * 0.15)})
                .attr("r", chartHeight * 0.015)

            svg.selectAll(".legendLine")
                .append("text")
                .text(d => d.appliance)
                .attr("x", chartWidth * 0.78)
                .attr("y", function(d,i){ return (i + 1) * (chartHeight * 0.15)})
                .attr("text-anchor", "left")
                .attr("fill", d => color(d.appliance))
                .style("alignment-baseline", "middle")
                .attr("font-size", chartHeight * 0.07)
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

    heightMult: 1,
    widthMult: 0.9,

}


export default PieChart;