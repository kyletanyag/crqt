<template>
<div>
  <h4> {{ title }} Settings:</h4>
  <div class="pb-2"> 
    Please select the vendor, product, quantity, and associated vulnerabilites for {{ title }}.
  </div>
  <table class="table table-bordered" style="width: 80%">
      <tbody>
        <tr>
            <td width="15%">
              <div class="pt-1 text-center px-0 mx-0">
                <h5>Vendor</h5>
                <select style="width: 50%;" v-model="selectedVendor">
                  <option class="text-center" v-for="item in vendors" :key="item" :value="item">{{ item }}</option>
                </select>
              </div>
            </td> 
            <td width="20%">
              <div class="text-center pt-1 pb-2">
                <h5>Product</h5>
                <select style="width: 60%" v-model="selectedProduct">
                  <option v-for="item in products" :key="item" :value="item">{{ item }}</option>               
                </select>
              </div>
            </td>
            <td width="15%">
              <div class="text-center pt-1 pb-2">
                <h5>Number of Firewalls</h5>                     
                <input style="width: 50%" type="number" v-model="numfirewalls" placeholder="1" min="1"
                  onkeyup="if(this.value < 0) this.value = 1;"/>
              </div>
            </td> 
            <td width="20%">
              <div class="text-center">
                <h5>Vulnerabilites</h5>
                <Multiselect 
                  v-model="selectedVulnerabilities"
                  mode="multiple"
                  placeholder="Select your Vulnerabilites"
                  :options="vulnerability_list"
                />
              </div>
            </td>
          </tr>
      </tbody>
  </table>
</div>
</template>
<script>
/* eslint-disable */
import Multiselect from '@vueform/multiselect';
import http from '@/http-common.js';
import axios from 'axios';

export default {
  name: 'Model Driven Firewall',
  computed: {
    rowData() {
      var nodes = [];
      for (let i = 0; i < this.numfirewalls; i++) {
        let cve_list = [];
        for (let j = 0; j < this.selectedVulnerabilities.length; j++)  {
          cve_list.push(this.vulnerability_list[this.selectedVulnerabilities[j]]);
        }
        nodes.push({
          layer: this.layer,
          id: i, 
          vendor: this.selectedVendor,
          product: this.selectedProduct, 
          cve_ids: this.selectedVulnerabilities.length > 0 ? cve_list : JSON.parse(JSON.stringify(this.vulnerability_list))
        });
      }
      return nodes;
    },
  },
  watch: {
    selectedVendor() { 
      http.get(`product_query/firewall/${this.selectedVendor}`)
      .then((r) => {
        if (r.data.error) console.log(r.data.error);
        this.products = r.data.query;
      });
    },
    selectedProduct() { // Example of how to get data from CVE-Search !!! 
    this.vulnerability_list = [];
      axios.get(`http://localhost:2000/api/search/${this.selectedVendor.toLowerCase()}/${this.selectedProduct.toLowerCase()}`).then((r) => {
        console.log(r);
        r.data.results.forEach((e) => {this.vulnerability_list.push(e.id)});
      });
    }
  },
  props: {
    title: String,
    layer: String,
    vendors: Array,
    product: Array,
  },
  
  components: {
    Multiselect,
  },
  
  methods: {
  },
  data() {
    return {
      selectedVendor: undefined, 
      selectedProduct: undefined,
      selectedVulnerabilities: [],
      numfirewalls: 1,
      products: [],
      vulnerability_list: [],
    };
  }
}
</script>
<style>
  
</style>