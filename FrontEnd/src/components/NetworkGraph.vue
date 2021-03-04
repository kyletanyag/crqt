<template>
<div v-if="data">
  <h3>Network Graph</h3>
  <button @click="click">Click here!</button>
  <div id="my_dataviz"></div>
</div>
</template>

<script>
import * as d3 from 'd3';
/* eslint-disable */


const render = (data) => {
  console.log(data);
const margin = {top: 100, right: 30, bottom: 30, left: 40},
  width = 400 - margin.left - margin.right,
  height = 400 - margin.top - margin.bottom;
  
  var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

  var link = svg
      .selectAll("line")
      .data(data.links)
      .enter()
      .append("line")
        .style("stroke", "#aaa")

    // Initialize the nodes
    var node = svg
      .selectAll("circle")
      .data(data.nodes)
      .enter()
      .append("circle")
        .attr("r", 20)
        .style("fill", "#69b3a2")

  var simulation = d3.forceSimulation(data.nodes)                 // Force algorithm is applied to data.nodes
      .force("link", d3.forceLink()                               // This force provides links between nodes
            .id(function(d) { return d.id; })                     // This provide  the id of a node
            .links(data.links)                                    // and this the list of links
      )
      .force("charge", d3.forceManyBody().strength(-400))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
      .force("center", d3.forceCenter(width / 2, height / 2))     // This force attracts nodes to the center of the svg area
      .on("end", ticked);  


function ticked() {
  console.log('here!')
  link
    .attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });

  node
    .attr("cx", function (d) { return d.x+6; })
    .attr("cy", function(d) { return d.y-6; });
}
};



export default {
  name: 'Network Graph',

  data() {
    return {
    };
  },

  props: {
    data: {
      type: Object,
      required: true,
    }
  },

  created() {
    if (this.data)
    { render(this.data)};
  },

  methods: {
    click() {
      render(this.data);
    }
  },

}


</script>
<style>
  
</style>