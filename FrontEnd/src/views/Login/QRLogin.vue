<template>
<div class="vertical-center">
  <div class="container">
    <div class="card align-center shadow p-3 mb-5 bg-white rounded" style="width: 25rem;">
      <div class="card-body">
        <img class="card-img-top" alt="CRQT logo" src="../../assets/logo.png">
        <h2 class="card-title pt-2">2FA</h2>
        <div>
          <div class="form-group">
            <input class="form-control" type="password" autocomplete="off" name="pin" v-model="pin" placeholder="OTP Pin" @keypress="keyEnter" /> 
          </div>
          <button type="submit" class="btn btn-primary" v-on:click="login()">Log in</button>
        </div>
      </div>
    </div>
    <transition name="fade">    
      <div v-show="error" class="alert alert-danger">
        <h3>{{ error }}</h3>
      </div>
    </transition>
  </div>
</div>
</template>

<script>
import http from '../../http-common.js';

export default {
  name: 'QR Login',

  data() {
    return {
      pin: "",
      error: undefined,
    }
  },

  props: {
    id: Number,
  },

  methods: {
    login() {
      http.post(`verify_otp/${this.id}`, {pin: this.pin}).then((r) => {
        console.log(r);

        if (r.data.access) {
          this.$emit("authenticated", true);
          this.$router.replace({ name: "Home" });
        } else {
          this.error = r.data.error;
        }
      });
    },

    keyEnter(e) {
      if ((e && e.keyCode === 13) || e === 0) {
        this.login();
      }
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
.card {
    margin: 0 auto; /* Added */
    float: none; /* Added */
    margin-bottom: 10px; /* Added */
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>