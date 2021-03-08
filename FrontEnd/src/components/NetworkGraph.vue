<template>
<div>
  <h3>Network Graph</h3>
  <div class="row">
    <div class="col">
      <svg id="network" width="960" height="600"></svg>
    </div>
    <div class="col">
      <object-array-as-table 
        :data="network.nodes" 
        tableTitle="Network Data" />
    </div>
  </div>
</div>
</template>


<script>
/* eslint-disable */
// import * as d3 from 'd3';

function dothis(data) {
var svg = d3.select("#network"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);
render(null, data);


function render (error, graph) {

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
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
      .attr('color', 'black');

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
      .attr("r", 5)
      .attr("fill", function(d) { return color(d.group); })
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
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
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
};
}

import http from '../http-common.js';
import ObjectArrayAsTable from './ObjectArrayAsTable.vue';
export default {
  name: 'Network Graph',

  data() {
    return {
      network: {
        nodes: undefined,
        links: undefined,
      }
    }
  },

  components: {
    ObjectArrayAsTable,
  },

  methods: {
  },

  mounted() {
    http.get('get-derived-scores').then((r) => {
      this.network = { links: r.data.edges, nodes: r.data.nodes };
      dothis(r.data);
    });
  }
}
</script>
