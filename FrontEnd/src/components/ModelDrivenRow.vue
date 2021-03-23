<template>
<div>
  <h4> {{ layer }} Settings:</h4>
    <p> Please select the poduct vendor, model, and quantity for your {{ layer }}.</p>
    <!-- <table width=100% border="0" cellspacing="0" >
        <tbody>
          <tr>
              <td width="33%">
                <div align="center">
                    <p align="center">{{ layer }} Vendor</p>
                    <select v-model="selectedVendor" @change="selectVendor">
                      <option v-for="(L1Vend,item) in L1VendorInput" :key="item" :value="item">{{L1Vend.label}}</option>
                    </select>
                </div>
              </td>
              <td align="center" width="33%">
                <div align="center">
                    <p> {{ layer }} Product</p>
                    <select v-model="L1Product">
                      <option v-for="item in L1ProductInput" :key="item" :value="item">{{item}}</option>               
                    </select>
                </div>
              </td>
              <td width="33%">
                <div align="center">
                    <p>Number of Coporate Firewall 1</p>                     
                      <input type="text" v-model="NumberFireWall" placeholder="Number of Firewalls 1" />        
                </div>
              </td>
          </tr>
                <tr width="100%">
              <td>
              <div v-if="selectedVendor != -1">
                <Multiselect 
                    v-model="L1Vendor.options"
                    mode="multiple"
                    placeholder="Select your Vulnerabilites"
                    :options="L1VendorInput[selectedVendor].options"
                    />
              </div>
              </td>
              </tr>
        </tbody>
    </table> -->
</div>
</template>
<script>

import Multiselect from '@vueform/multiselect'
export default {
  name: 'Model Driven Row',

  props: {
    layer: String,
    vendors: Array,
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
}
</script>
<style>
  
</style>