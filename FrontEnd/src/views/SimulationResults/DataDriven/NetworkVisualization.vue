<template>
<div class="mb-5">
  <result-header 
    title="Network Visualization"
    nextPage="Data Driven Results - Derived Node Exploitation"
    prevPage="Data Driven Results - Overall Network Compromise"
    defaultPage="Data Driven Results"
  />
  <div class="row mx-5 text-left">
    <div>
      <h2>Instructions</h2>
      <p>
        Below contains a graph representation of a network alongside a data table containing
        all the node data such as a node's ID, description, type, base, exploitability, and impact
        scores. 
        <br>
        On the network graph, you can hover over a node to get specific information or You
        can hover over a row in the network table and the corresponding node in the network graph will
        be highlighted.
      </p>
    </div>
  </div>
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