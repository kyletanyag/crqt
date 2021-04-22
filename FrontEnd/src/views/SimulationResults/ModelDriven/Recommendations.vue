<template>
<div class="mb-5">
  <result-header 
    title="Recommendations"
    prevPage="Model Driven Results - Severity Display"
    nextPage="Model Driven Results - Printout"
    defaultPage="Model Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="mx-5 row">
    <div class="col-6">
      <div class="text-left">
        <h2 class="text-center">TOPSIS Recommendations</h2>
        <p>
          The recommendations computed were based on the Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) method.
          The TOPSIS method assesses device criticality by building on the concept
          that the chosen alternative should have the shortest geometric distance from the positive 
          ideal solution and the largest geometric distance from the negative ideal solution.
        </p>
        <p>
          Applying the TOPSIS method, we get the following rankings for 
          nodes that need to be reviewed.
        </p>
        <div>
          How many recommendations would you like to see? 
          <input type="number" v-model.number="numRecommend" max="10" min="1" maxlength="2"> 
        </div>
        <div>
          Our top <strong>{{ Math.min(numRecommend, topsisResults.length) }}</strong> recommendations: 
          <ol v-if="!loading">
            <li v-for="(node, index) in topsisResults.slice(0, numRecommend)" :key="index" class="pb-2">
              Resolve node ID <strong>{{ node.id }}</strong> ( <strong>{{node.vendor}} {{node.product}}</strong> ),
              at the <strong>{{node.layer}}</strong> layer.
              <br>
              You can increase your cyber resiliency by patching/fixing any of the vulnerablities found 
              <a :href="`https://cve.circl.lu/search/${node.vendor}/${node.product}`" target="_blank">here</a>.
            </li>
          </ol>
        </div>
      </div>
    </div>
    <div class="col-6">
      <h2>TOPSIS Node Ranking</h2>
      <div :style="`overflow-y: auto; height: 800px;`">
        <table v-if="topsisResults" class="table table-hover">
          <thead>
            <tr>
              <th @click="sort('id')" scope="col" style="width: 10%">ID<i :class="sortDirection('id')"></i></th>
              <th @click="sort('layer')" scope="col" style="width: 15%">Layer<i :class="sortDirection('layer')"></i></th>
              <th @click="sort('vendor')" scope="col" style="width: 15%">Product<i :class="sortDirection('product')"></i></th>
              <th @click="sort('product')" scope="col" style="width: 15%">Vendor<i :class="sortDirection('vendor')"></i></th>
              <th @click="sort('topsis_score')" scope="col" style="width: 20%">TOPSIS Score<i :class="sortDirection('topsis_score')"></i></th>
              <th @click="sort('ranking')" scope="col" style="width: 15%">Ranking<i :class="sortDirection('ranking')"></i></th>
            </tr>
          </thead> 
          <tbody>
            <tr v-for="result in sortedTopsisResults" :key="result.id"              
              @mouseover="highlight(edge.id)"
              @mouseleave="unhighlight(edge.id)"
            >
              <td style="width: 10%; word-wrap: anywhere;">{{ result.id }}</td>
              <td style="width: 15%; word-wrap: anywhere;">{{ result.layer }}</td>
              <td style="width: 15%; word-wrap: anywhere;">{{ result.vendor }}</td>
              <td style="width: 15%; word-wrap: anywhere;">{{ result.product }}</td>
              <td style="width: 20%; word-wrap: anywhere;">{{ result.topsis_score }}</td>
              <td style="width: 15%; word-wrap: anywhere;">{{ result.ranking }}</td>
            </tr> 
          </tbody>
        </table>
      </div>     
    </div>
  </div>
</div>
</template>
<script>
import http from '@/http-common.js';
import ResultHeader from '@/components/ResultHeader.vue';

export default {
  name: 'Model Driven Results - Recommendations',

  components: {
    ResultHeader,
  },

  data() {
    return {
      error: undefined,
      nodes: [],
      topsis: [],
      currentSort: 'ranking',
      currentSortDir: 'asc',
      numRecommend: 3,
      topsisResults: []
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      http.get('/model_driven/get_network_topology').then((r) => {
        this.nodes = r.data.nodes;
      }).then(() => {
        http.get('/model_driven/topsis').then((r) => {
            this.topsis = r.data.topsis;
          }).then(() => {
            var arr = Array(this.nodes.length - 1);

            for (let i = 0; i < arr.length; i++) {
              arr[i] = {
                id: this.nodes[i+1].id,
                layer: this.nodes[i+1].layer,
                vendor: this.nodes[i+1].vendor,
                product: this.nodes[i+1].product,
                topsis_score: this.topsis[i].topsis_score
              }
            }

            var temp = arr.slice(0).sort((a,b) => {
              if(a['topsis_score'] < b['topsis_score']) return 1;
              if(a['topsis_score'] > b['topsis_score']) return -1;
            });

            for (let i = 0; i < temp.length; i++) {
              temp[i]['ranking'] = i + 1;
            }

            this.topsisResults = temp;
          }).catch((e) => {
            this.error = e;
          });
      }).catch((e) => {
        this.error = e;
      });

 
    },

    sort(s) {
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir ==='asc' ? 'desc':'asc';
      }
      this.currentSort = s;
    },

    sortDirection(s) {
      if (this.currentSortDir === 'asc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-asc';
      else if (this.currentSortDir === 'desc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-desc';
      else
        return 'fa fa-fw fa-sort';
    },
  },

  computed: {
    sortedTopsisResults() {
      if (!this.topsisResults) return 0;
      return this.topsisResults.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    }
  },

  watch: {
    numRecommend() {
      if (this.numRecommend > 10) this.numRecommend = 10;
      if (this.numRecommend < 0) this.numRecommend = null;
      if (!this.numRecommend === "") this.numRecommend = 1;
    },
  }
}
</script>
<style>
</style>