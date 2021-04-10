<template>
<div>
  <result-header 
    title="Network Visualization"
    nextPage="Data Driven Results - Derived Node Exploitation"
    prevPage="Data Driven Results - Overall Network Compromise"
    defaultPage="Data Driven Results"
  />
  <network-graph></network-graph>
</div>
</template>
<script>
import ResultHeader from '@/components/ResultHeader.vue';
import NetworkGraph from '@/components/DataDrivenNetworkGraph.vue';
export default {
  name: 'Data Driven Results - Network Visualization',

  components: {
    ResultHeader,
    NetworkGraph
  },
}
</script>
<style>
</style>