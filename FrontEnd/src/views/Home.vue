<template>
    <div class="home">
        <img alt="CRQT logo" src="../assets/logo.png">
        <H1>Welcome to the Cyber Resilience Quantification Tool (CRQT)</H1>
        <h3 align="center">Log In</h3>
        <div id="login">
            <h1>Login</h1>
            <input type="text" name="emailAddress" v-model="input.emailAddress" placeholder="Email Address" />
            <input type="password" name="password" v-model="input.password" placeholder="Password" />
            <button type="button" v-on:click="login()">Log in</button>
        </div>
    </div>
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
    
// // @ is an alias to /src
//     import HelloWorld from '@/components/HelloWorld.vue';
//     import Demo from '@/components/Demo.vue';
//     export default {
//         name: 'Home',
//         components: {
//             HelloWorld,
//             Demo
//         }
//     }
</script>
