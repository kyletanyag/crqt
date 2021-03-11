<template>
<div class="vertical-center">
  <div class="container">
    <div class="card align-center shadow p-3 mb-5 bg-white rounded" style="width: 25rem;">
      <div class="card-body">
        <img class="card-img-top" alt="CRQT logo" src="../assets/logo.png">
        <h2 class="card-title pt-2">Register</h2>
        <form class="needs-validation">
          <div class="form-group">
            <input class="form-control" type="text" v-model="first_name" placeholder="First Name" required/>
          </div>
          <div class="form-group">
            <input class="form-control" type="text" v-model="last_name" placeholder="Last Name" required/>
          </div>
          <div class="form-group">
            <input class="form-control" type="email" autocomplete="off" v-model="email" placeholder="Email Address" required/> 
          </div>
          <div class="form-group">
            <input type="password" class="form-control" name="password" v-model="password" placeholder="Password" required/>
          </div>
          <div class="mb-3 d-flex justify-content-between">
            <div style="display: inline;" class="custom-control custom-switch pl-4.5">
              <input type="checkbox" class="custom-control-input px-2" id="customSwitch1" v-model="dual_factor">
              <label class="custom-control-label" for="customSwitch1">Enable 2FA?</label>
            </div>
            <div style="display: inline;" class="custom-control custom-switch">
              <input type="checkbox" class="custom-control-input px-2" id="customSwitch2" v-model="user_role">
              <label class="custom-control-label" for="customSwitch2">Admin Account?</label>
            </div>
          </div>
        </form>
        <button type="submit" class="btn btn-primary" v-on:click="Register()">Register</button>
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
  name: 'Register',

  data() {
    return {
      email: undefined,
      password: undefined,
      error: undefined,
      first_name: undefined,
      last_name: undefined,
      user_role: 0,
      dual_factor: 0,
    }
  },

  computed: {
    userInfo() {
      return {
        email: this.email,
        password: this.password,
        first_name: this.first_name,
        last_name: this.last_name,
        user_role: this.user_role ? 1 : 0,
        dual_factor: this.dual_factor ? 1: 0,
      };
    }
  },

  methods: {
      Register() {
        http.post('register', this.userInfo).then((r) => {
          console.log(r);
          if (r.data.registered && this.dual_factor) {
            this.$router.replace({name: 'QR Setup', params: {id: r.data.id}})
          } else if (r.data.registered) {
            alert('Thanks for registering! Rerouting back to Login page.')
            this.$router.replace({ name: "Login" });
          } else {
            this.error = r.data.error;
          }
        });
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