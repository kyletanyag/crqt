<template>
  <img alt="CRQT logo" src="../assets/logo.png">
  <h3 align="center">Log In</h3>
  <form>
    <input type="submit" style="display: none">
    <input type="text" name="emailAddress" v-model="email" placeholder="Email Address" />
    <input type="password" name="password" v-model="password" placeholder="Password" />
    <button type="button" v-on:click="login()">Log in</button>
  </form>
  <router-link to="/Register" tag="button">Don't have an account? Click here to register!</router-link>
</template>

<script>
import http from '../http-common.js';

export default {
  name: 'Login',

  data() {
    return {
      email: "",
      password: ""
    }
  },
  methods: {
      login() {
        if(this.email != "" && this.password != "") {
            // if(this.input.emailAddress == this.$parent.mockAccount.emailAddress && this.input.password == this.$parent.mockAccount.password) {
            
          http.post('verify_user', {'email': this.email, 'password': this.password}).then((r) => {
            if (r.data.access) {
              this.$emit("authenticated", true);
              this.$router.replace({ name: "Secure" });
            }
          });


        }
        //     if(this.input.email == "email" && this.input.password == "password") {
        //         this.$emit("authenticated", true);
        //         this.$router.replace({ name: "Secure" });
        //     } else {
        //         console.log("The email address and / or password is incorrect");
        //     }
        // } else {
        //     console.log("An email address and password must be present");
        // }
      },
  }
}
</script>