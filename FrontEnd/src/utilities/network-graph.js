/*global d3*/
/*eslint no-undef: "error"*/

function generateNetworkDiagram(data) {
    var svg = d3.select("#network"),
        width = +svg.attr("width"),
        height = +svg.attr("height");
  
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
  
  
    var color = d3.scaleOrdinal(d3.schemeCategory10);
    render(null, data);
  
  
    function render (error, graph) {
    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody().strength(-30))
        .force("center", d3.forceCenter(width / 2, height / 2));
  
  
      if (error) throw error;
  
        console.log(graph);
      var link = svg.append("g")
          .attr("class", "links")
          .attr("stroke", "#999")
        .selectAll("line")
        .data(graph.edges)
        .enter().append("line")
          .attr("stroke-width", function(d) { return Math.sqrt(d.value); })
          .attr('color', 'black')
          .attr('marker-end', 'url(#arrowhead)');
  
      var node = svg.append("g")
          .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
          .attr("r", 5)
          .attr("fill", function(d) { return color(d.node_type); })
          .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));
  
      node.append("title")
          .text(function(d) { return d.id; });
  
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
    }
  
    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }
  
    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    }
  }

export { generateNetworkDiagram };