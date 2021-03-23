<template>
<div>
  <div id="cy"></div>
</div>
</template>

<script>
  /* eslint-disable */
import http from '../http-common.js';
import { ref } from 'vue';

function cytoExample(a) {
  var cy = cytoscape({
  container: document.getElementById('cy'),

  boxSelectionEnabled: false,
  autounselectify: true,

  style: cytoscape.stylesheet()
    .selector('node')
      .style({
        'content': function(ele) {return `${ele.data('id')}: ${ele.data('description')}`},
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

  name: 'Model Driven Graph',

  components: {
  },

  data() {

    http.get('get-derived-scores').then((r) => {

      console.log(r.data)
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
    });

    return {
      nodes,
      edges,
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
  left: 0;
  /* top: 0; */
  text-align: start;
}
</style>