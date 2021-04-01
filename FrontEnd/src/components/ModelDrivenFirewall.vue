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
              <!-- <div v-if="selectedVendor != -1">
                <Multiselect 
                    v-model="L1Vendor"
                    mode="multiple"
                    placeholder="Select your Vulnerabilites"
                    :options="vendors[selectedVendor].options"
                    />
              </div> -->
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
// import axios from 'axios';
export default {
  name: 'Model Driven Firewall',

  computed: {
    rowData() {
      var nodes = [];
        for(let j = 0; j < this.numfirewalls; j++) {
          nodes.push({
            layer: this.layer,
            id: j, 
            vendor: this.selectedVendor,
            product: this.selectedProduct, 
            // vulnerabilities: this.selectedVulnerabilities[i]
          });
        }
      return nodes;
    },
  },

  watch: {
    selectedVendor() { // double check this !!!
      http.get(`product_query/firewall/${this.selectedVendor}`)
      .then((r) => {
        if (r.data.error) console.log(r.data.error);
        this.products = r.data.query;
      });
    },

    selectedProduct() {
      // Example of how to get data from CVE-Search !!! 
      // axios.get('http://localhost:2000/api/search/microsoft/windows_xp').then((r) => {
      //     r.data.results.forEach((e) => {console.log(e.id)});
      // });
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
      L1Vendor:[],
      numfirewalls: 1,
      products: [],
    };
  }
}
</script>
<style>
  
</style>