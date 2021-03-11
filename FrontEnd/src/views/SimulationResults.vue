<template>
<div>
  <div v-if="!loading && rawData.length > 0">
    <h1>Node Probability Histogram</h1>
    <histogram :data="rawData" />
  </div>
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
      loading: Boolean,
    };
  },

  created() {
    this.getData();
  },

  methods: {
    getData() {
      this.loading = true;
      http.get('get-derived-scores').then((r) => {
        r.data.nodes.filter((n) => {
          this.rawData.push(n.base_score);
        });
        this.loading = false;
      });
    },
  },
}
</script>