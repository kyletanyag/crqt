<template>
  <div class="vertical-center">
    <div class="container">
      <div class="card align-center shadow p-3 mb-5 bg-white rounded">
        <div class="card-body">
        <h1>Two Factor Authentication Setup</h1>
        <p class="mb-0">Then scan the following QR code below to associate your 2FA app with your CRQT account.</p>
        <div class="row justify-content-center" v-html="svg">
        </div>
        <div class="row justify-content-center">
          <div style="text-align: left;">
            <p>Please have one of the following 2FA apps downloaded below on your smartphone device: </p>
            <ul>
              <li v-for="app in totpApps" :key="app">
                <a :href="app.link" target="_blank">{{ app.name }}</a>
              </li>
            </ul>
          </div>
        </div>
        <h5>
          Once you are done, click
          <router-link :to="'/login'" class="font-weight-bold">here</router-link>
          to be sent to login page!
        </h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import http from '../http-common';

export default {
  name: 'QRCode',
    
  data() {

    const svg = ref();
    const totpApps = [
      {
        name: 'Google Authenticator',
        link: 'https://rb.gy/eejbzl'
      },
      {
        name: 'Microsoft Authenticator',
        link: 'https://rb.gy/7nuvy9'
      },
      {
        name: 'FreeOTP Authenticator',
        link: 'https://freeotp.github.io/'
      },
      {
        name: 'Duo Security',
        link: 'https://rb.gy/vqrg6c'
      },
      {
        name: 'or any TOTP/HOTP authentication application.',
        link: 'https://rb.gy/g5jf3m'
      }
    ]

    http.get(`qrcode/${this.id}`).then((r) => {svg.value = r.data; });

    return {
      svg,
      totpApps
    }
  },

  props: {
    id: { 
      type: Number,
      required: true
    },  
  }
}
</script>

<style>
.vertical-center {
  min-height: 100%;  /* Fallback for browsers do NOT support vh unit */
  min-height: 100vh; /* These two lines are counted as one :-)       */

  display: flex;
  align-items: center;
}
</style>