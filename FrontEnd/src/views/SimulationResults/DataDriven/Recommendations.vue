<template>
<div>
  <result-header 
    title="Recommendations"
    prevPage="Data Driven Results - Specific Node Information"
    defaultPage="Data Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="mx-5 row">
    <div class="col text-left">
      How many recommendations would you like to see? 
      <input type="number" v-model.number="numRecommend" max="10" min="1" maxlength="2"
        onkeyup="if(this.value > 10) this.value = 10; else if(this.value < 0) this.value = 0;"
      > 
    </div>
  </div>
  <div class=" mx-5 mb-2 row">
    <div class="col text-left">
      <div class="pb-4"></div>
      <p>
        To the right is a table containing a sorted list of all the derived fact nodes from your network
        ranked from highest derived score probability to lowest derived score probability.
      </p>
      <div>
        Our top <strong>{{ Math.min(numRecommend, rankedDerivedFactNodes.length) }}</strong> recommendations: 
        <ol v-if="!loading">
          <li v-for="(node, index) in rankedDerivedFactNodes.slice(0, numRecommend)" :key="index">
            Resolve node <strong>{{ node.id }}</strong>, <strong>{{node.description}}</strong>.
          </li>
        </ol>
      </div>
    </div>
    <div class="col">
      <network-data-table :data="rankedDerivedFactNodes" title="Derived Fact Nodes Data Table" />
    </div>
  </div>
  <hr>
  <div class="mx-5 mb-2 row">
    <div class="col text-left">
      <div class="pb-4"></div>
      <p>
        To the right is a table containing a sorted list of all the listed vulnerabilities from your network
        ranked from highest derived score probability to lowest derived score probability.
      </p>
      <div>
        Our top <strong>{{ Math.min(numRecommend, rankedVulExistsNodes.length) }}</strong> recommendations: 
        <ol v-if="!loading">
          <li v-for="(node, index) in rankedVulExistsNodes.slice(0,numRecommend)" :key="index">
            Close vulnerabilty <strong>{{ getCVEID(node.description)}}</strong>
            at the host: <strong>{{getHost(node.description)}}</strong>
            found at node <strong>{{node.id}}</strong>. 
            <br>The severity level of this node is marked as <strong>{{getSeverityLevel(node.base_score)}}</strong>.
          </li>
        </ol>
      </div>
    </div>
    <div class="col">
      <network-data-table :data="rankedVulExistsNodes" title="Vulnerability Nodes Data Table" />
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
import ResultHeader from '@/components/ResultHeader.vue';
import NetworkDataTable from '@/components/NetworkDataTable.vue';
export default {
  name: 'Data Driven Results - Recommendations',

  components: {
    ResultHeader,
    NetworkDataTable
  },

  data() {
    return {
      error: undefined,
      numRecommend: 3,
      derivedFactNodes: [],
      vulExistsNodes: [],
      loading: true,
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      this.loading = true;
      http.get('data_driven/get_derived_scores').then((r) => {
        this.derivedFactNodes = r.data.nodes.filter((n) => { return n.node_type === 'Derived Fact' });
        this.vulExistsNodes = r.data.nodes.filter((n) => { return n.description.includes('vulExists') });
        this.loading = false;
      }).catch((e) => {
        this.error = e;
      });
    },

    getCVEID(str) {
      var values = str.split("'");
      return values[1];
    },

    getHost(str) {
      return str.substring(str.lastIndexOf("(") + 1, str.indexOf(","));
    },

    getSeverityLevel(score) {
      if (score >= 0.7) return 'High';
      if (score >= 0.4) return 'Medium';
      return 'Low';
    },
  },

  watch: {
    numRecommend() {
      if (this.numRecommend > 10) this.numRecommend = 10;
      if (this.numRecommend < 0) this.numRecommend = null;
      if (!this.numRecommend === "") this.numRecommend = 1;
    },

    desiredNodeID() {
      if (this.desiredNodeID > this.lastNodeID) this.desiredNodeID = this.lastNodeID;
      if (this.desiredNodeID < 1) this.desiredNodeID = null;
    }
  },

  computed: {
    rankedDerivedFactNodes() {
      var temp = this.derivedFactNodes.slice(0).sort((a,b) => {
        if(a['base_score'] < b['base_score']) return 1;
        if(a['base_score'] > b['base_score']) return -1;
      });

      for (let i = 0; i < temp.length; i++) {
        temp[i]['ranking'] = i + 1
      }
      return temp;
    },

    rankedVulExistsNodes() {
      var temp = this.vulExistsNodes.slice(0).sort((a,b) => {
        if(a['base_score'] < b['base_score']) return 1;
        if(a['base_score'] > b['base_score']) return -1;
      });

      for (let i = 0; i < temp.length; i++) {
        temp[i]['ranking'] = i + 1
      }
      return temp;
    }
  }
}
</script>
<style>
</style>