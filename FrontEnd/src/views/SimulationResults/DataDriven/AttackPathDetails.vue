<template>
<div>
  <result-header 
    title="Attack Path Details"
    nextPage="Data Driven Results - Recommendations"
    prevPage="Data Driven Results - Derived Node Exploitation"
    defaultPage="Data Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="mx-5 row">
    <div class="col">
      <div class="text-left">
        <p>
          Average number of conditions to reach a derived fact node: <strong>{{ avgNumConditions }}</strong>.
          <br>
          Average number of rules to reach a derived fact node: <strong>{{ avgNumRules }}</strong>.
        </p>
      </div>
      <div class="">
        <table v-if="data" class="table table-hover">
          <thead style="display: block;">
            <tr>
              <th @click="sort('id')" scope="col" style="width: 15%">ID<i :class="sortDirection('id')"></i></th>
              <th @click="sort('description')" scope="col" style="width: 35%; text-align: right;">Description<i :class="sortDirection('description')"></i></th>
              <th @click="sort('numConds')" scope="col" style="width: 30%; text-align: right;"># Conditions<i :class="sortDirection('numConds')"></i></th>
              <th @click="sort('numRules')" scope="col" style="width: 15%"># Rules<i :class="sortDirection('numRules')"></i></th>
            </tr>
          </thead>
          <div style="overflow-y: auto; height: 600px;">
            <tbody>
              <tr v-for="(node, index) in sortedData" :key="index">
                <td style="width: 15%">{{ node.id }}</td>
                <td style="width: 35%">{{ node.description }}</td>
                <td style="width: 20%">{{ node.num_conditions }}</td>
                <td style="width: 20%">{{ node.num_rules }}</td>
              </tr>
            </tbody>
          </div>
        </table>
      </div>
    </div>  
    <div class="col" v-if="!loading">
      <div class="btn-group btn-group-toggle pb-2" id="histogram">
        <label class="btn btn-secondary" :class="{active: histogramType === 'All'}">
          <input type="radio" v-model="histogramType" value="All" autocomplete="off"> All
        </label>
        <label class="btn btn-secondary" :class="{active: histogramType === 'Exec Code'}">
          <input type="radio" v-model="histogramType" value="Exec Code"  autocomplete="off"> Exec Code
        </label>
      </div>
      <Histogram 
        :data="histogramCondData"
        :numBins="5"
        :name="histogramCondName"
        barColor='#f87979'
        style="width: 60%"
        class="container"
      />
      <Histogram 
        :data="histogramRuleData"
        :numBins="5"
        :name="histogramRuleName"
        barColor='#f87979'
        style="width: 60%"
        class="container"
      />
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
import ResultHeader from '@/components/ResultHeader.vue';
import Histogram from '@/components/Histogram.vue';

export default {
  name: 'Data Driven Results - Attack Path Details',

  components: {
    ResultHeader,
    Histogram
  },

  data() {
    return {
      error: undefined,
      data: [],
      rules: [],
      avgNumConditions: 0,
      avgNumRules: 0,
      currentSort: 'id',
      currentSortDir: 'asc',
      condVals: [],
      ruleVals: [],
      histogramType: 'All',
      histogramCondData: [],
      histogramRuleData: [],
      loading: true,
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      this.loading = true;
      http.get('/data_driven/conditions_and_rules_per_node').then((r) => {
        this.data = r.data.derived_data;
        
        this.data.forEach((n) => {
          this.condVals.push(n.num_conditions);
        });
        
        this.data.forEach((n) => {
          this.ruleVals.push(n.num_rules);
        });
        
        this.histogramCondData = this.condVals;
        this.histogramRuleData = this.ruleVals;

        this.avgNumConditions = this.condVals.reduce((a, b) => a + b) / this.condVals.length;
        this.avgNumRules = this.ruleVals.reduce((a, b) => a + b) / this.ruleVals.length;
        this.loading = false;
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
    sortedData() {
      if (!this.data) return 0;
      return this.data.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    },

    histogramCondName() {
      if (this.histogramType === 'All') return 'Node Conditions Histogram (All Derived Fact Nodes)';
      else return 'Node Conditions Histogram (Exec Code Nodes)';
    },

    histogramRuleName() {
      if (this.histogramType === 'All') return 'Node Rules Histogram (All Derived Fact Nodes)';
      else return 'Node Rules Histogram (Exec Code Nodes)';
    }
  },

  watch: {
    histogramType(type) {
      const btns = document.getElementById('histogram').getElementsByTagName('input');
      btns.forEach((b) => {
        b.disabled = true;
      });
      setTimeout(() => {
        btns.forEach((b) => {
          b.disabled = false;
        });
      }, 1500)

      if (type === 'All') {
        this.histogramCondData = this.condVals;
        this.histogramRuleData = this.ruleVals;
      } else {
        var tempCond = [];
        var tempRule = [];
          this.data
            .filter((n) => {return n.description.includes('execCode')})
            .forEach((n) => {
              tempCond.push(n.num_conditions);
              tempRule.push(n.num_rules);
            });
        this.histogramCondData = tempCond;
        this.histogramRuleData = tempRule;
      }
    },
  }
}
</script>

<style>
</style>