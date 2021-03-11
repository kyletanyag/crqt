<template>
<div>
  <h1>Node Probability Histogram</h1>
  <histogram :data="rawData" />
</div> 
</template>
<script>
import Histogram from '../components/Histogram.vue'
import http from '../http-common.js';

export default {

  name: 'Simulation Results',

  components: { 
    Histogram,
  },

  data() {
    return {
      rawData: [],
    };
  },

  mounted() {
    http.get('get-derived-scores').then((r) => {
      r.data.nodes.filter((n) => {
        this.rawData.push(n.base_score);
      })
    })
  },
}
</script>