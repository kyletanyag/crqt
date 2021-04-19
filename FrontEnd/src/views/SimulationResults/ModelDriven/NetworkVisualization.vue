<template>
<div class="mb-5">
  <result-header 
    title="Network Visualization"
    nextPage="Model Driven Results - Graph Metrics"
    prevPage="Model Driven Results - Summary"
    defaultPage="Model Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="row mx-5 text-left">
    <div>
      <h2>Instructions</h2>
      <p>
        Below contains a graph representation of your network following the NIST's control
        system security recommended architecture. Alongside the graph is a data table containing
        all the network edge data such as node ID, layer, product, vendor, base, exploitability,
        and impact scores. The scores in the table represent the CVSS score needed to access into 
        that node and because all the incoming edges to a node have the same score, the data table
        reflects only the nodes in the network.
        <br><br>
        On the network graph, you can hover over a node to get specific information about that node or 
        you can hover an edge to get the scores associated to getting to that node. Futhermore, you
        can hover over a row in the network table and the corresponding node in the network graph will
        be highlighted.
      </p>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <network-graph></network-graph>
    </div>
    <div class="col">
      <div class="row-12 my-2">
        <h2>Network Edge Data</h2>
        <div :style="`overflow-y: auto; height: 800px;`">
          <table v-if="network" class="table table-hover">
            <thead>
              <tr>
                <th @click="sort('target.id')" scope="col" style="width: 7.5%">ID<i :class="sortDirection('id')"></i></th>
                <th @click="sort('layer')" scope="col" style="width: 15%">Layer<i :class="sortDirection('layer')"></i></th>
                <th @click="sort('product')" scope="col" style="width: 16.6%">Product<i :class="sortDirection('product')"></i></th>
                <th @click="sort('vendor')" scope="col" style="width: 16.6%">Vendor<i :class="sortDirection('vendor')"></i></th>
                <th @click="sort('base_score')" scope="col" style="width: 16.6%">Base Score<i :class="sortDirection('base_score')"></i></th>
                <th @click="sort('exploitability_score')" scope="col" style="width: 16.6%">Exploitability Score<i :class="sortDirection('exploitability_score')"></i></th>
                <th @click="sort('impact_score')" scope="col" style="width: 16.6%">Impact Score<i :class="sortDirection('impact_score')"></i></th>
              </tr>
            </thead> 
            <tbody>
              <tr v-for="edge in sortedEdges" :key="edge.id"              
                @mouseover="highlight(edge.id)"
                @mouseleave="unhighlight(edge.id)"
              >
                <td style="width: 5%; word-wrap: anywhere;">{{ edge.id }}</td>
                <td style="width: 15%; word-wrap: anywhere;">{{ edge.layer }}</td>
                <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.vendor }}</td>
                <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.product }}</td>
                <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.base_score }}</td>
                <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.exploitability_score }}</td>
                <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.impact_score }}</td>
              </tr> 
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
import ResultHeader from '@/components/ResultHeader.vue';
import NetworkGraph from '@/components/ModelDrivenNetworkGraph.vue';
export default {
  name: 'Model Driven Results - Network Visualization',

  components: {
    ResultHeader,
    NetworkGraph
  },

  data() {
    return {
      network: {
        nodes: undefined,
        links: undefined,
      },
      edges: [],
      currentSort: 'id',
      currentSortDir: 'asc',
    }
  },

  computed: {
    sortedEdges() {
      if (!this.edges) return 0;
      return this.edges.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    },
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      http.get('/model_driven/get_network_topology').then((r) => {        
        this.network = { links: r.data.edges, nodes: r.data.nodes };
        var unique = [];
        r.data.edges.forEach((e) => {
          var n = r.data.nodes.filter((x) => x.id === e.target)[0];
          if (!unique.includes(n.id)) {
            this.edges.push({
              id: n.id,
              layer: n.layer,
              vendor: n.vendor,
              product: n.product,
              base_score: e.base_score,
              exploitability_score: e.exploitability_score,
              impact_score: e.impact_score
            });
            unique.push(n.id);
          }
        });
      });
    },

    highlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '20');
      document.getElementById(`node_${id}`).setAttribute('stroke', 'black');
    },

    unhighlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '15');
      document.getElementById(`node_${id}`).setAttribute('stroke', 'white');
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
    },
  },
}
</script>
<style>
</style>