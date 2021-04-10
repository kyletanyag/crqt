<template>
<div>
  <div class="container">
    <div id="networkContainer">
      <h3>Network Graph</h3>
      <svg id="network" :width="width" :height="height"></svg>
    </div>
  </div> 
</div>
</template>


<script>
import http from '@/http-common.js';
import { generateModelDrivenNetworkDiagram } from '../utilities/network-graph.js';

export default {
  name: 'Model Driven Network Graph',

  data() {
    return {
      network: {
        nodes: undefined,
        links: undefined,
      },
      currentSort: 'id',
      currentSortDir: 'asc',
    }
  },

  computed: {
    sortedNodes() {
      if (!this.network.nodes) return 0;
      return this.network.nodes.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    },
  },

  components: {
  },

  props: {
    width: {
      type: Number,
      default: 1000,
    },
    height: {
      type: Number,
      default: 1000,
    },
  },

  methods: {
    highlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '10');
    },

    unhighlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '5');
    },

    sort(s) {
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir ==='asc' ? 'desc':'asc';
      }
      this.currentSort = s;
    },

    sortDirection(s) {
      if (this.currentSortDir === 'asc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-asc';
      else if (this.currentSortDir === 'desc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-desc';
      else
        return 'fa fa-fw fa-sort';
    }
  },

  mounted() {
    http.get('/model_driven/get_network_topology').then((r) => {
      this.network = { links: r.data.edges, nodes: r.data.nodes };
      generateModelDrivenNetworkDiagram(r.data);
    })
  }
}
</script>

<style>
</style>
