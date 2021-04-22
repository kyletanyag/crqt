<template>
<div>
  <h1>Model-Driven Results</h1>
  <div class="mx-5 row">
    <div class="col-2"></div>
    <div class="col-8">
      <table>
        <tbody>
          <tr v-for="opt in options" :key="opt.title">
            <td class="py-3 text-center" style="width: 20%">
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
                Downloadable JSON file of the simulation results except for attack path specific data. 
                Unfortunately, we are unable to contain that in the JSON file due to the massive number
                of possible attack paths.
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
import { ModelDrivenResultOptions } from '@/utilities/result-constants.js';
export default {
  name: 'Model Driven Results',

  data() {
    return {
      options: ModelDrivenResultOptions,
      error: undefined,
      rawData: {
        nodes: [],
        edges: [],
        vhp: undefined,
        centrality: undefined,
        topsis: undefined,
      }
    }
  },

  methods: {
    DownloadRawData() {
      http.get('/model_driven/get_network_title').then((r) => {
        this.rawData.network_title = r.data.network_title;
      }).catch((e) => {
        this.error = e;
      }).then(() => {
        http.get('/model_driven/get_input_date').then((r) => {
          this.rawData.input_date = r.data.input_date;
        }).catch((e) => {
          this.error = e;
        }).then(() => {
          http.get('/model_driven/get_network_topology').then((r) => {
            this.rawData.nodes = r.data.nodes;
            this.rawData.edges = r.data.edges;
          }).catch((e) => {
            this.error = e;
          }).then(() => {
            http.get('/model_driven/vulnerable_host_percentage').then((r) => {
              this.rawData.vhp = r.data;
            }).catch((e) => {
              this.error = e;
            }).then(() => {
              http.get('/model_driven/centrality').then((r) => {
                this.rawData.centrality = r.data;
              }).catch((e) => {
                this.error = e;
              }).then(() => {
                http.get('/model_driven/topsis').then((r) => {
                  this.rawData.topsis = r.data.topsis;
                }).catch((e) => {
                  this.error = e;
                }).then(() => {
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
  
</style>