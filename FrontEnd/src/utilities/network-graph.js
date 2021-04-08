/*global d3*/
/*eslint no-undef: "error"*/

function generateNetworkDiagram(data) {
  const svg = d3.select("#network"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

  var keys = ['Derived Fact', 'Derivation', 'Primitive Fact']

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  svg.selectAll("mydots")
  .data(keys)
  .enter()
  .append("circle")
    .attr("cx", 20)
    .attr("cy", function(d,i){ return 40 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
    .attr("r", 7)
    .style("fill", function(d){ return color(d)})

  // Add one dot in the legend for each name.
  svg.selectAll("mylabels")
    .data(keys)
    .enter()
    .append("text")
      .attr("x", 40)
      .attr("y", function(d,i){ return 40 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
      .style("fill", function(d){ return color(d)})
      .text(function(d){ return d})
      .attr("text-anchor", "left")
      .style("alignment-baseline", "middle")

    svg.append('defs').append('marker')
        .attrs({'id':'arrowhead',
            'viewBox':'-0 -5 10 10',
            'refX':13,
            'refY':0,
            'orient':'auto',
            'markerWidth':13,
            'markerHeight':13,
            'xoverflow':'visible'})
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke','none');
    
    render(null, data);
  
    function render (error, graph) {
      const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));
  
  
      if (error) throw error;
  
      console.log(graph);

      const link = svg.append("g")
          .attr("class", "links")
          .attr("stroke", "#999")
        .selectAll("line")
        .data(graph.edges)
        .enter().append("line")
          .attr("stroke-width", function(d) { return Math.sqrt(d.value); })
          .attr('color', 'black')
          .attr('marker-end', 'url(#arrowhead)');
  

      const nodeWrapper = svg.append('g')
        .attr('class', 'nodes')
        .selectAll('.node')
        .data(graph.nodes)
        .enter().append('g')
        .attr('class', 'nodeWrapper')

      const node = nodeWrapper
        .append("circle")
        .attr("r", 5)
        .attr("fill", function(d) { return color(d.node_type); })
        .attr("id", function(d) { return `node_${d.id}`; })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
      
      const tooltip = d3.select('#networkContainer')
        .append('div')
        .classed('tooltip', true)
        .style('opacity', 0);

      
      nodeWrapper
        .on("mouseover", function(d) {
          tooltip.transition()
            .duration(300)
            .style("opacity", 1) // show the tooltip
            .style('background-color', 'rgba(211, 211, 211, 0.8)')
          tooltip.html(`<div style="width: 300px">\
ID: ${d.id} <br>\
Description: ${d.description} <br>\
Type: ${d.node_type} <br>\
Base Score: ${d.base_score} <br>\
Exploitability Score: ${d.exploitability_score} <br>\
Impact Score ${d.impact_score}\
</div>`)
            .style("left", (d3.event.pageX - d3.select('.tooltip').node().offsetWidth + 350) + "px")
            .style("top", (d3.event.pageY - d3.select('.tooltip').node().offsetHeight - 100) + "px");
            // .style("top", (d3.select('.tooltip').node().offsetHeight) + "px");
        })
        .on("mouseleave", function() {
          tooltip.transition()
            .duration(0)
            .style("opacity", 0)
            .style('left', 0 + 'px')
            .style('top', 0 + 'px');
          tooltip.html('<div />')
        })
  
      // node.append("title")
      //     .text(function(d) { return d.id; });

      simulation
          .nodes(graph.nodes)
          .on("tick", () => {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
  
            node
                .attr("cx", function(d) { return d.x = Math.max(5, Math.min(width - 5, d.x)); })
                .attr("cy", function(d) { return d.y = Math.max(5, Math.min(height - 5, d.y)); });
          });
  
      simulation.force("link")
          .links(graph.edges);
  
  
    function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
      d3.select(this).classed('fixed', true);
    }
  
    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    //   d.fx = clamp(event.x, 0, width);
    //   d.fy = clamp(event.y, 0, height);
    //   simulation.alpha(1).restart();
    }
  
    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // function clamp(x, lo, hi) {
    //   return x < lo ? lo : x > hi ? hi : x;
    // }

    }
  }

export { generateNetworkDiagram };