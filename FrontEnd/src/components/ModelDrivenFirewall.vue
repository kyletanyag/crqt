<template>
<div>
  <h4> {{ title }} Settings:</h4>
  
    <p> Please select the product vendor, model, and quantity for your {{ layer }}.</p>
    <table width=100% border="0" cellspacing="0" >
        <tbody>
          <tr>
              <td width="33%">
                <div align="center">
                    <p align="center">{{ title }} Vendor</p>
                    <select v-model="selectedVendor">
                      <option v-for="item in vendors" :key="item" :value="item">{{ item }}</option>
                    </select>
                </div>
              </td> 
              <td align="center" width="33%">
                <div align="center">
                    <p> {{ title }} Product</p>
                    <select v-model="selectedProduct">
                      <option v-for="item in products" :key="item" :value="item">{{ item }}</option>               
                    </select>
                </div>
              </td>
              <td width="33%">
                <div align="center">
                    <p>Number of Coporate Firewall 1</p>                     
                      <!-- <input type="text" v-model="NumberFireWall" placeholder="Number of Firewalls 1" />         -->
                      <input type="text" v-model="numfirewalls" placeholder="1" />
                </div>
              </td> 
          </tr>
          <tr width="100%">
              <td>
              <div v-if="selectedProduct">
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
        let cve_list = []
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