<template>
<div>
    <div class="row"  v-show="this.$route.name != 'Login'">
        <header class="col">
            <nav class="navbar navbar-expand navbar-dark bg-dark mb-3" variant="dark" >
                <strong class="mr-3" style="color:white; font-size:30px;">CRQT |</strong>
                <button class="navbar-toggler"
                        type="button"
                        data-toggle="collapse"
                        data-target="#navbarActual"
                        aria-controls="navbarActual"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarActual">
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item" >
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/">Home</router-link>
                        </li>
                        <li class="nav-item" >
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/NetworkTopology">Network Topology</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/SimulationResults">Simulation Results</router-link>
                        </li>

                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" data-toggle="dropdown">Resilience Metrics</a>
                            <div class="dropdown-menu" style="width: 20em " >
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/Robustness">Robustness</router-link>
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/Redundancy">Redundancy</router-link>
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/Resourcefullness">Resourcefullness</router-link>
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/Rapidity">Rapidity</router-link>
                            </div>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" data-toggle="dropdown">Visualization</a>
                            <div class="dropdown-menu" style="width: 20em">
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/BasicGraphView">Basic Graph View</router-link>
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/ColorGraphView">Color Graph View</router-link>
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/CollapsibleLayout">Collapsible Layout</router-link>
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/ForceLayout">Force Layout</router-link>
                                <router-link class="nav-link" style="color:black;"
                                             active-class="bg-primary text-white"
                                             to="/TidyTree">Tidy Tree Layout</router-link>
                            </div>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/ContactUs">Contact Us</router-link>
                        </li>    
                        <li class="nav-item">
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/Secure">Secure Page</router-link>
                        </li>   
                    </ul>
                </div>
                <div id="log">
                  <router-link v-if="authenticated" to="/Login" v-on:click="logout()" replace>Logout</router-link>
               </div>
            </nav>
        </header>
    </div>
    <div>
      <router-view @authenticated="setAuthenticated" />
    </div>
</div>
</template>

<script>
  export default {
    name: 'App',
    data() {
      return {
        authenticated: true, // change to true when developing
        mockAccount: {
          emailAddress: "email",
          password: "password"
        }
      }
    },
    mounted() {
      if (!this.authenticated) {
        this.$router.replace({ name: "Login" });
      }
    },
    methods: {
      setAuthenticated(status) {
        this.authenticated = status;
      },
      logout() {
        this.authenticated = false;
      }
    }
  }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.button {
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}
.button1 {
  background-color: white; 
  color: black; 
  border: 2px solid #2a79b9;
}
.button1:hover {
  background-color: #2c20d4;
  color: white;
}
.dropdown-menu{
  color: #0d0852;
}
</style>
