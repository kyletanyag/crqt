<template>
<div class="pt-5 mt-5">
  <div class="pt-5">
    <img alt="CRQT logo" src="../assets/logo.png">
    <h1 class="pt-2">Welcome to the Cyber Resilience Quantification Tool (CRQT)</h1>
    <h2>Developed by: </h2>
      <ul class="list-unstyled">
        <li v-for="member in team" :key="member">
          <h4>
            {{ member }}
          </h4>
        </li>
      </ul>
  </div>
</div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Home',

  data() {
    return {
      team: [
        'Gul Ayaz',
        'Cierra Hall',
        'Thomas Laverghetta',
        'Alex Soliza',
        'Kyle Tanyag'
      ]
    }
  },

  created() {
    axios.get('http://localhost:5000/test_connection')
      .then((r) => {
        console.log(r);
        axios.get('http://localhost:2000/api/browse/microsoft')
          .then((r) => {
            console.log(r);
          })
          .catch(() => {
            this.$router.push({name: 'Error', params: {errorCode: 'CVE-Search'}})
          })
      })
      .catch(() => {
        this.$router.push({name: 'Error', params: {errorCode: 'Flask'}})
      });
  },
}
</script>

<style>
</style>
