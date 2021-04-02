<template>
<div>
  <h4> {{ title }} Settings:</h4>
 
    <p> Please select the product vendor, model, and quantity for your {{ title }}. Use the "Add Server" button to add and "Remove Server" button to remove</p>
    <form>
      <input type="button" style="margin-bottom:5px;" class="btn btn-secondary mx-2" @click="addRow(index)" value="Add Server">
    </form>
      <table id="AddServer" width="100%">
         <tbody>
            <tr v-for="(row, index) in rows" :key="index" :row="row">
               <td>
                 <input type="button" class="btn btn-secondary mx-2" @click="removeRow(index)" value="Remove">
               </td>
               <td width="20%">
                  <div align="center">
                     <p align="center">Server Type</p>
                     <select v-model="rows[index][0]">
                        <option v-for="item in serverTypes" :key="item" :value="item">{{item}}</option>
                     </select>
                  </div>
               </td>
               <td width="20%">
                  <div align="center">
                     <p>Server Vendor</p>
                     <select v-model="rows[index][1]" @change="getProducts(index)">
                        <option v-for="item in vendors" :key="item" :value="item">{{item}}</option>
                     </select>
                  </div>
               </td>
               <td width="20%">
                  <div align="center">
                     <p>Server Product</p>
                     <select v-model="rows[index][2]">
                        <option v-for="item in serverProduct[index]" :key="item" :value="item">{{item}}</option>                        
                     </select>
                  </div>
               </td>
               <td width="20%">
                  <div align="center">
                     <p>Number of Servers</p>
                         <input type="text" v-model="rows[index][3]" placeholder="None" @click="getRowData"/>      
                  </div>
               </td>
               <td width="20%">
                <div>
                  <Multiselect v-if="rows[index][2]" 
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
import Multiselect from '@vueform/multiselect'
import http from '@/http-common.js';
export default {
  name: 'Model Driven Setting',
    
  components: {
    Multiselect,
  },

  props: {
    title: String,
    layer: String,
    vendors: Array,
    serverTypes: Array,
  },  
  
  computed: {
    rowData() {
      var nodes = []
      for (let i = 0; i < this.rows.length; i++) {
        for(let j = 0; j < this.rows[i][3]; j++){
          nodes.push({
            layer: this.layer,
            id: j, 
            type:this.rows[i][0],
            vendor: this.rows[i][1],
            product: this.rows[i][2],   
            // vulnerabilities: this.selectedVulnerabilities[i]
          });
        }
      }
      return nodes;
    }
  },

  methods: {
    addRow() {
      this.rows.push([undefined, undefined, undefined, 1]);
    },
    removeRow(index) {
      this.rows.splice(index, 1);
    },
    getProducts(index) {
      http.get(`/product_query/server/${this.rows[index][1]}`).then((r) => {
        // console.log(r);
        if (r.data.error) console.log(r.data.error);
        this.serverProduct[index] = r.data.query;
      });
    },
  },
  data() {
    return{
      rows: [[undefined, undefined, undefined, 1]],
      serverProduct: [],
      selectedVulnerabilities:[]
    };
  },
}
</script>

<style>
</style>
