<template>
<div class="row">
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="col">
    <div id="networkContainer">
      <h2>Network Graph</h2>
      <svg id="network" :width="width" :height="height"></svg>
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
      error: undefined,
    }
  },

  components: {
  },

  props: {
    width: {
      type: Number,
      default: 800,
    },
    height: {
      type: Number,
      default: 800,
    },
  },

  mounted() {
    http.get('/model_driven/get_network_topology').then((r) => {
      console.log(r);
      generateModelDrivenNetworkDiagram(r.data);
    }).catch((e) => {
        this.error = e;
    });
  },
}
</script>

<style>
</style>
