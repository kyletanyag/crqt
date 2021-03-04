<template>
<div>
  <p>hello!</p>
  <network-graph :data="d"></network-graph>
</div> 
</template>


<script>
import NetworkGraph from '../components/NetworkGraph.vue'


export default {

  name: 'Sandbox',

  components: {
    NetworkGraph
  },

  data() {
    return {
      d: {
        nodes: [
          {
            id: 1
          },
          {
            id: 2
          },
          {
            id: 3
          }
        ],
        links: [
          {
            source: 1,
            target: 2
          },
          {
            source: 2,
            target: 3
          }
        ]
      }
    }
  },
}
</script>
