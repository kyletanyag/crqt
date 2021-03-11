<template>
<div>
  <div class="row">
    <div class="col-5" id="networkContainer">
      <h3>Network Graph</h3>
      <svg id="network" :width="width" :height="height"></svg>
    </div>
    <div class="col-7">
      <h3>Network Data</h3>
      <table v-if="network" class="table table-hover" id="network-table">
        <thead style="display: block;">
          <tr>
            <th scope="col" style="width: 5%">ID</th>
            <th scope="col" style="width: 30%">Description</th>
            <th scope="col" style="width: 16.6%">Node Type</th>
            <th scope="col" style="width: 16.6%">Base Score</th>
            <th scope="col" style="width: 16.6%">Exploitability Score</th>
            <th scope="col" style="width: 16.6%">Impact Score</th>
            <th scope="col"></th>
          </tr>
        </thead> 
        <div :style="`overflow-y: auto; height: ${height}px;`">
          <tbody v-for="node in network.nodes" :key="node.id" 
            @mouseover="highlight(node.id)"
            @mouseleave="unhighlight(node.id)">
            <tr>
              <td style="width: 5%; word-wrap: anywhere;">{{ node.id }}</td>
              <td style="width: 30%; word-wrap: anywhere;">{{ node.discription }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ node.node_type}}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ node.base_score }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ node.exploitability_score }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ node.impact_score }}</td>
            </tr> 
          </tbody>
        </div>

      </table>
    </div>
  </div> 
</div>
</template>


<script>

import http from '../http-common.js';
import { generateNetworkDiagram } from '../utilities/network-graph.js';

export default {
  name: 'Network Graph',

  data() {
    return {
      network: {
        nodes: undefined,
        links: undefined,
      },
    }
  },

  components: {
  },

  props: {
    width: {
      type: Number,
      default: 600,
    },
    height: {
      type: Number,
      default: 600,
    },
  },

  methods: {
    highlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '20');
    },

    unhighlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '5');
    }
  },

  mounted() {
    http.get('get-derived-scores').then((r) => {
      this.network = { links: r.data.edges, nodes: r.data.nodes };
      generateNetworkDiagram(r.data);
    })
  }
}
</script>

<style>
</style>
