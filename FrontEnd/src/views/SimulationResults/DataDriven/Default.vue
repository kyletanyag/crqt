<template>
<div>
  <h1>Data-Driven Results</h1>
  <div class="mx-5 row">
    <div class="col-2"></div>
    <div class="col-8">
      <table>
        <tbody>
          <tr v-for="opt in options" :key="opt.title">
            <td class="py-3 text-center" style="width: 22%">
              <button class="btn btn-outline-primary" style="width: 100%;"
                @click="this.$router.push({name: opt.routeName})">
                {{ opt.title }}
              </button>
            </td>
            <td class=" pl-3 text-left">
              <div>
                {{ opt.description }}
              </div>
            </td>
          </tr>
          <tr>
            <td class="py-3 text-center">
              <button class="btn btn-outline-primary" style="width: 100%;"
                @click="DownloadRawData"
               >
                Raw Result Data Download
              </button>
            </td>
            <td class="pl-3 text-left">
              <div>
                Downloadable JSON file of the simulation results.
                <a id="downloadAnchorElem" style="display:none"></a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
</template>
<script>
import http from '@/http-common.js';
import { DataDrivenResultOptions } from '@/utilities/result-constants.js';
export default {
  name: 'Data Driven Results',

  data() {
    return {
      options: DataDrivenResultOptions,
      error: undefined,
      rawData: {
        network_title: '',
        input_date: '',
        network_entropy: {
          base: 0,
          exploitability: 0,
          impact: 0
        },
        nodes: [],
        edges: [],
        conditions_per_derived_node: [],
        rules_per_derived_node: []
      }
    }
  },



  methods: {
    DownloadRawData() {
      http.get('/data_driven/get_network_title').then((r) => {
        this.rawData.network_title = r.data.network_title;
      }).catch((e) => {
        this.error = e;
      }).then(() =>{
        http.get('/data_driven/get_input_date').then((r) => {
          this.rawData.input_date = r.data.input_date;
        }).catch((e) => {
          this.error = e;
        }).then(() =>{
          http.get('/data_driven/network_entropy').then((r) => {
            this.rawData.network_entropy.base = r.data.network_entropy[0].base,
            this.rawData.network_entropy.exploitability = r.data.network_entropy[1].exploitability,
            this.rawData.network_entropy.impact = r.data.network_entropy[2].impact
          }).catch((e) => {
            this.error = e;
          }).then(() =>{
            http.get('data_driven/get_derived_scores').then((r) => {
              this.rawData.nodes = r.data.nodes;
              this.rawData.edges = r.data.edges;
            }).catch((e) => {
              this.error = e;
            }).then(() =>{
              http.get('/data_driven/conditions_per_derived_node').then((r) => {
                this.rawData.conditions_per_derived_node = r.data.conditions_per_derived_node;
              }).catch((e) => {
                this.error = e;
              }).then(() =>{
                http.get('/data_driven/rules_per_derived_node').then((r) => {
                  this.rawData.rules_per_derived_node = r.data.rules_per_derived_node;
                }).catch((e) => {
                  this.error = e;
                }).then(() =>{
                  var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.rawData, undefined, 2));
                  var dlAnchorElem = document.getElementById('downloadAnchorElem');
                  dlAnchorElem.setAttribute("href", dataStr);
                  dlAnchorElem.setAttribute("download", `${this.rawData.network_title.toLowerCase()}_results.json`);
                  dlAnchorElem.click();                    
                });                  
              });               
            });              
          });
        });
      });
    }
  },
}
</script>
<style>
/* table, th, td {
  border-collapse: collapse;
  margin-left: 7px;
} */
</style>