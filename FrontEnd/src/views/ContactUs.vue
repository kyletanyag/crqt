<template>
<div>
  <div class="about">
      <h1>This is the About page</h1>
  </div>
</div>
  <hello-world :msg="test"> </hello-world>
</template>

<script>
import HelloWorld from '../components/HelloWorld.vue'
export default {
  components: { HelloWorld },
  name: 'ContactUs'
  
}
</script>