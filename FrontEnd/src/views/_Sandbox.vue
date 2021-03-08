<template>
<div>
  <network-graph></network-graph>
</div> 
</template>

<script>
  /* eslint-disable */
import NetworkGraph from '../components/NetworkGraph.vue';



export default {

  name: 'Sandbox',

  components: {
    NetworkGraph,
  },

  data() {
    return {
      data: [['A', 'B', 'C'],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
      ],
    };
  },

  mounted() {
  },
}
</script>
