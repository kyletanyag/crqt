<template>
  <div class="container">
    <h1>Two Factor Authentication Setup</h1>
    <div class="row justify-content-center">
      <div style="text-align: left;">
        <p>Please have one of the following 2FA apps downloaded below on your smartphone device: </p>
        <ul>
          <li v-for="app in totpApps" :key="app">
            <a :href="app.link" target="_blank">{{ app.name }}</a>
          </li>
        </ul>
        Then scan the following QR code below to associate your 2FA app with your CRQT account.
      </div>
    </div>
    <div class="row justify-content-center" v-html="svg">
    </div>
    <div>
      Once you are done, click
      <router-link :to="'/login'" class="font-weight-bold">here</router-link>
      to be sent to login page!
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

    http.get(`qrcode/${this.email}`).then((r) => {svg.value = r.data; });

    return {
      svg,
      totpApps
    }
  },

  props: {
    email: { 
      type: String,
      required: true
    },  
  }
}
</script>
