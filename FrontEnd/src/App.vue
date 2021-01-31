<template>
<div>
    <div class="row">
        <header class="col">
            <nav class="navbar navbar-expand navbar-light bg-light mt-3 mb-3">
                <strong class="mr-3">CRQT</strong>
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
                        <li class="nav-item">
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/">Home</router-link>
                        </li>
                        <li class="nav-item">
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
                            <div class="dropdown-menu" style="width: 20em">
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/Robustness">Robustness</router-link>
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/Redundancy">Redundancy</router-link>
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/Resourcefullness">Resourcefullness</router-link>
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/Rapidity">Rapidity</router-link>
                            </div>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" data-toggle="dropdown">Visualization</a>
                            <div class="dropdown-menu" style="width: 20em">
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/BasicGraphView">Basic Graph View</router-link>
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/ColorGraphView">Color Graph View</router-link>
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/CollapsibleLayout">Collapsible Layout</router-link>
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/ForceLayout">Force Layout</router-link>
                                <router-link class="nav-link"
                                             active-class="bg-primary text-white"
                                             to="/TidyTree">Tidy Tree Layout</router-link>
                            </div>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link"
                                         active-class="active"
                                         to="/ContactUs">Contact Us</router-link>
                        </li>
                        
                    </ul>
                </div>
            </nav>
        </header>
    </div>
    <div class="row">
        <div class="container">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
        </div>
    </div>
    <div>
        <router-view />
    </div>
</div>
</template>

<script>
export default {
    name: 'App',
}
</script>

<!--<template>
    <div id="nav">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <router-link to="/about">Network Topology
        <mdb-dropdown-item router-link to="/about">Network Topology</mdb-dropdown-item></router-link><router-view />
    </div>

</template>-->
<!--<template>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div id="nav">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Link</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Dropdown
                    </a>
                    <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <a class="dropdown-item" href="#">Action</a>
                        <a class="dropdown-item" href="#">Another action</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">Something else here</a>
                    </div>
                </li>
                <li class="nav-item">
                    <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
                </li>
            </ul>
            <form class="form-inline my-2 my-lg-0">
                <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
            </form>
        </div>
    </nav>`

</template>-->
<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    #nav {
        padding: 30px;
    }

        #nav a {
            font-weight: bold;
            color: #2c3e50;
        }

            #nav a.router-link-exact-active {
                color: #42b983;
            }
</style>
