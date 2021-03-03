<template>
<div>
  <button class="btn btn-primary" @click="runme"></button>
  <svg id="viz_area" height=200 width=450></svg>
</div>
</template>

<script>
import * as d3 from 'd3';
// const d = {
//   'nodes': [
//     {
//       'id': 1
//     },
//     {
//       'id': 2
//     },
//     {
//       'id': 3
//     }
//   ],
//   'edges': [
//     {
//       'source': 1,
//       'target': 2,
//     },
//     {
//       'source': 2,
//       'target': 3,
//     }
//   ]
// }

const test = () => {
var svg = d3.select("#viz_area");

var x = d3.scaleLinear()
.domain([0, 100])         // This is the min and the max of the data: 0 to 100 if percentages
.range([0, 400]); 

svg.append("circle")
  .attr("cx", x(10))
  .attr("cy", 100)
  .attr("r", 40)
  .style("fill", "blue");

svg.append("circle")
  .attr("cx", x(50)).attr("cy", 100).attr("r", 40).style("fill", "red");
svg.append("circle")
  .attr("cx", x(100)).attr("cy", 100).attr("r", 40).style("fill", "green");

console.log(svg);
}


export default {
  name: 'Network Graph',

  // props: {
  //   data: {
  //     type: Array,
  //     required: true,
  //   }
  // }

  created() {
    test();
  },

  methods: {
    runme() {
      test();
    }
  },
}


</script>
<style>
  
</style>