<template>
<div>
  <div v-if="loading_progress == loading_goal && nodeProbHistData_derivedNodes.length > 0">
    <div class="histogram">
      <Histogram :data="nodeProbHistData_derivedNodes" numBins="10" name="Node Probability Histogram (Derived Nodes)" barColor='#f87979'/>
    </div>
    <div class="histogram">
      <Histogram :data="nodeProbHistData_derivedNodes" numBins="10" name="Node Probability Histogram (All Nodes [NOTE: CURRENTLY USES thE SAME DATA AS THE PREVIOUS ONE])" barColor='#00FF00'/>
    </div>
    <div class="doughnut">
      <DoughnutChart :data="doughnutChartData" name="Doughnut Chart"/>
    </div>
  </div> 
</div> 
</template>
<script>
import Histogram from '@/components/Histogram.vue'
import DoughnutChart from '@/components/DoughnutChart.vue'
import http from '@/http-common.js';

export default {

  name: 'Simulation Results',

  components: { 
    Histogram,
    DoughnutChart,
  },

  data() {
    return {
      nodeProbHistData_derivedNodes: [],
      nodeProbHistData_allNodes: [],

      percentage_execCode_nodes: [], 
      percentage_rule_nodes: [],
      percentage_derived_nodes: [],
      doughnutChartData: [], // group the above three values
      
      loading_progress: Number, // starts at zero, counts up every time you load a get()
      loading_goal: Number, // starts equal to the number of get() calls you intend to perform
    };
  },

  created() {
    this.getData();
  },

  methods: {
    getData() {
      this.loading_progress = 0;
      this.loading_goal = 4;
      http.get('get-derived-scores').then((r) => {
        r.data.nodes.filter((n) => {
          this.nodeProbHistData_derivedNodes.push(n.base_score);
        });
      this.loading_progress += 1;
      });

      // Get data for the doughnut chart
      this.doughnutLabels = new Array(3)
      http.get('percentage_execCode_nodes').then((r) => {
        this.percentage_execCode_nodes.push(r.data.percentage_execCode_nodes);
        this.loading_progress += 1;
      });
      http.get('percentage_rule_nodes').then((r) => {
        this.percentage_rule_nodes.push(r.data.percentage_rule_nodes);
        this.loading_progress += 1;
      });
      http.get('percentage_derived_nodes').then((r) => {
        this.percentage_derived_nodes.push(r.data.percentage_derived_nodes);
        this.loading_progress += 1;
      });
      this.doughnutChartData = [this.percentage_execCode_nodes,this.percentage_rule_nodes,this.percentage_derived_nodes]
    },
  },
}
</script>

<style>
   .histogram {
   width: 35%;
   }
   .doughnut {
   width: 35%;
   }
</style>