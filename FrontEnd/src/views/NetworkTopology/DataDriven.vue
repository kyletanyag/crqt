<template>
<div>
  <h1>Data-Driven Input</h1>
  <div class="mx-5">
    <div>
      <p>
        From this page, you can enter your network topology following the <a target="_blank" href="http://people.cs.ksu.edu/~xou/mulval/">MulVAL</a> format.
        <br>
        You should have prepared: two CSV files - one containing the vertices and the other containing
        the arcs for your network topology.
      </p>
    </div>
    <div>
      <data-driven-input @uploadedData="emitEventUp"></data-driven-input>
    </div>
  </div>  
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