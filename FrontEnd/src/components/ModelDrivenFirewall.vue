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
                      <option v-for="(L1Vend,item) in vendors" :key="item" :value="L1Vend.label" @change="sendDataParentFirwall">{{L1Vend.label}}</option>
                    </select>
                </div>
              </td> 
              <td align="center" width="33%">
                <div align="center">
                    <p> {{ title }} Product</p>
                    <select v-model="selectedProduct">
                      <option v-for="item in products" :key="item" :value="item" @change="sendDataParentFirwall">{{item}}</option>               
                    </select>
                </div>
              </td>
              <td width="33%">
                <div align="center">
                    <p>Number of Coporate Firewall 1</p>                     
                      <!-- <input type="text" v-model="NumberFireWall" placeholder="Number of Firewalls 1" />         -->
                      <input type="text" v-model="numfirewalls" placeholder="Number of Firewalls" @change="sendDataParentFirwall" />
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

import Multiselect from '@vueform/multiselect';
import http from '@/http-common.js';
import axios from 'axios';
export default {
  
  name: 'Model Driven Firewall',
  computed: {

    rowData() {
      var nodes = [];
      
        for(let j=0; j< this.numfirewalls;j++){
          
          nodes.push({
            layer: this.layer,
            id: j, 
            vendors: this.selectedVendor,
            products: this.selectedProduct,
            firewalls: this.numfirewalls,      
            // vulnerabilities: this.selectedVulnerabilities[i]
          });
          console.log(nodes)
        }
      
      return {
        nodes
      };
    },
    sendDataParentFirwall(){
      console.log("Sending data to the parent")
      this.$emit('DataCall', this.rowData);
      return{
        
      }
    }

  },

  watch: {
    selectedVendor() { // double check this !!!
      http.get(`product_query/firewall/${this.selectedVendor}`)
      .then((r) => {
        if (r.data.error)
          console.log(r.data.error);
          
        var temp = [];
        r.data.query.forEach((e) => {
          temp.push(e.product)
        });

        this.products = temp;
      })
      .catch(() => {
        console.log('Cannot complete query. Invalid data.');
      });
    },
  },

  props: {
    title:String,
    layer: String,
    vendors: Array,
    vendor: Array,
    product:Array,
    firewalls: Number,
  },
  
  component: {
    Multiselect,
  },
  

  methods: {
    sendDataParent() {
      this.$emit('DataCall', this.rowData);
    }
  },
  data(){
    axios.get('http://localhost:2000/api/search/microsoft/windows_xp').then((r) => {
        r.data.results.forEach((e) => {console.log(e.id)});
    });
    return{
      selectedVendor:[], 
      selectedProduct:[],
      L1Vendor:[],
      numfirewalls:[],
      products: [],
    };
  }
}
</script>
<style>
  
</style>