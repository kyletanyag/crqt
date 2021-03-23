<template>
<div>
  <h1>Network Topology Results (Data-Driven)</h1>
  <hr>
  <h3 class="pb-1">Summary</h3>
  <div class="mx-5 text-justify row">
    <!-- Summary, contain basic network information -->
    <!-- Node statistics -->
    <div class="col">
      <p>
        You have entered your network topology titled: <strong>{{ title }}</strong> on {{ }}. 
        It took {{ }} to compute the generated metrics.
      </p>
      <p>
        Your inputted network contains a total of <strong>{{ nodes.length }}</strong> nodes and <strong>{{ edges.length }}</strong> edges.
      </p>
      <p>
        Out of the <strong>{{ nodes.length }}</strong> nodes: 
        <br><strong>{{ derivedFactNodes.length }} </strong> nodes were derived fact nodes. 
        <br><strong>{{ derivationNodes.length }}</strong> nodes were rule nodes.
        <br><strong>{{ primitiveFactNodes.length }}</strong> nodes were primitive fact nodes.
      </p>
    </div>
    <div class="col" v-if="!loading">
      <doughnut-chart 
        name="Network Topology Breakdown"
        :data="[derivedFactPercentage, derivationPercentatge, primitiveFactPercentage]" 
        :labels="['% of Derived Fact Nodes', '% of Rule Nodes', '% of Primitive Fact Nodes']"
        style="width: 50%; height: 20%"
        class="container"
      />
    </div>
  </div>
  <hr>
  <h3 class="pb-1">Overall Network Compromise / Exploitation</h3>
  <div class="mx-5 row">
    <!-- Overall network compromise/exploitation -->
    <div class="col text-left">
      <p>
        The graph to the right shows a histogram of all the computed probabilities of every node in the network by score.
      </p>
      <p>
        Your network's overall risk (uncertainty) or network entropy:
        <br>Base Score: <strong>{{networkEntropy.base }}</strong>
        <br>Impact Score: <strong>{{networkEntropy.impact }}</strong>
        <br>Exploitability Score: <strong>{{networkEntropy.exploitability }}</strong>
      </p>
      <p>
        Your total network severity breakdown:
        <br><strong>{{ highSeverityNodes.length }}</strong> nodes are marked as <strong>high</strong> severity. (Base Score > 0.7)
        <br><strong>{{ mediumServerityNodes.length }}</strong> nodes are marked as <strong>medium</strong> severity. (0.4 &lt; Base Score &lt; 0.7)
        <br><strong>{{ lowSeverityNodes.length }}</strong> nodes are marked as <strong>low</strong> severity. (Base Score &lt; 0.4)
      </p>
      <p>
        Nodes marked as <strong>High Severity</strong> must be corrected with the highest priority.
        <br>Nodes marked as <strong>Medium Severity</strong> must be corrected with high priority.
        <br>Nodes marked as <strong>Low Severity</strong> are encouraged, but not required, to be corrected.
      </p>
    </div>
    <div class="col" v-if="!loading">
      <Histogram
        :data="histogramScoreData" 
        numBins="10" 
        :name="histogramScoreName" 
        barColor='#f87979'
        style="width: 60%"
        class="container"
      />
      <div class="btn-group btn-group-toggle pt-2" id="histogram score">
        <label class="btn btn-secondary" :class="{active: histogramScoreType === 'Base'}">
          <input type="radio" v-model="histogramScoreType" value="Base" autocomplete="off"> Base
        </label>
        <label class="btn btn-secondary" :class="{active: histogramScoreType === 'Impact'}">
          <input type="radio" v-model="histogramScoreType" value="Impact"  autocomplete="off"> Impact
        </label>
        <label class="btn btn-secondary" :class="{active: histogramScoreType === 'Exploitability' }">
          <input type="radio" v-model="histogramScoreType" value="Exploitability" autocomplete="off"> Exploitability
        </label>
      </div>
    </div>
  </div>
  <hr>
  <h3 class="pb-1">Derived Node Exploitation Scenario</h3>
  <div class="mx-5 row">
    <!-- Derived Node exploitation Scenario -->
    <div class="col text-left">
      <p>
        The graph to the right shows a histogram of all the computed probabilities of every <strong>derived fact</strong> node in the network.
      </p>
      <p>
        <strong>{{ execCodePercentage }}%</strong> of derived fact nodes or
        <strong>{{ execCodeNodes.length }}</strong> nodes in your network contain code execution capabilities.
      </p>
    </div>
    <div class="col" v-if="!loading">
      <Histogram
        :data="histogramNodeData" 
        numBins="5" 
        :name="histogramNodeName" 
        barColor='#f87979'
        style="width: 60%"
        class="container"
      />
      <div class="btn-group btn-group-toggle pt-2" id="histogram node">
        <label class="btn btn-secondary" :class="{active: histogramNodeType === 'All'}">
          <input type="radio" v-model="histogramNodeType" value="All" autocomplete="off"> All
        </label>
        <label class="btn btn-secondary" :class="{active: histogramNodeType === 'Exec Code'}">
          <input type="radio" v-model="histogramNodeType" value="Exec Code"  autocomplete="off"> Exec Code
        </label>
      </div>
    </div>    
  </div>
  <hr>
  <h3 class="pb-1">Specific Node Information</h3>
  <div>
    <!-- Conditions to reach a node -->
    <network-graph></network-graph>
  </div>
  <hr>
  <h3 class="pb-1">Recommendations</h3>
  <div class="mb-4">
    <!-- Highest ranking issues -->
    <div class=" mx-5 mb-2 row">
      <div class="col text-left">
        <p>
          To the right is a table containing a sorted list of all the derived fact nodes from your network
          ranked from highest derived score probability to lowest derived score probability.
        </p>
        <p>
          Our top <strong>3</strong> recommendations: 
          <br> Resolve {{ }}
          <br> Resolve {{ }}
          <br> Resolve {{ }}
        </p>
      </div>
      <div class="col">
        table goes here
      </div>
    </div>
    <div class="mx-5 mb-2 row">
      <div class="col text-left">
        <p>
          To the right is a table containing a sorted list of all the listed vulnerabilities from your network
          ranked from highest derived score probability to lowest derived score probability.
        </p>
        <p>
          Our top <strong>3</strong> recommendations: 
          <br> Close vulnerabilty {{ }}
          <br> Close vulnerabilty {{ }}
          <br> Close vulnerabilty {{ }}
        </p>
      </div>
      <div class="col">
        table goes here
      </div>
    </div>
  </div>
</div>
</template>

<script>
// import { ref } from 'vue';
import http from '@/http-common.js';
import DoughnutChart from '@/components/DoughnutChart.vue';
import Histogram from '@/components/Histogram.vue';
import NetworkGraph from '@/components/NetworkGraph.vue';

export default 
{
  name: 'Data Driven Results',

  components: { 
    DoughnutChart,
    Histogram, 
    NetworkGraph 
  },

  data() {
    return {
      nodes: [],
      edges: [],
      title: undefined,
      derivedFactNodes: [],
      primitiveFactNodes: [],
      derivationNodes: [],
      derivedFactPercentage: 0,
      primitiveFactPercentage: 0,
      derivationPercentatge: 0,
      baseScores: [],
      impactScores: [],
      exploitabilityScores: [],
      histogramScoreType: 'Base',
      histogramScoreData: [],
      histogramNodeType: 'All',
      histogramNodeData: [],
      allDerivedFactNodesBaseScores: [],
      execDerivedFactNodesBaseScores: [],
      execCodeNodes: [],
      execCodePercentage: 0,
      networkEntropy: undefined,
      loading: true,
    }
  },

  created() {
    this.getData();
  },

  methods: {
    getData() {
      this.loading = true;

      http.get('get-derived-scores').then((r) => {
        console.log(r);
        this.nodes = r.data.nodes;
        this.edges = r.data.edges;

        r.data.nodes.forEach((n) => {

          this.baseScores.push(n.base_score);
          this.impactScores.push(n.impact_score);
          this.exploitabilityScores.push(n.exploitability_score);

          if (n.node_type === 'Derived Fact') {
            this.derivedFactNodes.push(n);
            this.allDerivedFactNodesBaseScores.push(n.base_score);
          } else if (n.node_type === 'Primitive Fact') {
            this.primitiveFactNodes.push(n);
          } else {
            this.derivationNodes.push(n);
          }
        });

        this.derivedFactPercentage = Math.round(this.derivedFactNodes.length / this.nodes.length * 100);
        this.primitiveFactPercentage = Math.round(this.primitiveFactNodes.length / this.nodes.length * 100);
        this.derivationPercentatge = Math.round(this.derivationNodes.length / this.nodes.length * 100);
        this.execCodePercentage = Math.round(this.execCodeNodes.length / this.derivedFactNodes.length * 100);
        this.histogramScoreData = this.baseScores;
        this.histogramNodeData = this.allDerivedFactNodesBaseScores;
        this.loading = false;
      });

      http.get('network_entropy').then((r) => {
        console.log(r);
        this.networkEntropy = {
          base: r.data.network_entropy[0].base,
          exploitability: r.data.network_entropy[1].exploitability,
          impact: r.data.network_entropy[2].impact
        } 
      })
    },
  },

  watch: {
    histogramScoreType(type) {
      // Histogram must be fully rendered before switching datasets.
      // Disables radio buttons for 1200 ms to allow for full render.
      const btns = document.getElementById('histogram score').getElementsByTagName('input');
      btns.forEach((b) => {
        b.disabled = true;
      });
      setTimeout(() => {
        btns.forEach((b) => {
          b.disabled = false;
        });
      }, 1500)

      if (type === 'Base')
        this.histogramScoreData = this.baseScores;
      else if (type === 'Impact')
        this.histogramScoreData = this.impactScores;
      else 
        this.histogramScoreData = this.exploitabilityScores;
    },

    histogramNodeType(type) {
      const btns = document.getElementById('histogram node').getElementsByTagName('input');
      btns.forEach((b) => {
        b.disabled = true;
      });
      setTimeout(() => {
        btns.forEach((b) => {
          b.disabled = false;
        });
      }, 1200)

      if (type === 'All')
        this.histogramNodeData = this.allDerivedFactNodesBaseScores;
      else
        this.histogramNodeData = this.execDerivedFactNodesBaseScores;
    }
  },

  computed: {
    histogramScoreName() {
      return `Node Probability Histogram (${this.histogramScoreType} Scores)`
    },

    histogramNodeName() {
      if (this.histogramNodeType === 'All')
        return 'Node Probability Histogram (All Derived Fact Nodes)';
      else
        return 'Node Probability Histogram (Exec Code Nodes)';
    },

    highSeverityNodes() {
      return this.nodes.filter((n) => {
        return n.base_score >= 0.7;
      });
    },

    mediumServerityNodes() {
      return this.nodes.filter((n) => {
        return n.base_score >= 0.4 && n.base_score < 0.7
      });
    },

    lowSeverityNodes() {
      return this.nodes.filter((n) => {
        return n.base_score < 0.4;
      })
    }
  }
}
</script>

<style>
</style>