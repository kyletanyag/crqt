<template>
<div>
  <h1>Model Driven Results</h1>
  <div class="mx-5 row">
    <div class="container">
      <table>
        <tbody>
          <tr v-for="opt in options" :key="opt.title">
            <td class="py-3 text-center">
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
            <td class=" pl-3 text-left">
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
import { ModelDrivenResultOptions } from '@/utilities/result-constants.js';
export default {
  name: 'Data Driven Results',

  data() {
    return {
      options: ModelDrivenResultOptions,
      error: undefined,
      rawData: {
        nodes: [],
        edges: [],
      }
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      http.get('/model_driven/get_network_topology').then((r) => {
        this.rawData.nodes = r.data.nodes;
        this.rawData.edges = r.data.edges;
        
      }).catch((e) => {
        this.error = e;
      });
    },

    DownloadRawData() {
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.rawData, undefined, 2));
      var dlAnchorElem = document.getElementById('downloadAnchorElem');
      dlAnchorElem.setAttribute("href", dataStr);
      dlAnchorElem.setAttribute("download", `${this.rawData.network_title.toLowerCase()}_results.json`);
      dlAnchorElem.click();
    }
  },
}
</script>
<style>
  
</style>