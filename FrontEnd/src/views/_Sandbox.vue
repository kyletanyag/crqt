<template>
<div>
  <!-- <network-graph></network-graph> -->
  <div class="col" style="height: 500px;">
    <div id="cy"></div>
  </div>
  <div class="col">hello</div>
  <!-- <div id="example"></div> -->
</div> 
</template>

<script>
  /* eslint-disable */
import NetworkGraph from '../components/NetworkGraph.vue';
import http from '../http-common.js';
import { ref } from 'vue';
import Handsontable from "handsontable";
import 'handsontable/dist/handsontable.full.css';

function hotExample(data) {
  const container = document.getElementById('example');
  const hot = new Handsontable(container, {
    data: data,
    rowHeaders: true,
    colHeaders: true,
    filters: true,
    dropdownMenu: true,
  });  
  document.getElementById('hot-display-license-info').innerHTML = "";
};

function cytoExample(a) {
  var cy = cytoscape({
  container: document.getElementById('cy'),

  boxSelectionEnabled: false,
  autounselectify: true,

  style: cytoscape.stylesheet()
    .selector('node')
      .style({
        'content': function(ele) {return `${ele.data('id')}: ${ele.data('description')}`},
        'style': {'height': '1px', 'width': '2px'}
        // 'background-color': function(ele) {return getColor(ele.data('node_type'))}
      })
    .selector('edge')
      .style({
        'curve-style': 'bezier',
        'target-arrow-shape': 'triangle',
        'width': 4,
        'line-color': '#ddd',
        'target-arrow-color': '#ddd'
      })
    .selector('.highlighted')
      .style({
        'background-color': '#61bffc',
        'line-color': '#61bffc',
        'target-arrow-color': '#61bffc',
        'transition-property': 'background-color, line-color, target-arrow-color',
        'transition-duration': '0.5s'
      }),

  layout: {
    name: 'breadthfirst',
    directed: true,
    roots: '#a',
    padding: 10
  }
});

cy.ready(() => {
  cy.add(a);
})

var bfs = cy.elements().bfs('#15', function(){}, true);
console.log(bfs);
var i = 0;
var highlightNextEle = function(){
  if( i < bfs.path.length ){
    bfs.path[i].addClass('highlighted');

    i++;
    setTimeout(highlightNextEle, 500);
  }
};

// kick off first highlight
highlightNextEle();

cy.userZoomingEnabled(false);

function getColor(type) {

  if (type === 'Derived Fact') {
    return 'green';
  } else if (type === 'Derivation') {
    return 'blue';
  } else {
    return 'orange';
  }
}
};

export default {

  name: 'Sandbox',

  components: {
    NetworkGraph,
  },

  data() {
    
    const nodes = ref([]);
    const edges = ref([]);

    http.get('get-derived-scores').then((r) => {

      console.log(r.data)
      nodes.value = r.data.nodes;
      edges.value = r.data.edges;
      var array = [];
      var x = 100;
      var y = 100;
      var i = 0;
      var j = 1;

      r.data.nodes.forEach((e) => {
        array.push({group: 'nodes', data: e, position: {x: x, y: y}})
        if (i%3) {
          x += 100;
        }
        if (j%5) {
          y += 100;
        }
        i++;
        j++;
      });

      let id = 100
      r.data.edges.forEach((j) => {
        array.push({group: 'edges', data:{weight: 1, source: j.source, target: j.target, id: id}})
        id++;
      });

      
      cytoExample(array);
      // hotExample(r.data.nodes);
    });

    return {
      nodes,
      edges,
      params: {
        data: [
          ['Cell-1', 'Cell-2', 'Cell-3'],
          ['Cell-4', 'Cell-5', 'Cell-6'],
          ['Cell-7', 'Cell-8', 'Cell-9']
        ]
      }
    };
  },

  mounted() {
  },
}
</script>

<style>
#cy {
  height: 100%;
  width: 100%;
  position: absolute;
  /* left: 0; */
  /* top: 0; */
  text-align: start;
}
</style>