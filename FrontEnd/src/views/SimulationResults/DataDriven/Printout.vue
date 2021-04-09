<template>
<div>
  <div class="noprint">
    <button class="btn btn-secondary" @click="PrintResults">
      Print
    </button>
  </div>
  <div v-if="error" class="alert alert-danger noprint">
    {{ error }}
  </div>
  <hr class="noprint">
  <div>
    <h1>Summary</h1>
    <div class="mx-5 text-justify row">
      <div class="col">
        <p>
          You have entered your network topology titled: <strong>{{ title }}</strong> on <strong>{{ inputDate }}</strong>. 
          It took <strong>{{ computationTime }}</strong> second(s) to compute the generated metrics.
        </p>
        <p>
          Your inputted network contains a total of <strong>{{ numNodes }}</strong> nodes and <strong>{{ numEdges }}</strong> edges.
        </p>
        <p>
          Out of the <strong>{{ numNodes }}</strong> nodes: 
          <br><strong>{{ numDerivedFactNodes}}</strong> or <strong>{{ derivedFactPercentage }}</strong> nodes were derived fact nodes. 
          <br><strong>{{ numDerivationNodes }}</strong> or <strong>{{ derivationPercentatge }}</strong> nodes were rule nodes.
          <br><strong>{{ numPrimitiveFactNodes }}</strong> or <strong>{{ primitiveFactPercentage }}</strong> nodes were primitive fact nodes.
        </p>
      </div>
      <div class="col" v-if="!loadingDerivedScores">
        <doughnut-chart 
          name="Network Topology Breakdown"
          :data="[numDerivedFactNodes, numDerivationNodes, numPrimitiveFactNodes]" 
          :labels="['Derived Fact Nodes', 'Rule Nodes', 'Primitive Fact Nodes']"
          style="width: 50%; height: 20%"
          class="container"
        />
      </div>
    </div>
    <hr>
    <h1>Overall Network Compromise / Exploitation Scenario</h1>
    <div class="mx-5 row">
      <!-- Overall network compromise/exploitation -->
      <div class="text-left">
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
          <br><strong>{{ numHighSeverity }}</strong> nodes are marked as <strong>high</strong> severity. (Computed Score &#8805; 0.7)
          <br><strong>{{ numMedSeverity }}</strong> nodes are marked as <strong>medium</strong> severity. (0.4 &#8804; Computed Score &lt; 0.7)
          <br><strong>{{ numLowSeverity }}</strong> nodes are marked as <strong>low</strong> severity. (Computed Score &lt; 0.4)
        </p>
        <p>
          Nodes marked as <strong>High Severity</strong> must be corrected with the highest priority.
          <br>Nodes marked as <strong>Medium Severity</strong> must be corrected with high priority.
          <br>Nodes marked as <strong>Low Severity</strong> are encouraged, but not required, to be corrected.
        </p>
      </div>
      <div class="row" v-if="!loadingDerivedScores">
        <Histogram
          :data="baseScores" 
          :numBins="10" 
          name="Node Probability Histogram (Computed Base Scores)" 
          barColor='#f87979'
          style="width: 60%"
          class="col"
        />
        <Histogram
          :data="impactScores" 
          :numBins="10" 
          name="Node Probability Histogram (Computed Impact Scores)" 
          barColor='#f87979'
          style="width: 60%"
          class="col"
        />
        <Histogram
          :data="exploitabilityScores" 
          :numBins="10" 
          name="Node Probability Histogram (Computed Exploitability Scores)" 
          barColor='#f87979'
          style="width: 60%"
          class="col"
        />
      </div>
    </div>
    <hr>
    <h1>Derived Node Exploitation Scenario</h1>
    <div class="mx-5 row">
      <div class="text-left">
        <p>
          The graph to the right shows a histogram of all the computed probabilities of every <strong>derived fact</strong> node in the network.
        </p>
        <p>
          Your network has a total of <strong>{{ derivedFact.num }} </strong> derived fact nodes. The breakdown of the derived fact nodes are as followed:
          <br>
          <strong>{{ execCode.percentage }}%</strong> of derived fact nodes or
          <strong>{{ execCode.num }}</strong> nodes in your network contain <strong>code execution capabilities</strong>: execCode().
          <br>
          <strong>{{ netAccess.percentage }}%</strong> of derived fact nodes or
          <strong>{{ netAccess.num }}</strong> nodes in your network <strong>allow for network access</strong>: netAccess().
          <br>
          <strong>{{ canAccess.percentage }}%</strong> of derived fact nodes or
          <strong>{{ canAccess.num }}</strong> nodes in your network have the <strong>ability to access the host</strong>: canAccessHost().
          <br>
          <strong>{{ principalCompromised.percentage }}%</strong> of derived fact nodes or
          <strong>{{ principalCompromised.num }}</strong> nodes in your network can have a <strong>compromised principal</strong>: principalCompromised().
          <br>
          <strong>{{ taskImpact.percentage }}%</strong> of derived fact nodes or
          <strong>{{ taskImpact.num }}</strong> nodes in your network if reached will <strong>impact node tasking</strong>: taskImpact().
          <br>
        </p>
      </div>
      <div class="row" v-if="!loadingDerivedScores">
        <!-- Still need to be able to define bin size -->
        <Histogram
          :data="derivedFact.scores" 
          :numBins="3"
          :binNames="['Low', 'Medium', 'High']" 
          name="Node Severity Histogram (All Derived Fact Nodes)" 
          :binLimits="[0.4, 0.7, 1]"
          barColor='#f87979'
          style="width: 60%"
          class="col"
        />
        <Histogram
          :data="execCode.scores" 
          :numBins="3"
          :binNames="['Low', 'Medium', 'High']" 
          name="Node Severity Histogram (Exec Code Nodes)" 
          :binLimits="[0.4, 0.7, 1]"
          barColor='#f87979'
          style="width: 60%"
          class="col"
        />
      </div>    
    </div>
    <hr>
    <h1>Attack Path Details</h1>
    <div class="mx-5 row">
      <div class="col-12">
        <div class="text-left">
          <p>
            Average number of conditions to reach a derived fact node: <strong>{{ avgNumConditions }}</strong>.
            <br>
            Average number of rules to reach a derived fact node: <strong>{{ avgNumRules }}</strong>.
          </p>
        </div>
      </div>  
      <div class="row" v-if="!loading">  
        <Histogram 
          :data="condVals"
          :numBins="5"
          name="Node Conditions Histogram (All Derived Fact Nodes)"
          barColor='#f87979'
          style="width: 50%"
          class="col"
        />
        <Histogram 
          :data="ruleVals"
          :numBins="5"
          name="Node Rules Histogram (All Derived Fact Nodes)"
          barColor='#f87979'
          style="width: 50%"
          class="col"
        />
      </div>
      <div class="row" v-if="!loading">
        <Histogram 
          :data="execCond"
          :numBins="5"
          name="Node Conditions Histogram (Exec Code Nodes)"
          barColor='#f87979'
          style="width: 50%"
          class="col"
        />
        <Histogram 
          :data="execRule"
          :numBins="5"
          name="Node Rules Histogram (Exec Code Nodes)"
          barColor='#f87979'
          style="width: 50%"
          class="col"
        />
      </div>
    </div>
  </div>
  <hr>
  <h1>Recommendations</h1>
  <div class=" mx-5 mb-4 row">
    <div class="col text-left">
      <div class="pb-4"></div>
      <p>
        To the right is a table containing a sorted list of all the derived fact nodes from your network
        ranked from highest derived score probability to lowest derived score probability.
      </p>
      <div>
        Our top <strong>{{ Math.min(numRecommend, rankedDerivedFactNodes.length) }}</strong> recommendations: 
        <ol v-if="!loading">
          <li v-for="(node, index) in rankedDerivedFactNodes.slice(0, numRecommend)" :key="index">
            Resolve node <strong>{{ node.id }}</strong>, <strong>{{node.description}}</strong>.
          </li>
        </ol>
      </div>
    </div>
    <div class="col">
      <network-data-table :data="rankedDerivedFactNodes" title="Derived Fact Nodes Data Table" :height="-1" />
    </div>
  </div>
  <div class="mx-5 mb-4 row">
    <div class="col text-left">
      <div class="pb-4"></div>
      <p>
        To the right is a table containing a sorted list of all the listed vulnerabilities from your network
        ranked from highest derived score probability to lowest derived score probability.
      </p>
      <div>
        Our top <strong>{{ Math.min(numRecommend, rankedVulExistsNodes.length) }}</strong> recommendations: 
        <ol v-if="!loading">
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
      <network-data-table :data="rankedVulExistsNodes" title="Vulnerability Nodes Data Table" :height="-1" />
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
import DoughnutChart from '@/components/DoughnutChart.vue';
import Histogram from '@/components/Histogram.vue';
import NetworkDataTable from '@/components/NetworkDataTable.vue';
export default {
  name: 'Data Driven Results - Printout',

  components: {
    DoughnutChart,
    Histogram,
    NetworkDataTable
  },

  data() {
    return {
      error: undefined,
      numNodes: 0,
      numEdges: 0,
      title: undefined,
      inputDate: undefined,
      computationTime: undefined,
      loadingDerivedScores: true,
      numDerivedFactNodes: 0,
      numDerivationNodes: 0,
      numPrimitiveFactNodes: 0,
      derivedFactPercentage: 0,
      derivationPercentatge: 0,
      primitiveFactPercentage: 0,
      loadingNetworkEntropy: true,
      networkEntropy: undefined,
      histogramScoreType: 'Base',
      histogramScoreData: [],
      baseScores: [],
      impactScores: [],
      exploitabilityScores: [],
      numHighSeverity: 0,
      numMedSeverity: 0,
      numLowSeverity: 0,
      histogramNodeData: [],
      histogramNodeType: 'All',
      execCode: {num: 0, percentage: 0, scores: []},
      netAccess: {num: 0, percentage: 0, scores: []},
      canAccess: {num: 0, percentage: 0, scores: []},
      principalCompromised: {num: 0, percentage: 0, scores: []},
      taskImpact: {num: 0, percentage: 0, scores: []},
      derivedFact: {num: 0, scores: []},
      data: [],
      rules: [],
      avgNumConditions: 0,
      avgNumRules: 0,
      currentSort: 'id',
      currentSortDir: 'asc',
      condVals: [],
      ruleVals: [],
      histogramType: 'All',
      histogramCondData: [],
      histogramRuleData: [],
      execCond: [],
      execRule: [],
      loading: true,
      numRecommend: 5,
      derivedFactNodes: [],
      vulExistsNodes: [],
    }
  },

  created() {
    this.GetData()
  },

  methods: {
    PrintResults() {
      window.print()
    },

    GetData() {
      this.loadingDerivedScores = true;
      this.loadingNetworkEntropy = true;
      this.loading = true;

      http.get('get_network_title').then((r) => {
        console.log(r);
        this.title = r.data.network_title;
      });

      http.get('get_input_date').then((r) => {
        console.log(r);
        this.inputDate = r.data.input_date;
      });

      http.get('/data_driven/network_entropy').then((r) => {
        // console.log(r);
        this.networkEntropy = {
          base: r.data.network_entropy[0].base,
          exploitability: r.data.network_entropy[1].exploitability,
          impact: r.data.network_entropy[2].impact
        } 
        this.loadingNetworkEntropy = false;
      }).catch((e) => {
        this.error = e;
      });

      http.get('data_driven/get_derived_scores').then((r) => {
        console.log(r);
        this.computationTime = r.data.computation_time < 1 ? 'less than 1' : Number(r.data.computation_time.toPrecision(3));

        this.numNodes = r.data.nodes.length;
        this.numEdges = r.data.edges.length;

        this.numDerivedFactNodes = r.data.nodes.filter((n) => {return n.node_type === 'Derived Fact'}).length;
        this.numPrimitiveFactNodes = r.data.nodes.filter((n) => {return n.node_type === 'Primitive Fact'}).length;
        this.numDerivationNodes = r.data.nodes.filter((n) => {return n.node_type === 'Derivation'}).length;

        this.derivedFactPercentage = Math.round(this.numDerivedFactNodes / this.numNodes  * 100);
        this.primitiveFactPercentage = Math.round(this.numPrimitiveFactNodes / this.numNodes  * 100);
        this.derivationPercentatge = Math.round(this.numDerivationNodes / this.numNodes * 100);

        r.data.nodes.forEach((n) => {
          this.baseScores.push(n.base_score);
          this.impactScores.push(n.impact_score);
          this.exploitabilityScores.push(n.exploitability_score);
        });

        this.histogramScoreData = this.baseScores;
        this.numHighSeverity = r.data.nodes.filter((n) => { return n.base_score >= 0.7 }).length;
        this.numMedSeverity = r.data.nodes.filter((n) => { return n.base_score >= 0.4 && n.base_score < 0.7 }).length;
        this.numLowSeverity = r.data.nodes.filter((n) => { return n.base_score < 0.4 }).length;

        this.derivedFactNodes = r.data.nodes.filter((n) => {return n.node_type === 'Derived Fact'});
        this.derivedFact.num = this.derivedFactNodes.length;

        this.derivedFactNodes.forEach((n) => {
          this.derivedFact.scores.push(n.base_score);
          if (n.description.includes('execCode')) this.execCode.scores.push(n.base_score);
          else if (n.description.includes('netAccess')) this.netAccess.scores.push(n.base_score);
          else if (n.description.includes('canAccessHost')) this.canAccess.scores.push(n.base_score);
          else if (n.description.includes('principalCompromised')) this.principalCompromised.scores.push(n.base_score);
          else if (n.description.includes('taskImpact')) this.taskImpact.scores.push(n.base_score);
        });

        this.execCode.num = this.execCode.scores.length;
        this.execCode.percentage = Math.round(this.execCode.num / this.derivedFact.num * 100);
        this.netAccess.num = this.netAccess.scores.length;
        this.netAccess.percentage = Math.round(this.netAccess.num / this.derivedFact.num * 100);
        this.canAccess.num = this.canAccess.scores.length;
        this.canAccess.percentage = Math.round(this.canAccess.num / this.derivedFact.num * 100);
        this.principalCompromised.num = this.principalCompromised.scores.length;
        this.principalCompromised.percentage = Math.round(this.principalCompromised.num / this.derivedFact.num * 100);
        this.taskImpact.num = this.taskImpact.scores.length;
        this.taskImpact.percentage = Math.round(this.taskImpact.num / this.derivedFact.num * 100);

        this.histogramNodeData = this.derivedFact.scores;

        this.vulExistsNodes = r.data.nodes.filter((n) => { return n.description.includes('vulExists') });

        this.loadingDerivedScores = false;
      }).catch((e) => {
        this.error = e;
      });

      http.get('/data_driven/conditions_and_rules_per_node').then((r) => {
        this.data = r.data.derived_data;
        
        this.data.forEach((n) => {
          this.condVals.push(n.num_conditions);
        });
        
        this.data.forEach((n) => {
          this.ruleVals.push(n.num_rules);
        });
        
        this.data
            .filter((n) => {return n.description.includes('execCode')})
            .forEach((n) => {
              this.execCond.push(n.num_conditions);
              this.execRule.push(n.num_rules);
            });

        this.avgNumConditions = this.condVals.reduce((a, b) => a + b) / this.condVals.length;
        this.avgNumRules = this.ruleVals.reduce((a, b) => a + b) / this.ruleVals.length;
        this.loading = false;
      }).catch((e) => {
        this.error = e;
      });
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
  
  computed: {
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
@media print {
   .noprint {
      visibility: hidden;
   }
}
</style>