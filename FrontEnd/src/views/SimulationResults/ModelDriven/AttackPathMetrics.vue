<template>
<div class="mb-5">
  <result-header 
    title="Attack Path Metrics"
    nextPage="Model Driven Results - Severity Display"
    prevPage="Model Driven Results - Graph Metrics"
    defaultPage="Model Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="row mx-5 text-left">
    <div>
      <h2>Instructions</h2>
      <p>
        Below contains a graph representation of your network following the NIST's control
        system security recommended architecture. Alongside is an interface that asks you to 
        input a target node that are you are interesting in viewing metrics on. 
        <br>
        Based on your chosen node, you will be provided general attack path information,
        a data table containing all the possible attack paths to that target node, histograms
        containing the computed base, exploitability, and impact scores of all the paths, and
        finally the top exploitable and top impactful attack paths to that target node.
        <br><br>
        On the network graph, you can hover over a node to get specific information about that node or 
        you can hover an edge to get the scores associated to getting to that node. Futhermore, you
        can hover over a row in the any of the data tables and the corresponding path in the network graph will
        be highlighted. You can also click on any of the rows to keep the path highlighted.
      </p>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <network-graph></network-graph>
    </div>
    <div class="col">
      <div class="row-12 my-2">
        <h2>Attack Path Data</h2>
        <div class="text-left">
          <div class="row-12 py-2 align-center">
            <div class="col-12">
              Which node are you interested in analyzing? ID:&nbsp;&nbsp;
              <input type="number" v-model.number="desiredNodeID" :max="lastNodeID" min="1" maxlength="2"  style="width: 75px" 
              @change="NotifyChange"
              @keydown="NotifyChange">
              <button class="ml-2 btn btn-primary btn-sm pause" id="id_submit" @click="GetAttackPaths(desiredNodeID)">Submit</button>
              <span v-if="loading" class="pl-1"><strong>Loading ...</strong></span>
            </div>
            <div class="row pl-3 my-2">
              <div class="col-6 text-left">
                Computation Time: <strong v-if="!loading && desiredNodeID > 0 && desiredNodeID <= lastNodeID">{{ compTime }} s</strong>
                <br>
                Number of Attack Paths: <strong v-if="!loading && desiredNodeID > 0 && desiredNodeID <= lastNodeID">{{ numPaths }}</strong>
                <br>
                Average Base Score Cost: <strong v-if="!loading && desiredNodeID > 0 && desiredNodeID <= lastNodeID">{{ avgBasScore }}</strong>
                <br>
                Average Exploitability Score Cost: <strong v-if="!loading && desiredNodeID > 0 && desiredNodeID <= lastNodeID">{{ avgExpScore }}</strong>
                <br>
                Average Impact Score Cost: <strong v-if="!loading && desiredNodeID > 0 && desiredNodeID <= lastNodeID">{{ avgImpScore }}</strong>
              </div>
              <div class="col-6">
                <tr>
                  <td class="px-2 py-1">
                    <button :class="toggleBtnState(pathShow)" style="width: 100%" @click="pathShow = !pathShow">Show Path Data</button>
                  </td>
                  <td class="px-2 py-1">
                    <button :class="toggleBtnState(histogramShow) + ' pause'" style="width: 100%" @click="histogramShow = !histogramShow; pause()">Show Histograms</button>
                  </td>
                </tr>
                <tr>
                  <td class="px-2 py-1">
                    <button :class="toggleBtnState(expShow)"  style="width: 100%" @click="expShow = !expShow">Show Top Exploitable</button>
                  </td>
                  <td class="px-2 py-1">
                    <button :class="toggleBtnState(impShow)"  style="width: 100%" @click="impShow = !impShow">Show Top Impact</button>
                  </td>
                </tr>
              </div>
            </div>
            <div class="col-12 pt-2 text-center" v-if="pathShow && paths.length && desiredNodeID > 0 && desiredNodeID">
              <h3>Path Data Table</h3>
              <div :style="`overflow-y: auto; height: 500px;`">
                <table class="table table-hover">
                    <thead>
                      <tr>
                        <th @click="sort('path_id')" scope="col" style="width: 15%">Path #<i :class="sortDirection('path_id')"></i></th>
                        <th @click="sort('path')" scope="col" style="width: 20%">Path<i :class="sortDirection('path')"></i></th>
                        <th @click="sort('base_score')" scope="col" style="width: 20%">Base Score<i :class="sortDirection('base_score')"></i></th>
                        <th @click="sort('exploitability_score')" scope="col" style="width: 25%">Exploitability Score<i :class="sortDirection('exploitability_score')"></i></th>
                        <th @click="sort('impact_score')" scope="col" style="width: 20%">Impact Score<i :class="sortDirection('impact_score')"></i></th>
                      </tr>
                    </thead> 
                    <tbody>
                      <tr v-for="p in sortedPaths" 
                        :key="p.path_id"
                      @mouseover="highlightPath(p.path)"
                      @click="toggleHighlightPath(p.path)"
                      @mouseleave="unhighlightPath(p.path)"
                      :class="cssHighlightedRow(p.path)"
                      >
                        <td style="width: 15%">{{ p.path_id }}</td>
                        <td style="width: 20%; word-wrap: anywhere;">{{ p.path }}</td>
                        <td style="width: 20%">{{ p.base_score }}</td>
                        <td style="width: 25%">{{ p.exploitability_score }}</td>
                        <td style="width: 20%">{{ p.impact_score }}</td>
                      </tr> 
                    </tbody>
                </table>
              </div>
            </div>
            <div class="col-12 pt-2 text-center" v-if="expShow && topExpPaths.length && desiredNodeID > 0 && desiredNodeID">
              <h3>Top Exploitable</h3>
              <div :style="`overflow-y: auto; height: 300px;`">
                <table class="table table-hover justify-content-center">
                  <thead>
                    <tr>
                      <th scope="col" style="width: 20%">Path #</th>
                      <th scope="col" style="width: 40%">Path</th>
                      <th scope="col" style="width: 20%">Score</th>
                      <th scope="col" style="width: 20%">Ranking</th>
                    </tr>
                  </thead> 
                  <tbody>
                    <tr v-for="(p, idx) in topExpPaths" :key="p.path"              
                      @mouseover="highlightPath(p.nodes)"
                      @click="toggleHighlightPath(p.nodes)"
                      @mouseleave="unhighlightPath(p.nodes)"
                      :class="cssHighlightedRow(p.nodes)"
                    >
                      <td style="width: 20%">{{ p.path }}</td>
                      <td style="width: 40%">{{ p.nodes }}</td>
                      <td style="width: 20%">{{p.exploitability }}</td>
                      <td style="width: 20%">{{ idx + 1 }}</td>
                    </tr> 
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-12 pt-2 text-center" v-if="impShow && topImpPaths.length && desiredNodeID > 0 && desiredNodeID">
              <h3>Top Impact</h3>
              <div :style="`overflow-y: auto; height: 300px;`">
                <table class="table table-hover justify-content-center">
                  <thead>
                    <tr>
                      <th scope="col" style="width: 20%">Path #</th>
                      <th scope="col" style="width: 40%">Path</th>
                      <th scope="col" style="width: 20%">Score</th>
                      <th scope="col" style="width: 20%">Ranking</th>
                    </tr>
                  </thead> 
                  <tbody>
                    <tr v-for="(p, idx) in topImpPaths" :key="p.path"              
                      @mouseover="highlightPath(p.nodes)"
                      @click="toggleHighlightPath(p.nodes)"
                      @mouseleave="unhighlightPath(p.nodes)"
                      :class="cssHighlightedRow(p.nodes)"
                    >
                      <td style="width: 20%">{{ p.path }}</td>
                      <td style="width: 60%">{{ p.nodes }}</td>
                      <td style="width: 20%">{{p.impact }}</td>
                      <td style="width: 20%">{{ idx + 1 }}</td>
                    </tr> 
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-12 pt-2 text-center" v-if="histogramShow && topImpPaths.length && desiredNodeID > 0 && desiredNodeID">
              <h3>Histograms</h3>
              <div class="row">
                <Histogram
                  :data="baseScores"
                  :numBins="10"
                  :range="[0, 10]"
                  yAxis="Frequency"
                  xAxis="Base Score"
                  name="Base Scores"
                  barColor='#f87979'
                  class="col-6" 
                />
                <Histogram
                  :data="exploitabilityScores"
                  :numBins="10"
                  :range="[0, 10]"
                  yAxis="Frequency"
                  xAxis="Exploitability Score"
                  name="Exploitability Scores"
                  barColor='#78BCFF'
                  class="col-6"
                />
                <Histogram
                  :data="impactScores"
                  :numBins="10"
                  :range="[0, 10]"
                  yAxis="Frequency"
                  xAxis="Impact Score"
                  name="Impact Scores"
                  barColor='#81DFA9'
                  class="col-6"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
import ResultHeader from '@/components/ResultHeader.vue';
import NetworkGraph from '@/components/ModelDrivenNetworkGraph.vue';
import Histogram from '@/components/Histogram.vue';
export default {
  name: 'Model Driven Results - Node Specific Metrics',

  components: {
    ResultHeader,
    NetworkGraph,
    Histogram,
  },

  data() {
    return {
      error: undefined,
      currentSort: 'id',
      currentSortDir: 'asc',
      desiredNodeID: 0,
      lastNodeID: 0,
      loading: false,
      numPaths: 0,
      avgBasScore: 0,
      avgExpScore: 0,
      avgImpScore: 0,
      compTime: 0,
      paths: [],
      selected: null,
      toggled: false,
      topExpPaths: [],
      topImpPaths: [],
      pathShow: false,
      expShow: false,
      impShow: false,
      histogramShow: false
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      http.get('/model_driven/get_network_topology').then((r) => {        
        this.lastNodeID = Math.max.apply(Math, r.data.nodes.map(function(o) { return o.id; }));
      });
    },

    highlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '20');
      document.getElementById(`node_${id}`).setAttribute('stroke', 'black');
    },

    unhighlight(id) {
      document.getElementById(`node_${id}`).setAttribute('r', '15');
      document.getElementById(`node_${id}`).setAttribute('stroke', 'white');
    },

    highlightEdge(id1, id2) {
      document.getElementById(`edge_${id1}_${id2}`).setAttribute('stroke', 'black');
      document.getElementById(`edge_${id1}_${id2}`).setAttribute('stroke-width', '1.5');
      document.getElementById(`arrowtip_${id1}_${id2}`).setAttribute('fill', 'black');
    },

    unhighlightEdge(id1, id2) {
      document.getElementById(`edge_${id1}_${id2}`).setAttribute('stroke', 'grey');
      document.getElementById(`edge_${id1}_${id2}`).setAttribute('stroke-width', '1');
      document.getElementById(`arrowtip_${id1}_${id2}`).setAttribute('fill', 'grey');
    },

    highlightPath(a) {
      if (!this.selected) {
        a.forEach((x) => {this.highlight(x)});
        this.highlight(0);
        this.highlightEdge(0, a[0]);
        for (let i = 0; i < a.length - 1; i++) {
          this.highlightEdge(a[i], a[i+1]);
        }
      }
    },

    unhighlightPath(a) {
      if (!this.toggled) {
        a.forEach((x) => {this.unhighlight(x)});
        this.unhighlight(0);
        this.unhighlightEdge(0, a[0]);

        for (let i = 0; i < a.length - 1; i++) {
          this.unhighlightEdge(a[i], a[i+1]);
        }
      }
    },

    toggleHighlightPath(a) {
      if (!this.selected) {
        this.highlightPath(a);
        this.selected = a;
        this.toggled = true;
      } else if (this.selected === a) {
        this.unhighlightPath(a);
        this.selected = null;
        this.toggled = false;
      } else {
        this.toggled = false;
        this.unhighlightPath(this.selected);
        this.selected = null;
        this.highlightPath(a);
        this.toggled = true;
        this.selected = a;
      }
    },

    cssHighlightedRow(x) {
      return x === this.selected ? 'table-primary' : '';
    },

    NotifyChange() {
      document.getElementById('id_submit').className = "ml-2 btn btn-primary btn-sm";
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

    GetAttackPaths(ap) {
      this.loading = true;
      http.get(`/model_driven/attack_paths/${ap}`).then((r) => {
        // console.log(r);

        this.numPaths = r.data.number_attack_paths;
        this.avgBasScore = r.data.averge_length_attack_paths[0];
        this.avgExpScore= r.data.averge_length_attack_paths[1];
        this.avgImpScore = r.data.averge_length_attack_paths[2];
        this.compTime = Number(r.data.computation_time.toPrecision(3));
        this.paths = r.data.metrics_per_path;
        this.paths.forEach((p) => {p.path.reverse()});
        this.topExpPaths = r.data.top_exploitable.slice(0).sort((a,b) => { return a.exploitability < b.exploitability ? 1 : -1; });
        this.topExpPaths.forEach((p) => {p.nodes.reverse()});
        this.topImpPaths = r.data.top_impactful.slice(0).sort((a,b) => {return a.impact < b.impact ? 1 : -1; });
        this.topImpPaths.forEach((p) => {p.nodes.reverse()});
        this.loading = false;
      }).catch((e) => {
        this.error = e;
      });
      document.getElementById('id_submit').className = "ml-2 btn btn-secondary btn-sm";
    },

    toggleBtnState(x) {
      return x ? 'btn btn-secondary' : 'btn btn-primary'
    },

    pause() {
      if (this.histogramShow) {
        const btns = document.getElementsByClassName('pause');
          btns.forEach((b) => {
            b.disabled = true;
          });
        setTimeout(() => {
            btns.forEach((b) => {
              b.disabled = false;
            });
          }, 1500)
      }
    }
  },

  computed: {
    sortedPaths() {
      if (!this.paths) return 0;
      return this.paths.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    },

    baseScores() {
      return this.paths.map(x => x.base_score);
    },  

    exploitabilityScores() {
      return this.paths.map(x => x.exploitability_score);
    },

    impactScores() {
      return this.paths.map(x => x.impact_score);
    },
  },

  watch: {
    desiredNodeID() {
      if (this.desiredNodeID > this.lastNodeID) this.desiredNodeID = this.lastNodeID;
      if (this.desiredNodeID < 1) this.desiredNodeID = null;
    }
  }
}
</script>
<style>
</style>