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
        You have entered your network topology titled: <strong>{{ title }}</strong> on <strong>{{ input_date }}</strong>. 
        It took <strong>{{ computation_time }}</strong> second(s) to compute the generated metrics.
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
    <div class="col" v-if="!loadingDerivedScores">
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
      <p v-if="!loadingNetworkEntropy">
        Your network's overall risk (uncertainty) or network entropy:
        <br>Base Score: <strong>{{networkEntropy.base }}</strong>
        <br>Impact Score: <strong>{{networkEntropy.impact }}</strong>
        <br>Exploitability Score: <strong>{{networkEntropy.exploitability }}</strong>
      </p>
      <p>
        Your total network severity breakdown:
        <br><strong>{{ highSeverityNodes.length }}</strong> nodes are marked as <strong>high</strong> severity. (Base Score &#8805; 0.7)
        <br><strong>{{ mediumServerityNodes.length }}</strong> nodes are marked as <strong>medium</strong> severity. (0.4 &#8804; Base Score &lt; 0.7)
        <br><strong>{{ lowSeverityNodes.length }}</strong> nodes are marked as <strong>low</strong> severity. (Base Score &lt; 0.4)
      </p>
      <p>
        Nodes marked as <strong>High Severity</strong> must be corrected with the highest priority.
        <br>Nodes marked as <strong>Medium Severity</strong> must be corrected with high priority.
        <br>Nodes marked as <strong>Low Severity</strong> are encouraged, but not required, to be corrected.
      </p>
    </div>
    <div class="col" v-if="!loadingDerivedScores">
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
        Your network has a total of <strong>{{ derivedFactNodes.length }} </strong> derived fact nodes. The breakdown of the derived fact nodes are as followed:
        <br>
        <strong>{{ execCodePercentage }}%</strong> of derived fact nodes or
        <strong>{{ execCodeNodes.length }}</strong> nodes in your network contain <strong>code execution capabilities</strong>: execCode().
        <br>
        <strong>{{ netAccessCodePercentage }}%</strong> of derived fact nodes or
        <strong>{{ netAccessNodes.length }}</strong> nodes in your network <strong>allow for network access</strong>: netAccess().
        <br>
        <strong>{{ canAccessHostPercentage }}%</strong> of derived fact nodes or
        <strong>{{ canAccessHostNodes.length }}</strong> nodes in your network have the <strong>ability to access the host</strong>: canAccessHost().
        <br>
        <strong>{{ principalCompromisedPercentage }}%</strong> of derived fact nodes or
        <strong>{{ principalCompromisedNodes.length }}</strong> nodes in your network can have a <strong>compromised principal</strong>: principalCompromised().
        <br>
        <strong>{{ taskImpactPercentage }}%</strong> of derived fact nodes or
        <strong>{{ taskImpactNodes.length }}</strong> nodes in your network if reached will <strong>impact node tasking</strong>: taskImpact().
        <br>
      </p>
    </div>
    <div class="col" v-if="!loadingDerivedScores">
      <!-- Still need to be able to define bin size -->
      <Histogram
        :data="histogramNodeData" 
        numBins="3"
        :binNames="['Low', 'Medium', 'High']" 
        :name="histogramNodeName" 
        :binLimits="[0.4, 0.7, 1]"
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
        How many recommendations would you like to see? 
        <input type="number" v-model.number="numRecommend" max="10" min="1" maxlength="2"
          onkeyup="if(this.value > 10) this.value = 10; else if(this.value < 0) this.value = 0;"
        > 
        <br>
        <p>
          To the right is a table containing a sorted list of all the derived fact nodes from your network
          ranked from highest derived score probability to lowest derived score probability.
        </p>
        <div>
          Our top <strong>{{ Math.min(numRecommend, rankedDerivedFactNodes.length) }}</strong> recommendations: 
          <ol v-if="!loadingDerivedScores">
            <li v-for="(node, index) in rankedDerivedFactNodes.slice(0, numRecommend)" :key="index">
              Resolve node <strong>{{ node.id }}</strong>, <strong>{{node.description}}</strong>.
            </li>
          </ol>
        </div>
      </div>
      <div class="col">
        <network-data-table :data="rankedDerivedFactNodes" title="Derived Fact Nodes Data Table" />
      </div>
    </div>
    <div class="mx-5 mb-2 row">
      <div class="col text-left">
        <p>
          To the right is a table containing a sorted list of all the listed vulnerabilities from your network
          ranked from highest derived score probability to lowest derived score probability.
        </p>
        <div>
          Our top <strong>{{ Math.min(numRecommend, rankedVulExistsNodes.length) }}</strong> recommendations: 
          <ol v-if="!loadingDerivedScores">
            <li v-for="(node, index) in rankedVulExistsNodes.slice(0,numRecommend)" :key="index">
              Close vulnerabilty <strong>{{ getCVEID(node.description)}}</strong>
              at the host: <strong>{{getHost(node.description)}}</strong>
              found at node <strong>{{node.id}}</strong>. 
              <br>The severity level of this node is marked as <strong>{{getSeverityLevel(node.base_score)}}</strong>.
            </li>
          </ol>
        </div>
      </div>
      <div class="col">
        <network-data-table :data="rankedVulExistsNodes" title="Vulnerability Nodes Data Table" />
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
import NetworkDataTable from '@/components/NetworkDataTable.vue';

export default 
{
  name: 'Data Driven Results',

  components: { 
    DoughnutChart,
    Histogram, 
    NetworkGraph,
    NetworkDataTable,
  },

  data() {
    return {
      nodes: [],
      edges: [],
      title: undefined,
      input_date: undefined,
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
      netAccessNodes: [],
      netAccessCodePercentage: 0,
      canAccessHostNodes: [],
      canAccessHostPercentage: 0,
      principalCompromisedNodes: [],
      principalCompromisedPercentage: 0,
      taskImpactNodes: [],
      taskImpactPercentage: 0,
      vulExistsNodes: [],
      networkEntropy: undefined,
      loadingDerivedScores: true,
      loadingNetworkEntropy: true,
      numRecommend: 3,
      computation_time: 0,
    }
  },

  created() {
    this.getData();
  },

  methods: {
    getData() {
      this.loadingDerivedScores = true;
      this.loadingNetworkEntropy = true;

      http.get('get_network_title').then((r) => {
        console.log(r);
        this.title = r.data.network_title;
      });

      http.get('get_input_date').then((r) => {
        console.log(r);
        this.input_date = r.data.input_date;
      });

      http.get('data_driven/get_derived_scores').then((r) => {
        console.log(r);
        this.computation_time = r.data.computation_time < 1 ? 'less than 1' : Number(r.data.computation_time.toPrecision(3));

        this.nodes = r.data.nodes;
        this.edges = r.data.edges;

        r.data.nodes.forEach((n) => {

          this.baseScores.push(n.base_score);
          this.impactScores.push(n.impact_score);
          this.exploitabilityScores.push(n.exploitability_score);

          if (n.node_type === 'Derived Fact') {
            this.derivedFactNodes.push(n);
            this.allDerivedFactNodesBaseScores.push(n.base_score);
            if (n.description.includes('execCode')) {
              this.execCodeNodes.push(n);
              this.execDerivedFactNodesBaseScores.push(n.base_score);
            }
            if (n.description.includes('netAccess')) this.netAccessNodes.push(n);
            if (n.description.includes('canAccessHost')) this.canAccessHostNodes.push(n);
            if (n.description.includes('principalCompromised')) this.principalCompromisedNodes.push(n);
            if (n.description.includes('taskImpact')) this.taskImpactNodes.push(n);
          } else if (n.node_type === 'Primitive Fact') {
            this.primitiveFactNodes.push(n);
            if (n.description.includes('vulExists')) this.vulExistsNodes.push(n);
          } else {
            this.derivationNodes.push(n);
          }
        });

        this.derivedFactPercentage = Math.round(this.derivedFactNodes.length / this.nodes.length * 100);
        this.primitiveFactPercentage = Math.round(this.primitiveFactNodes.length / this.nodes.length * 100);
        this.derivationPercentatge = Math.round(this.derivationNodes.length / this.nodes.length * 100);
        this.execCodePercentage = Math.round(this.execCodeNodes.length / this.derivedFactNodes.length * 100);
        this.netAccessCodePercentage = Math.round(this.netAccessNodes.length / this.derivedFactNodes.length * 100);
        this.canAccessHostPercentage = Math.round(this.canAccessHostNodes.length / this.derivedFactNodes.length * 100);
        this.principalCompromisedPercentage = Math.round(this.principalCompromisedNodes.length / this.derivedFactNodes.length * 100);
        this.taskImpactPercentage = Math.round(this.taskImpactNodes.length / this.derivedFactNodes.length * 100);

        this.histogramScoreData = this.baseScores;
        this.histogramNodeData = this.allDerivedFactNodesBaseScores;
        this.loadingDerivedScores = false;
      });

      http.get('/data_driven/network_entropy').then((r) => {
        console.log(r);
        this.networkEntropy = {
          base: r.data.network_entropy[0].base,
          exploitability: r.data.network_entropy[1].exploitability,
          impact: r.data.network_entropy[2].impact
        } 
        this.loadingNetworkEntropy = false;
      })
    },

    getCVEID(str) {
      var values = str.split("'");
      return values[1];
    },

    getHost(str) {
      return str.substring(str.lastIndexOf("(") + 1, str.indexOf(","));
    },

    getSeverityLevel(score) {
      if (score >= 0.7) return 'High';
      if (score >= 0.4) return 'Medium';
      return 'Low';
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
      }, 1500)

      if (type === 'All')
        this.histogramNodeData = this.allDerivedFactNodesBaseScores;
      else
        this.histogramNodeData = this.execDerivedFactNodesBaseScores;
    },

    numRecommend() {
      if (this.numRecommend > 10) this.numRecommend = 10;
      if (this.numRecommend < 0) this.numRecommend = "";
      if (!this.numRecommend === "") this.numRecommend = 1;
    }
  },

  computed: {
    histogramScoreName() {
      return `Node Probability Histogram (${this.histogramScoreType} Scores)`
    },

    histogramNodeName() {
      if (this.histogramNodeType === 'All')
        return 'Node Severity Histogram (All Derived Fact Nodes)';
      else
        return 'Node Severity Histogram (Exec Code Nodes)';
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
    },

    rankedDerivedFactNodes() {
      var temp = this.derivedFactNodes.slice(0).sort((a,b) => {
        if(a['base_score'] < b['base_score']) return 1;
        if(a['base_score'] > b['base_score']) return -1;
      });

      for (let i = 0; i < temp.length; i++) {
        temp[i]['ranking'] = i + 1
      }
      return temp;
    },

    rankedVulExistsNodes() {
      var temp = this.vulExistsNodes.slice(0).sort((a,b) => {
        if(a['base_score'] < b['base_score']) return 1;
        if(a['base_score'] > b['base_score']) return -1;
      });

      for (let i = 0; i < temp.length; i++) {
        temp[i]['ranking'] = i + 1
      }
      return temp;
    }
  }
}
</script>

<style>
</style>