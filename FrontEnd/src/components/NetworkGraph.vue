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
            <th @click="sort('id')" scope="col" style="width: 7.5%">ID<i :class="sortDirection('id')"></i></th>
            <th @click="sort('description')" scope="col" style="width: 30%">Description<i :class="sortDirection('description')"></i></th>
            <th @click="sort('node_type')" scope="col" style="width: 16.6%">Node Type<i :class="sortDirection('node_type')"></i></th>
            <th @click="sort('base_score')" scope="col" style="width: 16.6%">Base Score<i :class="sortDirection('base_score')"></i></th>
            <th @click="sort('exploitability_score')" scope="col" style="width: 16.6%">Exploitability Score<i :class="sortDirection('exploitability_score')"></i></th>
            <th @click="sort('impact_score')" scope="col" style="width: 16.6%">Impact Score<i :class="sortDirection('impact_score')"></i></th>
            <th scope="col"></th>
          </tr>
        </thead> 
        <div :style="`overflow-y: auto; height: ${height}px;`">
          <tbody v-for="node in sortedNodes" :key="node.id" 
            @mouseover="highlight(node.id)"
            @mouseleave="unhighlight(node.id)">
            <tr>
              <td style="width: 5%; word-wrap: anywhere;">{{ node.id }}</td>
              <td style="width: 30%; word-wrap: anywhere;">{{ node.description }}</td>
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
import http from '@/http-common.js';
import { generateNetworkDiagram } from '../utilities/network-graph.js';

export default {
  name: 'Network Graph',

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
      default: 600,
    },
    height: {
      type: Number,
      default: 600,
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
    http.get('data_driven/get_derived_scores').then((r) => {
      this.network = { links: r.data.edges, nodes: r.data.nodes };
      generateNetworkDiagram(r.data);
    })
  }
}
</script>

<style>
</style>
