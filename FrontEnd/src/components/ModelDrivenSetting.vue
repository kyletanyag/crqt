<template>
<div>
  <h4> {{ title }} Settings:</h4>
  <div class="pb-2"> 
    <p style="width: 80%">
      Please select the product vendor, model, and quantity for your {{ title }}. 
      Use the "Add Server" button to add a new row and "Remove Server" button to remove a row.
      <br>
      You can select multiple vulnerabilities for your network component; however, if you do not select
      any at all, it will default and select all of them.
    </p>
  </div>
  <button class="btn btn-success mx-2 mb-2" @click="addRow(index)"> 
    <i class="fa fa-plus" aria-hidden="true"></i> Add Server
  </button>
  <table class="table table-bordered" style="width: 80%">
      <tbody>
        <tr v-for="(row, index) in rows" :key="index" :row="row">
            <td style="vertical-align: middle;" width="10%">
              <div style="text-align: center;">
              <button :class="`btn btn-danger ${layer}-remove`" @click="removeRow(index)">
                <i class="fa fa-times" aria-hidden="true"></i> Remove
              </button>
              </div>
            </td>
            <td width="20%">
              <div class="text-center pt-1 pb-2">
                  <h5>Server Type</h5>
                  <select v-model="rows[index][0]">
                    <option v-for="item in serverTypes" :key="item" :value="item">{{item}}</option>
                  </select>
              </div>
            </td>
            <td width="15%">
              <div class="text-center pt-1 pb-2">
                  <h5>Vendor</h5>
                  <select style="width: 50%;" v-model="rows[index][1]" @change="getProducts(index)">
                    <option v-for="item in vendors" :key="item" :value="item">{{item}}</option>
                  </select>
              </div>
            </td>
            <td width="20%">
              <div class="text-center pt-1 pb-2">
                  <h5>Product</h5>
                  <select style="width: 80%" v-model="rows[index][2]" @change="getVulnerabilities(index)">
                    <option v-for="item in serverProduct[index]" :key="item" :value="item" >{{item}}</option>                        
                  </select>
              </div>
            </td>
            <td width="15%">
              <div class="text-center pt-1 pb-2">
                  <h5>Number of Servers</h5>
                  <input style="width: 50%;" type="number" v-model="rows[index][3]" placeholder="None" @click="getRowData" min="1"
                    onkeyup="if(this.value <= 0) this.value = 1;"/>      
              </div>
            </td>
            <td width="20%">
            <div class="text-center">
              <h5>Vulnerabilites</h5>
              <Multiselect
                v-model="rows[index][4]"
                mode="multiple"
                placeholder="Select your Vulnerabilites"
                :options="vulnerability_list[index]"
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
import axios from 'axios';
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
        let cve_list = [];
        for (let j = 0; j < this.rows[i][4].length; j++)  {
          cve_list.push(this.vulnerability_list[i][this.rows[i][4][j]]);
        }

        for (let k = 0; k < this.rows[i][3]; k++) {
          nodes.push({
            layer: this.layer,
            id: k, 
            type:this.rows[i][0],
            vendor: this.rows[i][1],
            product: this.rows[i][2],   
            cve_ids: this.rows[i][4].length > 0 || !this.vulnerability_list[i] ? cve_list : JSON.parse(JSON.stringify(this.vulnerability_list[i]))
          });
        }
      }
      return nodes;
    },

    checkSelection() {
      for (let i = 0; i < this.rows.length; i++) {
        if(!(this.rows[i][0] && this.rows[i][1] && this.rows[i][2] && this.rows[i][3])) return false;
      }   
      return true;
    }
  },
  watch: {
    selectedVendor() { 
      for(let i =0; i< this.rows.length; i++){
      http.get(`product_query/server/${this.rows[i][1]}`)
      .then((r) => {
        if (r.data.error) console.log(r.data.error);
        this.products = r.data.query;
      });
      }
    },
  },

  methods: {
    addRow() {
      this.rows.push([undefined, undefined, undefined, 1, new Array()]);
      if (this.rows.length > 1) document.getElementsByClassName(`${this.layer}-remove`)[0].disabled = false;

    },
    removeRow(index) {
      this.rows.splice(index, 1);
      if (this.rows.length == 1) document.getElementsByClassName(`${this.layer}-remove`)[0].disabled = true;
    },
    getProducts(index) {
      http.get(`/product_query/server/${this.rows[index][1]}`).then((r) => {
        console.log(r);
        if (r.data.error) console.log(r.data.error);
        this.serverProduct[index] = r.data.query;
      });
    },
    getVulnerabilities(index) { // Example of how to get data from CVE-Search !!! 
    this.vulnerability_list[index] = [];
      axios.get(`http://localhost:2000/api/search/${this.rows[index][1].toLowerCase()}/${this.rows[index][2].toLowerCase()}`).then((r) => {
        // console.log(r);
        r.data.results.forEach((e) => {this.vulnerability_list[index].push(e.id)});
      });
    },
  },

  data() {
    return{
      rows: [[undefined, undefined, undefined, 1, new Array()]],
      serverProduct: [],
      vulnerability_list: [],
    };
  },

  mounted() {
    document.getElementsByClassName(`${this.layer}-remove`)[0].disabled = true;
  },
}
</script>

<style>

</style>
