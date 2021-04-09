<template>
<div>
  <result-header 
    title="Network Visualization"
    nextPage="Model Driven Results - Graph Metrics"
    prevPage="'Model Driven Results - Summary"
    defaultPage="Model Driven Results"
  />
  <network-graph></network-graph>
</div>
</template>

<script>
import ResultHeader from '@/components/ResultHeader.vue';
import NetworkGraph from '@/components/ModelDrivenNetworkGraph.vue';
export default {
  name: 'Model Driven Results - Network Visualization',

  components: {
    ResultHeader,
    NetworkGraph
  }
}
</script>
<style>
</style>