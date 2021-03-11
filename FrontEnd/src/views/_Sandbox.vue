<template>
<div>
  <network-graph></network-graph>
</div> 
</template>

<script>
  /* eslint-disable */
import NetworkGraph from '../components/NetworkGraph.vue';
import http from '../http-common.js';
import { ref } from 'vue';

export default {

  name: 'Sandbox',

  components: {
    NetworkGraph,
  },

  data() {

    const nodes = ref([]);

    http.get('get-derived-scores').then((r) => {
      nodes.value = r.data.nodes;
    })

    return {
      nodes,
    };
  },

  mounted() {
  },
}
</script>
