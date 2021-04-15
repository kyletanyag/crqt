<template>
<div>
  <result-header 
    title="Severity Display"
    nextPage="Model Driven Results - Recommendations"
    prevPage="Model Driven Results - Node Specific Metrics"
    defaultPage="Model Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="mx-5 row">
    <div class="col text-left">
      <div>
        <h2>Edge Severity Score Breakdown</h2>
        <p>
          Your inputted network contains a total of <strong>{{ edges.length }}</strong> edges. 
          The severity breakdown of each edge weight from the computed vulnerability graph is below.
        </p>
        <div class="py-2">
          <h5>For Base Scores:</h5>
          <strong>{{ highBase.length }}</strong> edges are marked as <strong>high</strong> severity. (Base Score &#8805; 0.7)
          <br><strong>{{ mediumBase.length }}</strong> edges are marked as <strong>medium</strong> severity. (0.4 &#8804; Base Score &lt; 0.7)
          <br><strong>{{ lowBase.length }}</strong> edges are marked as <strong>low</strong> severity. (Base Score &lt; 0.4)
        </div>
        <div class="py-2">
          <h5>For Exploitability Scores:</h5>
          <strong>{{ highExploitability.length }}</strong> edges are marked as <strong>high</strong> severity. (Exploitability Score &#8805; 0.7)
          <br><strong>{{ mediumExploitability.length }}</strong> edges are marked as <strong>medium</strong> severity. (0.4 &#8804; Exploitability Score &lt; 0.7)
          <br><strong>{{ lowExploitability.length }}</strong> edges are marked as <strong>low</strong> severity. (Exploitability Score &lt; 0.4)          
        </div>
        <div class="py-2">
          <h5>For Impact Scores:</h5>
          <strong>{{ highImpact.length }}</strong> edges are marked as <strong>high</strong> severity. (Impact Score &#8805; 0.7)
          <br><strong>{{ mediumImpact.length }}</strong> edges are marked as <strong>medium</strong> severity. (0.4 &#8804; Impact Score &lt; 0.7)
          <br><strong>{{ lowImpact.length }}</strong> edges are marked as <strong>low</strong> severity. (Impact Score &lt; 0.4)          
        </div>
      </div>
    </div>
    <div class="col">
      <h2>Network Edge Severity Table</h2>
      <table v-if="!loading" class="table table-hover">
        <div :style="`overflow-y: auto; height: 500px;`">
          <thead>
            <tr>
              <th @click="sort('source')" scope="col" style="width: 7.5%">Edge<i :class="sortDirection('source')"></i></th>
              <th @click="sort('base_score')" scope="col" style="width: 16.6%">Base Score<i :class="sortDirection('base_score')"></i></th>
              <th @click="sort('exploitability_score')" scope="col" style="width: 16.6%">Exploitability Score<i :class="sortDirection('exploitability_score')"></i></th>
              <th @click="sort('impact_score')" scope="col" style="width: 16.6%">Impact Score<i :class="sortDirection('impact_score')"></i></th>
            </tr>
          </thead> 
          <tbody>
            <tr v-for="edge in sortedEdges" :key="edge.id">
              <td style="width: 5%; word-wrap: anywhere;">({{ edge.source }}, {{edge.target}})</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.base_score }} / {{GetSeverity(edge.base_score)}}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.exploitability_score }} / {{GetSeverity(edge.exploitability_score)}}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.impact_score }} / {{GetSeverity(edge.impact_score)}}</td>
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
import ResultHeader from '@/components/ResultHeader.vue';
export default {
  name: 'Model Driven Results - Severity Display',

  components: {
    ResultHeader,
  },
  
  data() {
    return {
      error: undefined,
      edges: [],
      loading: true,
      currentSort: 'base_score',
      currentSortDir: 'desc',
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      this.loading = true;
      http.get('/model_driven/get_network_topology').then((r) => {        
        this.edges = r.data.edges;
        this.loading = false;
      });
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

    GetSeverity(x) {
      if (x >= 0.7) return 'High';
      if (x < 0.7 && x >= 0.4) return 'Medium';
      if (x < 0.4) return 'Low';
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
    highBase() {
      return this.edges.filter((e) => { return e.base_score >= 0.7});
    },

    mediumBase() {
      return this.edges.filter((e) => { return e.base_score < 0.7 && e.base_score >= 0.4});
    },

    lowBase() {
      return this.edges.filter((e) => { return e.base_score < 0.4});
    },

    highExploitability() {
      return this.edges.filter((e) => { return e.exploitability_score >= 0.7});
    },

    mediumExploitability() {
      return this.edges.filter((e) => { return e.exploitability_score < 0.7 && e.exploitability_score >= 0.4});
    },

    lowExploitability() {
      return this.edges.filter((e) => { return e.exploitability_score < 0.4});
    },

    highImpact() {
      return this.edges.filter((e) => { return e.impact_score >= 0.7});
    },

    mediumImpact() {
      return this.edges.filter((e) => { return e.impact_score < 0.7 && e.impact_score >= 0.4});
    },

    lowImpact() {
      return this.edges.filter((e) => { return e.impact_score < 0.4});
    }
  }
}
</script>

<style>
</style>