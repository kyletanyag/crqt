<template>
    <img alt="CRQT logo" src="../assets/logo.png">
    <h3 align="center">Log In</h3>
    <form>
        <input type="submit" style="display: none">
        <input type="text" name="emailAddress" v-model="input.emailAddress" placeholder="Email Address" />
        <input type="password" name="password" v-model="input.password" placeholder="Password" />
        <button type="button" v-on:click="login()">Log in</button>
    </form>
    <router-link to="/Register" tag="button">Don't have an account? Click here to register!</router-link>
</template>

<script>
    export default {
        name: 'Login',
        data() {
            return {
                input: {
                    emailAddress: "",
                    password: ""
                }
            }
        },
        methods: {
            login() {
                if(this.input.emailAddress != "" && this.input.password != "") {
                    // if(this.input.emailAddress == this.$parent.mockAccount.emailAddress && this.input.password == this.$parent.mockAccount.password) {
                    if(this.input.emailAddress == "email" && this.input.password == "password") {
                        this.$emit("authenticated", true);
                        this.$router.replace({ name: "Secure" });
                    } else {
                        console.log("The email address and / or password is incorrect");
                    }
                } else {
                    console.log("An email address and password must be present");
                }
            }
            
        }
    }
</script>