<template>
  <div class="container">
    <div v-html="svg">
    </div>
    <p>QR CODE</p>
  </div>
</template>

<script>
import { ref } from 'vue';
import http from '../http-common';

export default {
  name: 'QRCode',
    
  data() {

    const svg = ref();

    http.get(`qrcode/${this.username}`).then((r) => {svg.value = r.data; });

    return {
        svg
    }
  },

  props: {
    username: { 
      type: String,
      required: true
    },
  }
}
</script>
