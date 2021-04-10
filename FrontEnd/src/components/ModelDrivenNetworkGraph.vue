<template>
<div class="row">
  <div class="col">
    <div id="networkContainer">
      <h2>Network Graph</h2>
      <svg id="network" :width="width" :height="height"></svg>
    </div>
  </div> 
  <div class="col">
    <div class="row-12">
      <h2>Network Data</h2>
      <table v-if="network" class="table table-hover">
        <div :style="`overflow-y: auto; height: ${height/2}px;`">
          <thead>
            <tr>
              <th @click="sort('target.id')" scope="col" style="width: 7.5%">ID<i :class="sortDirection('id')"></i></th>
              <th @click="sort('target.layer')" scope="col" style="width: 15%">Layer<i :class="sortDirection('layer')"></i></th>
              <th @click="sort('target.vendor')" scope="col" style="width: 16.6%">Product<i :class="sortDirection('product')"></i></th>
              <th @click="sort('target.product')" scope="col" style="width: 16.6%">Vendor<i :class="sortDirection('vendor')"></i></th>
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
        </div>
      </table>
    </div>
    <div class="col-12 mt-4 text-left">
      Which node are you interested in analyzing? ID:
      <input type="number" v-model.number="desiredNodeID" :max="lastNodeID" min="1" maxlength="2"
        onkeyup="if(this.value > max) this.value = max; else if(this.value < 0) this.value = 0;"
        @change="getAttackPaths(desiredNodeID)"
      > 
      <div class="row pt-2">
        <div v-if="desiredNodeID > 0 && desiredNodeID <= lastNodeID ** !loading" class="col-6">
        <h2>Attack Path Averages</h2>
          <p class="text-left">
            Computation Time: <strong>{{ compTime }}</strong>
            <br>
            Number of Attack Paths: <strong>{{ numPaths }}</strong>
            <br>
            Average Base Score Cost: <strong>{{ avgBasScore }}</strong>
            <br>
            Average Exploitability Score Cost: <strong>{{ avgExpScore }}</strong>
            <br>
            Average Impact Score Cost: <strong>{{ avgImpScore }}</strong>
          </p>
        </div>
        <div class="col-6 pt-2 text-center">
          <h2>Attack Path Data</h2>
          <table v-if="paths && desiredNodeID > 0 && desiredNodeID " class="table table-hover">
            <div :style="`overflow-y: auto; height: ${height/4}px;`">
              <thead>
                <tr>
                  <th @click="sort('path')" scope="col" style="width: 20%">Path<i :class="sortDirection('path')"></i></th>
                  <th @click="sort('base_score')" scope="col" style="width: 25%">Base Score<i :class="sortDirection('base_score')"></i></th>
                  <th @click="sort('exploitability_score')" scope="col" style="width: 30%">Exploitability Score<i :class="sortDirection('exploitability_score')"></i></th>
                  <th @click="sort('impact_score')" scope="col" style="width: 25%">Impact Score<i :class="sortDirection('impact_score')"></i></th>
                </tr>
              </thead> 
              <tbody>
                <tr v-for="p in sortedPaths" :key="p.path">
                  <td style="width: 20%">{{ p.path }}</td>
                  <td style="width: 25%">{{ p.base_score }}</td>
                  <td style="width: 30%">{{ p.exploitability_score }}</td>
                  <td style="width: 25%">{{ p.impact_score }}</td>
                </tr> 
              </tbody>
            </div>
          </table>
        </div>
      </div>
      <div class="row pt-2">
        <div class="col text-center">
          <h2>Top Exploitable</h2>
          <table v-if="paths && desiredNodeID > 0 && desiredNodeID " class="table table-hover">
            <div :style="`overflow-y: auto; height: ${height/4}px;`">
              <thead>
                <tr>
                  <th scope="col" style="width: 40%">Path</th>
                  <th scope="col" style="width: 33%">Node List</th>
                  <th scope="col" style="width: 33%">Ranking</th>
                </tr>
              </thead> 
              <tbody>
                <tr v-for="(p, idx) in topExpPaths" :key="p.path"              
                  @mouseover="highlightPath(p.nodes)"
                  @click="toggleHighlightPath(p.nodes)"
                  @mouseleave="unhighlightPath(p.nodes)"
                >
                  <td style="width: 40%">{{ p.path }}</td>
                  <td style="width: 33%">{{ p.nodes }}</td>
                  <td style="width: 33%">{{ idx }}</td>
                </tr> 
              </tbody>
            </div>
          </table>
        </div>
        <div class="col text-center">
          <h2>Top Impactful</h2>
          <table v-if="paths && desiredNodeID > 0 && desiredNodeID " class="table table-hover">
            <div :style="`overflow-y: auto; height: ${height/4}px;`">
              <thead>
                <tr>
                  <th scope="col" style="width: 40%">Path</th>
                  <th scope="col" style="width: 33%">Node List</th>
                  <th scope="col" style="width: 33%">Ranking</th>
                </tr>
              </thead> 
              <tbody>
                <tr v-for="(p, idx) in topImpPaths" :key="p.path"              
                  @mouseover="highlightPath(p.nodes)"
                  @mouseleave="unhighlightPath(p.nodes)"
                >
                  <td style="width: 40%">{{ p.path }}</td>
                  <td style="width: 33%">{{ p.nodes }}</td>
                  <td style="width: 33%">{{ idx }}</td>
                </tr> 
              </tbody>
            </div>
          </table>
        </div>
      </div>
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
      edges: [],
      currentSort: 'id',
      currentSortDir: 'asc',
      desiredNodeID: 0,
      lastNodeID: 0,
      loading: true,
      numPaths: 0,
      avgBasScore: 0,
      avgExpScore: 0,
      avgImpScore: 0,
      compTime: 0,
      paths: [],
      topExpPaths: [],
      topImpPaths: [],
      selected: [],
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

    sortedPaths() {
      if (!this.paths) return 0;
      return this.paths.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    }
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
      document.getElementById(`node_${id}`).setAttribute('r', '20');
      document.getElementById(`node_${id}`).setAttribute('stroke', 'black');
    },

    unhighlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '15');
      document.getElementById(`node_${id}`).setAttribute('stroke', 'white');
    },

    highlightPath(a) {
      a.forEach((x) => {this.highlight(x)});
      this.highlight(0);
    },

    unhighlightPath(a) {
      if (a != this.selected) {
        a.forEach((x) => {this.unhighlight(x)});
        this.unhighlight(0);
      }
    },

    toggleHighlightPath(a) {
      if (this.selected != a) {
        a.forEach((x) => { this.highlight(x);});
        this.highlight(0);
        this.selected = a;
      } else {
        var ids = [...Array(this.lastNodeID).keys()]
        ids.forEach((x) => {this.unhighlight(x);});
        this.selected = null;
      }
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

    getAttackPaths(ap) {
      this.loading = true;
      http.get(`/model_driven/attack_paths/${ap}`).then((r) => {
        console.log(r);

        this.numPaths = r.data.number_attack_paths;
        this.avgBasScore = r.data.averge_length_attack_paths[0];
        this.avgExpScore= r.data.averge_length_attack_paths[1];
        this.avgImpScore = r.data.averge_length_attack_paths[2];
        this.compTime = Number(r.data.computation_time.toPrecision(3));
        this.paths = r.data.metrics_per_path;
        this.topExpPaths = r.data.top_exploitable;
        this.topImpPaths = r.data.top_impactful;
        this.loading = false;
      })
    }
  },

  mounted() {
    http.get('/model_driven/get_network_topology').then((r) => {
      console.log(r);
      
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

      this.lastNodeID = Math.max.apply(Math, r.data.nodes.map(function(o) { return o.id; }));
      generateModelDrivenNetworkDiagram(r.data);
    });
  },

  watch: {
    desiredNodeID() {
      if (this.desiredNodeID > this.lastNodeID) this.desiredNodeID = this.lastNodeID;
      if (this.desiredNodeID < 1) this.desiredNodeID = null;
    }
  }
}
</script>

<style>
h {
  color: orange;
}
</style>
