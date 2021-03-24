<template>
<div>
  <h4> {{ title }} Settings:</h4>
    <p> Please select the product vendor, model, and quantity for your {{ title }}. Use the "Add Server" button to add and "Remove Server" button to remove</p>
    <form>
      <input type="button" @click="addRow(index)" value="Add Server">
      <input type="button" @click="removeRow(index)" value="Remove Server">
    </form>
      <table id="AddServer" class="table-hover" width="100%" border="0" cellspacing="0" selectionMode="multiple"
        selectedClass="table-info">
         <tbody>
            <tr v-for="(row, index) in rows" :key="index" :row="row">
               <td width="25%">
                  <div align="center">
                     <p align="center">Server Type</p>
                     <select v-model="emailServer[index]">
                        <option v-for="item in emailServer" :key="item" :value="item">{{item}}</option>
                        
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Vendor</p>
                     <select v-model="serverVendor[index]">
                        <option v-for="item in vendorServer" :key="item" :value="item">{{item}}</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Product</p>
                     <select v-model="serverProduct[index]">
                        <option v-for="item in serverProduct" :key="item" :value="item">{{item}}</option>                        
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Servers</p>
                         <input type="text" v-model="numberServer" placeholder="Number of Server" />      
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
</div>
</template>
<script>
/* eslint-disable */ 
import Multiselect from '@vueform/multiselect'
export default {
  
  name: 'Model Driven Setting',

  props: {
    title: String,
    layer: String,
    type: Array,
    vendor: Array,
    products:Array,
    servers: Number,
    vendorServer: Array,
    emailServer: Array,
    serverProduct: Array,
    numberServer: Array,
    serverVendor: Array,
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
    },

    addRow: function(_index){
         this.rows.splice(_index+1,0, this.rows[_index]);
    },
    removeRow: function(_index){
      //console.log(row);d
      this.rows.splice(_index-1, 1);
    },
  },
 
  data() {
    return{
      rows: [1],
      selectedVendor:-1, 
    };
  }
  
}
</script>
<style>
  
</style>