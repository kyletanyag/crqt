<template>
<div>
  <div v-if="!loading && rawData.length > 0">
    <div class="histogram">
      <Histogram :data="rawData" numBins="10" name="Node Probability Histogram (Derived Nodes)" barColor='#f87979'/>
    </div>
    <div class="histogram">
      <Histogram :data="rawData" numBins="10" name="Node Probability Histogram (All Nodes [NOTE: CURRENTLY USES thE SAME DATA AS THE PREVIOUS ONE])" barColor='#00FF00'/>
    </div>
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

<style>
   .histogram {
   width: 35%;
   }
</style>