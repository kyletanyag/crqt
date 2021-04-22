<template>
<div class="container">
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <h1>Admin Page</h1>
  <p class="text-justify lead">
    This is the admin page. This page is restricted to only users with elevated privilges.
    From this page, you can do user account managment as well as adjust simulation 
    configurations for the model-driven component of this tool.
  </p>
  <hr>
  <div v-if="accountManagement">
    <h2>Account Management</h2>
    <p>
      In this section, you can approve/delete requested accounts as well as see your organization's user database.
    </p>
    <div v-if="!loadingUnregistered" class="row justify-content-center">
      <user-data-table @approve="fetchData" @delete="fetchUnregistered"
        title="Unregistered Users" 
        :users="unregisteredUsers"
        :happyError="true"
        :info="false"
        ></user-data-table>
    </div>
    <div v-else>
      Loading ...
    </div>
    <div v-if="!loadingRegistered" class="row justify-content-center">
      <user-data-table @delete="fetchRegistered"
        title="Registed Users" 
        :users="registeredUsers"
        :approve="false"
        :info="false"></user-data-table>
    </div>
    <div v-else>
      Loading ...
    </div>
    <hr>
  </div>
  <div class="pb-5" v-if="simulationManagement">
    <h2>Simulation Management</h2>
    <p class="text-left">
      In this section, you can add additional selection options to the model-driven network
      topology input interface. Make sure you use the check button before adding a new product 
      to make sure that product is available to use according to NIST's NVD. If you need a list 
      of possible products you could use, please visit <a href="http://localhost:2000/browse" target="_blank">here!</a>
    </p>
    <div class="row justify-content-center">
      <div class="col">
        <div class="card mt-4" >
          <div class="card-header font-weight-bold">
            Add Products
          </div>
          <div class="card-body">
            <form>
              <div class="mb-3">
                <label class="form-label">Vendor</label>
                <input type="text" v-model="vendorInput" class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Product</label>
                <input type="text" v-model="productInput" class="form-control">
              </div>
              <div>
                <label>Type</label>
                <div class="form-check">
                  <input class="form-check-input" name="type" type="radio" value="firewall" v-model="typeInput">
                  <label class="form-check-label">
                    Firewall
                  </label>
                </div>
                <div class="form-check">
                  <input class="form-check-input" name="type"  type="radio" value="server" v-model="typeInput">
                  <label class="form-check-label">
                    Server
                  </label>
                </div>
              </div>
            </form>
            <hr>
            <div>
              <button @click="checkInput" class="btn btn-secondary mx-2">
                Check
              </button>
              <button @click="addProduct()" :disabled="!isGood" class="btn btn-success mx-2">
                Add
              </button>
            </div>
            <div v-if="status">
              <hr>
              <div :class="cssInputStatus()">
                {{status}}
              </div>
            </div>
          </div>
        </div>
      </div>
      <product-data-table v-if="!loadingProducts"
        title="Available Model-Driven Choices"
        :data="products"
        :height="500"
        @delete="fetchProducts"
      />
      <div class="col" v-else>
        Loading ...
      </div>
    </div>
  </div>
</div>
</template>
<script>
import UserDataTable from '@/components/UserDataTable.vue'
import ProductDataTable from '@/components/ProductDataTable.vue'
import http from '@/http-common.js';
import axios from 'axios';

export default {
  
  name: 'Admin',

  components: { 
    UserDataTable,
    ProductDataTable
  },

  data() {
    return {
      error: undefined,
      unregisteredUsers: [],
      registeredUsers: [],
      products: [],
      loadingUnregistered: false,
      loadingRegistered: false,
      loadingProducts: false,
      accountManagement: true,
      simulationManagement: true,
      typeInput: 'firewall',
      vendorInput: '',
      productInput: '',
      status: undefined,
    }
  },
  
  created() {
    this.fetchData();
  },

  methods: {

    fetchData() {
      this.fetchUnregistered();
      this.fetchRegistered();
      this.fetchProducts();
    },

    fetchUnregistered() {
      this.loadingUnregistered = true;
      http.get('/get_unregistered_users').then((r) => {
        this.unregisteredUsers = r.data.unregistered_users;
        this.loadingUnregistered = false;
      }).catch((e) => {
          this.error = e;
      });
    },

    fetchRegistered() {
      this.loadingRegistered = true;
      http.get('/get_registered_users').then((r) => {
        this.registeredUsers = r.data.registered_users;
        this.loadingRegistered = false;
      }).catch((e) => {
          this.error = e;
      });
    },

    fetchProducts() {
      this.loadingProducts = true;
      http.get('/get_all_products').then((r) => {
        this.products = r.data.query;
        this.loadingProducts = false;
      }).catch((e) => {
          this.error = e;
      });
    },

    checkInput() {
      if(!this.hasInput) return;

      axios.get(`http://localhost:2000/api/search/${this.vendorInput.toLowerCase()}/${this.productInput.toLowerCase()}`).then((r) => {
        console.log(r);
        this.status = r.data.results.length > 0 ? 'Acceptable Product!' : 'Unable to Find Product.'
      }).catch((e) => {
        this.error = e;
        this.status = e;
      });
    },

    addProduct() {
      http.post('/product_add', this.input).then((r) => {
        console.log(r);
        if ('error' in r.data) this.status = r.data.error;
        if ('status' in r.data) this.status = r.data.status;
      }).catch((e) => {
        this.error = e;
      })
    },

    cssInputStatus() {
      return this.status === 'Acceptable Product!' || this.status ===  'Product Added!' ? 'alert alert-success' : 'alert alert-danger'
    }
  },
  
  computed: {
    input() {
      return {
        vendor: this.vendorInput,
        product: this.productInput,
        type: this.typeInput
      }
    },

    isGood() {
      return this.status === 'Acceptable Product!';
    },

    hasInput() {
      return this.vendorInput != '' && this.productInput != '';
    }
  }
}
</script>
<style>

</style>