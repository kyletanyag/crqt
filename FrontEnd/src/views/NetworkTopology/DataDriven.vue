<template>
<div>
  <h2>Data-Driven Input</h2>  
  <p>
    From this page, you can enter your network topology following the <a target="_blank" href="http://people.cs.ksu.edu/~xou/mulval/">MulVAL</a> format.
    <br>
    You should have prepared: two CSV files - one containing the vertices and the other containing
    the arcs for your network topology.
  </p>
  <data-driven-input @uploadedData="emitEventUp"></data-driven-input>
</div>
</template>

<script>

import DataDrivenInput from '../../components/DataDrivenInput.vue'
export default {
  name: 'Data Driven',

  components: {
    DataDrivenInput,
  },

  methods: {
    emitEventUp() {
      this.$emit('uploadedData');
    }
  },

}
</script>

<style>
</style>