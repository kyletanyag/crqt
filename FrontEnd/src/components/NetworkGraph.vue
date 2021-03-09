<template>
<div>
  <h3>Network Graph</h3>
  <div class="row">
    <div class="col">
      <svg id="network" width="960" height="600"></svg>
    </div>
    <!-- <div class="col">
      <object-array-as-table 
        :data="network.nodes" 
        tableTitle="Network Data" />
    </div> -->
  </div>
</div>
</template>


<script>
/* eslint-disable */
// import * as d3 from 'd3';


import http from '../http-common.js';
import ObjectArrayAsTable from './ObjectArrayAsTable.vue';
import { generateNetworkDiagram } from '../utilities/network-graph.js';

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
      generateNetworkDiagram(r.data);
    });
  }
}
</script>
