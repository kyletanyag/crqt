<template>
<div class="container-fluid">
    <div class="row" v-show="this.$route.name != 'Login'
       && this.$route.name != 'Register'
       && this.$route.name != 'QR Login'
       && this.$route.name != 'QR Setup'">
        <header class="col-12 px-0">
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
                        <li class="nav-item dropdown" >
                          <a class="nav-link dropdown-toggle" data-toggle="dropdown">Network Topology</a>
                          <div class="dropdown-menu" >
                            <router-link class="nav-link" style="color: black;"
                                         active-class="bg-primary text-white"
                                         to="/network-topology/data-driven">Data-Driven</router-link>
                            <router-link class="nav-link" style="color: black;"
                                         active-class="bg-primary text-white"
                                         to="/network-topology/model-driven">Model-Driven</router-link>                                         
                          </div>
                        </li>
                        <li class="nav-item dropdown" >
                          <a class="nav-link dropdown-toggle" data-toggle="dropdown">Simulation Results</a>
                          <div class="dropdown-menu" >
                            <router-link class="nav-link" style="color: black;"
                                         active-class="bg-primary text-white"
                                         :class="{ disabled: !dataDriven }"
                                         to="/simulation-results/data-driven">Data-Driven</router-link>
                            <router-link class="nav-link" style="color: black;"
                                         active-class="bg-primary text-white"
                                         :class="{ disabled: !modelDriven }"
                                         to="/simulation-results/model-driven">Model-Driven</router-link>                                         
                          </div>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/About">About</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/FAQ">FAQ</router-link>
                        </li>                             
                    </ul>
                </div>
                <div v-if="admin" class="pr-4">
                  <router-link v-if="admin" to="/Admin" replace>Admin</router-link>
                </div>
                <div id="log">
                  <router-link v-if="authenticated" to="/Login" @click="logout()" replace>Logout</router-link>
               </div>
            </nav>
        </header>
    </div>
    <div>
      <router-view @authenticated="setAuthenticated" @uploadedData="checkforResults" @adminAccount="setAdmin" />
    </div>
</div>
</template>

<script>
import http from '@/http-common.js';
export default {
  name: 'App',

  data() {
    return {
      authenticated: true, /// change to true when developing
      dataDriven: false,
      modelDriven: false,
      admin: true  /// change to true to pretend to be admin account
    }
  },

  mounted() {
    if (!this.authenticated && this.$route.name != 'Login' && this.$route.name != 'Register') {
      this.$router.replace({ name: 'Login' });
    }
  },
  
  created() { 
    this.checkforResults();
  },

  methods: {
    setAuthenticated(status) {
      this.authenticated = status;
    },

    setAdmin(status) {
      this.admin = status;
    },

    logout() {
      this.authenticated = false;
    },

    checkforResults(){
      http.get('/data_driven/get_network_title').then((r) => {
        
        r.data.network_title !== "" ? this.dataDriven = true : this.dataDriven = false;
      }).catch((e) => {
        console.log(e);
        this.dataDriven = false;
      });

      http.get('/model_driven/get_network_title').then((r) => {
        r.data.network_title !== "" ? this.modelDriven = true: this.modelDriven = false;
      }).catch((e) => {
        console.log(e);
        this.modelDriven = false;
      });
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
  /* font-size: 12pt; */
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

.dropdown-menu{
  color: #0d0852;
}

.disabled {
    opacity: 0.5;
    pointer-events: none;
}
</style>
