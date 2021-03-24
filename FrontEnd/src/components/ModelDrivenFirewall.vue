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
                      <option v-for="(L1Vend,item) in vendors" :key="item" :value="item">{{L1Vend.label}}</option>
                    </select>
                </div>
              </td> 
              <td align="center" width="33%">
                <div align="center">
                    <p> {{ title }} Product</p>
                    <select>
                      <option v-for="item in products" :key="item" :value="item">{{item}}</option>               
                    </select>
                </div>
              </td>
              <td width="33%">
                <div align="center">
                    <p>Number of Coporate Firewall 1</p>                     
                      <!-- <input type="text" v-model="NumberFireWall" placeholder="Number of Firewalls 1" />         -->
                      <input type="text" placeholder="Number of Firewalls" />
                </div>
              </td> 
          </tr>
          <tr width="100%">
              <td>
              <div v-if="selectedVendor != -1">
                <Multiselect 
                    v-model="L1Vendor"
                    mode="multiple"
                    placeholder="Select your Vulnerabilites"
                    :options="vendors[selectedVendor].options"
                    />
              </div>
              </td>
              </tr>
        </tbody>
    </table>
</div>
</template>
<script>

import Multiselect from '@vueform/multiselect'
export default {
  
  name: 'Model Driven Firewall',

  props: {
    title:String,
    layer: String,
    vendors: Array,
    products: Array,
    servers: Number,
  },
  
  component: {
    Multiselect,
  },
  
  computed: {
    rowData() {
      return {

      };
    },
  },

  methods: {
    sendDataParent() {

      this.$emit('DataCall', this.rowData);
    }
  },
  data(){
    return{
      selectedVendor:-1, 
      L1Vendor:[],
    };
  }
}
</script>
<style>
  
</style>