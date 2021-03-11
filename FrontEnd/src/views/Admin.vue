<template>
<div class="container">
  <h1>Admin Page</h1>
  <p class="text-justify lead">
    This is the admin page. This page is restricted to only users with elevated privilges.
    From this page, you can do user account managment as well as adjust simulation 
    configurations for the model-driven component of this tool.
  </p>
  <hr>
  <!-- <div class="text-right">
    <button class="btn btn-danger" @click="accountManagement = !accountManagement">
      X
    </button>
  </div> -->
  <div v-show="accountManagement">
    <h2>Account Management</h2>
    <div v-if="!loadingUnregistered" class="row justify-content-center">
      <user-data-table @approve="fetchData" @delete="fetchUnregistered"
        title="Unregistered Users" 
        :users="unregisteredUsers"
        :happyError="true"
        ></user-data-table>
    </div>
    <div v-else>
      Loading ...
    </div>
    <div v-if="!loadingRegistered" class="row justify-content-center">
      <user-data-table @delete="fetchRegistered"
        title="Registed Users" 
        :users="registeredUsers"
        :approve="false"></user-data-table>
    </div>
    <div v-else>
      Loading ...
    </div>
    <hr>
  </div>
  <div v-show="simulationManagement">
    <h2>Simulation Management</h2>
    <p>To be developed ...</p>
  </div>
</div>
</template>
<script>
import UserDataTable from '../components/UserDataTable.vue'
import http from '../http-common.js';

export default {
  
  name: 'Admin',

  components: { 
    UserDataTable 
  },

  data() {
    return {
      unregisteredUsers: [],
      registeredUsers: [],
      loadingUnregistered: false,
      loadingRegistered: false,
      accountManagement: true,
      simulationManagement: true,
    }
  },
  
  created() {
    this.fetchUnregistered();
    this.fetchRegistered();
  },

  methods: {

    fetchData() {
      this.fetchUnregistered();
      this.fetchRegistered();
    },

    fetchUnregistered() {
      this.loadingUnregistered = true;
      http.get('get_unregistered_users').then((r) => {
        this.unregisteredUsers = r.data.unregistered_users;
        this.loadingUnregistered = false;
      });
    },

    fetchRegistered() {
      this.loadingRegistered = true;
      http.get('get_registered_users').then((r) => {
        this.registeredUsers = r.data.registered_users;
        this.loadingRegistered = false;
      });
    },
  },
  
}
</script>
<style>

</style>