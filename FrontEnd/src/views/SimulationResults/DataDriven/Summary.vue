<template>
<div>
  <result-header 
    title="Summary"
    nextRouteName="Data Driven Results - Overall Network Compromise"
    defaultRouteName="Data Driven Results"
  />
  <div class="mx-5 text-justify row">
    <!-- Summary, contain basic network information -->
    <!-- Node statistics -->
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
</div>
</template>

<script>
import http from '@/http-common.js';
import DoughnutChart from '@/components/DoughnutChart.vue';
import ResultHeader from '@/components/ResultHeader.vue';

export default {
  name: 'Data Driven Results - Summary',

  data() {
    return {
      numNodes: 0,
      numEdges: 0,
      title: undefined,
      inputDate: undefined,
      computationTime: undefined,
      loadingDerivedScores: true,
      error: undefined,
      numDerivedFactNodes: 0,
      numDerivationNodes: 0,
      numPrimitiveFactNodes: 0,
      derivedFactPercentage: 0,
      derivationPercentatge: 0,
      primitiveFactPercentage: 0,
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      this.loadingDerivedScores = true;

      http.get('get_network_title').then((r) => {
        console.log(r);
        this.title = r.data.network_title;
      });

      http.get('get_input_date').then((r) => {
        console.log(r);
        this.inputDate = r.data.input_date;
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

        this.loadingDerivedScores = false;
      }).catch((e) => {
        this.error = e;
      });
    }
  },

  components: {
    DoughnutChart,
    ResultHeader,
  }
}
</script>
<style>
</style>