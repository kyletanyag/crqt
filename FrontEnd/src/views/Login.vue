<template>
<div class="vertical-center">
  <div class="container">
    <div class="card align-center shadow p-3 mb-5 bg-white rounded" style="width: 25rem;">
      <div class="card-body">
        <img class="card-img-top" alt="CRQT logo" src="../assets/logo.png">
        <h2 class="card-title pt-2">Login</h2>
        <div>
          <div class="form-group">
            <input class="form-control" name="email" autocomplete="off" v-model="email" placeholder="Email Address" @keypress="keyEnter"/> 
          </div>
          <div class="form-group">
            <input type="password" class="form-control" name="password" v-model="password" placeholder="Password" @keypress="keyEnter" />
          </div>
          <button type="submit" class="btn btn-primary" v-on:click="login()">Log in</button>
        </div>
        <hr>
        <router-link to="/Register" tag="button">Don't have an account? Click here to register!</router-link>
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
import http from '../http-common.js';

export default {
  name: 'Login',

  data() {
    return {
      email: "",
      password: "",
      error: undefined,
    }
  },

  computed: {
    credentials() {
      return {
        email: this.email,
        password: this.password,
      };
    }
  },

  methods: {
    login() {
      http.post('verify_user', this.credentials).then((r) => {
        if (r.data.dual_factor) {
          this.$router.replace({ name: "QR Login", params: {id: r.data.id} });
        } else if (r.data.access) {
          this.$emit("authenticated", true);
          this.$router.replace({ name: "Secure" });
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