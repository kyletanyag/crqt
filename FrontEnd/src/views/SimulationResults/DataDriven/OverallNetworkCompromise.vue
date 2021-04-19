<template>
<div>
  <result-header 
    title="Overall Network Compromise / Exploitation Scenario"
    nextPage="Data Driven Results - Network Visualization"
    prevPage="Data Driven Results - Summary"
    defaultPage="Data Driven Results"
    ref="rh"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="mx-5 row">
    <!-- Overall network compromise/exploitation -->
    <div class="col text-left">
      <h2>Network Node Scores</h2>
      <p>
        The graph to the right shows a histogram of all the computed probabilities of every node in the network by their computed scores.
        You can change which type of score that you are interested in as well as the bin size for the histograms. 
      </p>
      <p>
        The computed scores range from a scale from [0, 1] and represent the <strong>probability of access</strong>
        (or derived probability) of a node. The higher the score, the higher probability an attacker can access a node.
      </p>
      <h2>Network Entropy</h2>
      <p>
        Network entropy represents the <strong>uncertainty</strong> in a network and can be used to gauge network risk.
      </p>
      <p v-if="!loadingNetworkEntropy">
        Your network's overall risk (uncertainty) or network entropy by score:
        <br>Base Score: <strong>{{networkEntropy.base }}</strong>
        <br>Impact Score: <strong>{{networkEntropy.impact }}</strong>
        <br>Exploitability Score: <strong>{{networkEntropy.exploitability }}</strong>
      </p>
      <h2>Network Severity Statistics</h2>
      <p>
        Network severity provides a means to denote which nodes in a network are deemed as a highly 
        vulnerable and exploitable nodes. The higher the severity, the more important it is for that nodes
        be corrected.
      </p>
      <p>
        Nodes marked as <strong>High Severity</strong> must be corrected with the highest priority.
        <br>Nodes marked as <strong>Medium Severity</strong> must be corrected with high priority.
        <br>Nodes marked as <strong>Low Severity</strong> are encouraged, but not required, to be corrected.
      </p>
      <p>
        Your total network severity breakdown:
        <br><strong>{{ numHighSeverity }}</strong> nodes are marked as <strong>high</strong> severity. (Computed Base Score &#8805; 0.7)
        <br><strong>{{ numMedSeverity }}</strong> nodes are marked as <strong>medium</strong> severity. (0.4 &#8804; Computed Base Score &lt; 0.7)
        <br><strong>{{ numLowSeverity }}</strong> nodes are marked as <strong>low</strong> severity. (Computed Base Score &lt; 0.4)
      </p>

    </div>
    <div class="col" v-if="!loadingDerivedScores">
      <Histogram 
        :data="histogramScoreData" 
        :numBins="numBins" 
        :name="histogramScoreName" 
        yAxis="Frequency"
        xAxis="Probability Score"
        barColor='#f87979'
        style="width: 60%"
        class="container"
      />
      <div class="d-flex justify-content-center">
        <h5 class="pt-3">Select Computed Score:</h5>
        <div class="btn-group btn-group-toggle pt-2 px-2">
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
      <div class="d-flex justify-content-center">
        <h5 class="pt-3">Select Bin Size:</h5>
        <div class="btn-group btn-group-toggle pt-2 px-2"> 
          <label class="btn btn-secondary" :class="{active: numBins === 5}">
            <input  type="radio" v-model="numBins" :value="5" autocomplete="off"> 5
          </label>
          <label class="btn btn-secondary" :class="{active: numBins === 10}">
            <input  type="radio" v-model="numBins" :value="10"  autocomplete="off"> 10
          </label>
          <label class="btn btn-secondary" :class="{active: numBins === 20}">
            <input type="radio" v-model="numBins" :value="20"  autocomplete="off"> 20
          </label>
        </div>
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
  name: 'Data Driven Results - Overall Network Compromise',

  components: {
    ResultHeader,
    Histogram
  },
  
  data() {
    return {
      loadingNetworkEntropy: true,
      loadingDerivedScores: true,
      networkEntropy: undefined,
      histogramScoreType: 'Base',
      histogramScoreData: [],
      baseScores: [],
      impactScores: [],
      exploitabilityScores: [],
      numHighSeverity: 0,
      numMedSeverity: 0,
      numLowSeverity: 0,
      numBins: 10,
      error: undefined,
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      this.loadingNetworkEntropy = true;
      this.loadingDerivedScores = true;

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
        // console.log(r);
        r.data.nodes.forEach((n) => {
          this.baseScores.push(n.base_score);
          this.impactScores.push(n.impact_score);
          this.exploitabilityScores.push(n.exploitability_score);
        });

        this.histogramScoreData = this.baseScores;
        this.numHighSeverity = r.data.nodes.filter((n) => { return n.base_score >= 0.7 }).length;
        this.numMedSeverity = r.data.nodes.filter((n) => { return n.base_score >= 0.4 && n.base_score < 0.7 }).length;
        this.numLowSeverity = r.data.nodes.filter((n) => { return n.base_score < 0.4 }).length;
        this.loadingDerivedScores = false;
       }).catch((e) => {
         this.error = e; 
       });
    },
  },

  computed: {
    histogramScoreName() {
      return `Node Probability Histogram (Computed ${this.histogramScoreType} Scores)`
    },   
  },

  watch: {
    histogramScoreType(type) {
      if (type === 'Base')
        this.histogramScoreData = this.baseScores;
      else if (type === 'Impact')
        this.histogramScoreData = this.impactScores;
      else 
        this.histogramScoreData = this.exploitabilityScores;
    },
  }
}
</script>

<style>
</style>