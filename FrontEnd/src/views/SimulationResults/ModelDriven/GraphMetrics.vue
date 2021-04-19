<template>
<div class="mb-5">
  <result-header 
    title="Graph Property Based Metrics"
    nextPage="Model Driven Results - Attack Path Metrics"
    prevPage="Model Driven Results - Network Visualization"
    defaultPage="Model Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="mx-5 row">
    <div class="col text-left">
      <h2>Centrality Meaures</h2>
      <div class="mx-1 row">
        <div>
          <p>
            Below are histograms containing the node values for different centrality metrics such as:
          </p>
          <ul>
            <li class="pb-1">
              <strong>Out-Degree Centrality:</strong> The number of outgoing edges for each node.
            </li>
            <li class="pb-1">
              <strong>In-Degree Centrality:</strong> The number of incoming edges for each node. 
            </li>
            <li class="pb-1">
              <strong>Degree Centrality:</strong> The total number of incoming and outgoing edges for each node.
            </li>
            <li class="pb-1">
              <strong>Closeness Centrality:</strong> The average length of the shortest path between the node and all other nodes in the graph.
            </li>
            <li class="pb-1">
              <strong>Betweenness Centrality:</strong> Quantifies the number of times a node acts as a bridge along the shortest path between two other nodes.
            </li>
            <li class="pb-1">
              <strong>PageRank Centrality:</strong> Ranks nodes based on the number and quality of links to a node to give rough estimate of node importance.
            </li>
            <li class="pb-1">
              <strong>Katz Centrality (KC):</strong>  Measures the number of all nodes that can be connected through a path, while contributions of distant nodes are penalized.
            </li>
          </ul>
          <p>
            The purpose of these metrics are to provide a visualization for possible trends that may occurs within network graph.
          </p>
        </div>
      </div>
      <div class="row py-2" v-if="degree.length && closeness.length && betweeness.length">
        <Histogram
          :data="degree"
          :numBins="10"
          :range="[Math.min(...degree), Math.max(...degree)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Degree Centrality"
          barColor='#78BCFF'
          class="col-4"
        />
        <Histogram
          :data="closeness"
          :numBins="10"
          :range="[Math.min(...degree), Math.max(...degree)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Closeness Centrality"
          barColor='#81DFA9'
          class="col-4"
        />
        <Histogram
          :data="betweeness"
          :numBins="10"
          :range="[Math.min(...betweeness), Math.max(...betweeness)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Betweeness Centrality"
          barColor='#f87979'
          class="col-4"
        />
      </div>
      <div class="row py-4" v-if="pagerank.length && katz.length && outdegree.length">
        <Histogram
          :data="pagerank"
          :numBins="10"
          :range="[Math.min(...pagerank), Math.max(...pagerank)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Pagerank Centrality"
          barColor='#78BCFF'
          class="col-4"
        />
        <Histogram
          :data="katz"
          :numBins="10"
          :range="[Math.min(...katz), Math.max(...katz)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Katz Centrality"
          barColor='#81DFA9'
          class="col-4"
        />
        <Histogram
          :data="outdegree"
          :numBins="10"
          :range="[Math.min(...outdegree), Math.max(...outdegree)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Outdegree Centrality"
          barColor='#f87979'
          class="col-4"
        />
      </div>
      <hr>
      <h2>Degree Distributions</h2>
      <div class="mx-1 row">
        <div>
          <p>
            Below are histograms containing the node values of the degree centrality metrics but converted into probabilities:
          </p>
          <ul>
            <li class="pb-1">
              <strong>Out-Degree Centrality:</strong> The number of outgoing edges for each node.
            </li>
            <li class="pb-1">
              <strong>In-Degree Centrality:</strong> The number of incoming edges for each node. 
            </li>
            <li class="pb-1">
              <strong>Degree Centrality:</strong> The total number of incoming and outgoing edges for each node.
            </li>
          </ul>
          <p>
            The purpose of these metrics are to provide a visualization for possible trends that may occurs within network graph 
            when it comes to degree centrality probability distributions.
          </p>
        </div>
      </div>
      <div class="row py-2 justify-content-center" v-if="indegree.length && outdegree.length && degree.length">
        <Histogram
          :data="indegreeProb"
          :numBins="10"
          yAxis="Frequency"
          xAxis="Probability"
          name="In Degree"
          barColor='#78BCFF'
          class="col-4"
        />
        <Histogram
          :data="outdegreeProb"
          :numBins="10"
          yAxis="Frequency"
          xAxis="Probability"
          name="Out Degree"
          barColor='#81DFA9'
          class="col-4"
        />
      <!-- </div> -->
      <!-- <div class="row py-2 justify-content-center" v-if="indegree.length && outdegree.length && degree.length"> -->
        <Histogram
          :data="degreeProb"
          :numBins="10"
          yAxis="Frequency"
          xAxis="Probability"
          name="Degree"
          barColor='#C29AD3'
          class="col-4"
        />
        <!-- <Histogram
          :data="degreeProb"
          :numBins="10"
          name="Combined Degree Distributions"
          barColor='#f87979'
          class="col-4"
        /> -->
      </div>
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
import ResultHeader from '@/components/ResultHeader.vue';
import Histogram from '@/components/Histogram.vue';
export default {
  name: 'Model Driven Results - Graph Metrics',

  components: {
    ResultHeader,
    Histogram
  },

  data() {
    return {
      error: undefined,
      betweeness: [],
      closeness: [],
      degree: [],
      indegree: [],
      katz: [],
      outdegree: [],
      pagerank: [],
      indegreeSum: 1,
      outdegreeSum: 1,
      degreeSum: 1,

    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      http.get('/model_driven/centrality').then((r) => {
        console.log(r);

        this.betweeness = r.data.betweeness;
        this.closeness = r.data.closeness;
        this.degree = r.data.degree;
        this.indegree = r.data.indegree;
        this.katz = r.data.katz;
        this.outdegree = r.data.outdegree;
        this.pagerank = r.data.pagerank;

      }).catch((e) => {
        this.error = e;
      })
    }
  },

  computed: {
    degreeProb() {
      var ratio = Math.max.apply(Math, this.degree);
      return this.degree.map(x => x /= ratio);
    },

    indegreeProb() {
      var ratio = Math.max.apply(Math, this.indegree);
      return this.indegree.map(x => x /= ratio);
    },

    outdegreeProb() {
      var ratio = Math.max.apply(Math, this.outdegree);
      return this.outdegree.map(x => x /= ratio);
    },
  }
}
</script>
<style>
</style>