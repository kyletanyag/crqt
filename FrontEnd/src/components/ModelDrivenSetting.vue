<template>
<div>
  <h4> {{ title }} Settings:</h4>
    <p> Please select the product vendor, model, and quantity for your {{ title }}. Use the "Add Server" button to add and "Remove Server" button to remove</p>
    <form>
      <input type="button" style="margin-bottom:5px;" class="btn btn-secondary mx-2" @click="addRow(index)" value="Add Server">
      <!-- <input type="button" @click="removeRow(index)" value="Remove Server"> -->
    </form>

      <table id="AddServer" width="100%">
         <tbody>
            <tr v-for="(row, index) in rows" :key="index" :row="row">
                <td>
                 <input type="button" class="btn btn-secondary mx-2" @click="removeRow(index)" value="Remove">
               </td>
               <td width="25%">
                  <div align="center">
                     <p align="center">Server Type</p>
                     <select v-model="rows[index][0]">
                        <option v-for="item in serverType" :key="item" :value="item" @change="sendDataParent()">{{item}}</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Vendor</p>
                     <select v-model="rows[index][1]">
                        <option v-for="item in vendorServer" :key="item" :value="item" @change="sendDataParent()">{{item}}</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Product</p>
                     <select v-model="rows[index][2]">
                        <option v-for="item in serverProduct" :key="item" :value="item" @change="sendDataParent()">{{item}}</option>                        
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Servers</p>
                         <input type="text" v-model="rows[index][3]" placeholder="Number of Server" @change="sendDataParent()"/>      
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
import http from '@/http-common.js';
import { defineComponent, reactive } from "vue";
import TableLite from "@/components/TableLite.vue";

export default {
  name: 'Model Driven Setting',
    
  component: {
    Multiselect,
    TableLite,
    defineComponent

  },
  props: {
    title: String,
    layer: String,
    type: Array,
    vendor: Array,
    products:Array,
    servers: Number,
    vendorServer: Array,
    serverType: Array,
  },  
  computed: {
    rowData() {
      var nodes = [];
      // nested for loop for numProducts !!!
      for (let i = 0; i < this.numProducts; i++) {
        nodes.push({
          layer: this.layer,
          id: i, // change per layer
          vendor: this.selectedVendor[i],
          // product: this.selectedProduct[i],
          // vulnerabilities: this.selectedVulnerabilities[i]
        });
      }
      return {
        nodes
      };
    },

    selectedType() {
      var x = [];

      this.rows.forEach((i) => {
        x.push(i[0]);
      });
console.log(x)
      return {
        x
    
      };
    }
  },

  watch: {
    selectedVendor() { // double check this !!!
      this.getProducts();
    },
  },

  methods: {
    sendDataParent() {
      this.$emit('DataCall', this.rowData);
    },

    addRow: function(_index){
      this.rows.push([undefined, undefined, undefined, undefined]);
    },
    removeRow: function(_index){
      console.log(_index);

      this.rows.splice(_index, 1);
    },

    getProducts() {
      console.log('Getting products');
      // http.get(/* Some route name */)
    }
  },
 
  data() {
    return{
      rows: [[undefined, undefined, undefined, undefined]],
      selectedServerType: [],
      selectedVendor: [],
      selectedProduct: [],
      numProducts: [],
    };
  },
  
}
</script>

<style>

</style>

