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
}
</script>

<style>
</style>
