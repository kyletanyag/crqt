<template>
<div>
  <div class="noprint">
    <result-header 
      title="Printout"
      prevPage="Model Driven Results - Recommendations"
      defaultPage="Model Driven Results"
    />
    <button class="btn btn-secondary btn-lg" @click="PrintResults">
      Print
    </button>
    <p class="pt-2">Note: Printout does not include attack path metrics as that is interactive in nature.</p>
  </div>
  <div v-if="error" class="alert alert-danger noprint">
    {{ error }}
  </div>
  <hr class="noprint">
  <h1>Model-Driven Results Printout</h1>
  <h1>Summary</h1>
  <div class="mx-5 text-left row">
    <div class="col">
      <div class="pb-2" v-if="!loading">
        <h2>Network Metadata</h2>
        <p>
          You have entered your network topology titled: <strong>{{ title }}</strong> on <strong>{{ inputDate }}</strong>. 
          It took <strong>{{ compTime }}</strong> second(s) to compute the generated metrics. 
        </p>
        <p>
          The computed metrics use NVD Vulnerability data updated as recent as <strong v-if="!loadingNVD">{{ NVDDate }}</strong>.
        </p>
        <h2>Network Breakdown</h2>
        <p>
          Your inputted network contains a total of <strong>{{ network.nodes.length }}</strong> nodes and <strong>{{ network.links.length }}</strong> edges.
        </p>
        <div>
          The number of nodes per layer are:
          <tr>
            <td style="width: 210px;"><strong>Corporate Firewall 1:</strong></td>
            <td><strong>{{ corpFW1.length }}</strong> nodes</td>
          </tr>
          <tr>
            <td style="width: 210px"><strong>Corporate DMZ:</strong></td>
            <td><strong>{{ corpDMZ.length }}</strong> nodes</td>
          </tr>
          <tr>
            <td style="width: 210px"><strong>Corporate Firewall 2:</strong> </td>
            <td><strong>{{ corpFW2.length }}</strong> nodes</td>
          </tr>
          <tr>
            <td style="width: 210px"><strong>Corporate LAN:</strong> </td>
            <td><strong>{{ corpLAN.length }}</strong> nodes</td>
          </tr>
          <tr>
            <td style="width: 210px"><strong>Control Sytem Firewall 1:</strong> </td>
            <td><strong>{{ csFW1.length }}</strong> nodes</td>
          </tr>
          <tr>
            <td style="width: 210px"><strong>Control Sytem DMZ:</strong></td>
            <td><strong>{{ csDMZ.length }}</strong> nodes</td>
          </tr>
          <tr>
            <td style="width: 210px"><strong>Control Sytem Firewall 2:</strong> </td>
            <td><strong>{{ csFW2.length }}</strong> nodes</td>
          </tr>
          <tr>
            <td style="width: 210px"><strong>Control Sytem LAN:</strong> </td>
            <td><strong>{{ csLAN.length }}</strong> nodes</td>
          </tr>
        </div>
      </div>
      <div class="pt-2">
        <h2>Vulnerability Host Percentage</h2>
        <p>
          Vulnerability host percentage (VHP) is a metric that represents the overall security
          level of a network. The number of vulnerable hosts can be obtained by periodically 
          scanning a network via vulnerability scanning tools such as Nessus.
        </p>
        <p>
          <strong>{{ numVulnHosts }}</strong> of <strong>{{ numHosts }}</strong> hosts are denoted as vulnerable hosts.
          <br>Therefore, your network's VHP = <strong>{{ vulnHostPerc }}%</strong>.
        </p>
      </div>
    </div>
    <div class="col">
      <doughnut-chart v-if="!loading"
        name="Network Topology Layer Breakdown"
        :data="[
          corpFW1.length, corpDMZ.length, corpFW2.length, corpLAN.length,
          csFW1.length, csDMZ.length, csFW2.length, csLAN.length
        ]"
        :labels="[
          'Corporate Firewall 1', 'Corporate DMZ', 'Corporate Firewall 2', 'Corporate LAN',
          'Control Sytem Firewall 1', 'Control Sytem DMZ', 'Control Sytem Firewall 2', 'Control Sytem LAN'
        ]"
        style="width: 70%;"
        class="container"        
      />
    </div>
  </div>
  <hr>
  <h1>Network Visualization</h1>
  <div class="mx-5 text-center row">
    <network-graph></network-graph>
    <div class="row-12 my-2">
      <h2>Network Edge Data</h2>
      <div>
        <table v-if="network" class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 7.5%">ID</th>
              <th scope="col" style="width: 15%">Layer</th>
              <th scope="col" style="width: 16.6%">Product</th>
              <th scope="col" style="width: 16.6%">Vendor</th>
              <th scope="col" style="width: 16.6%">Base Score</th>
              <th scope="col" style="width: 16.6%">Exploitability Score</th>
              <th scope="col" style="width: 16.6%">Impact Score</th>
            </tr>
          </thead> 
          <tbody>
            <tr v-for="edge in edges" :key="edge.id"              
              @mouseover="highlight(edge.id)"
              @mouseleave="unhighlight(edge.id)"
            >
              <td style="width: 5%; word-wrap: anywhere;">{{ edge.id }}</td>
              <td style="width: 15%; word-wrap: anywhere;">{{ edge.layer }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.vendor }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.product }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.base_score }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.exploitability_score }}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.impact_score }}</td>
            </tr> 
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <hr>
  <h1>Graph Metrics</h1>
  <div class="mx-5 row">
    <div class="col text-left">
      <h2>Centrality Meaures</h2>
      <div class="mx-1 row">
        <div>
          <p>
            Below are histograms containing the node values for different centrality metrics such as:
          </p>
          <ul>
            <li class="pb-1">
              <strong>Out-Degree Centrality:</strong> The number of outgoing edges for each node.
            </li>
            <li class="pb-1">
              <strong>In-Degree Centrality:</strong> The number of incoming edges for each node. 
            </li>
            <li class="pb-1">
              <strong>Degree Centrality:</strong> The total number of incoming and outgoing edges for each node.
            </li>
            <li class="pb-1">
              <strong>Closeness Centrality:</strong> The average length of the shortest path between the node and all other nodes in the graph.
            </li>
            <li class="pb-1">
              <strong>Betweenness Centrality:</strong> Quantifies the number of times a node acts as a bridge along the shortest path between two other nodes.
            </li>
            <li class="pb-1">
              <strong>PageRank Centrality:</strong> Ranks nodes based on the number and quality of links to a node to give rough estimate of node importance.
            </li>
            <li class="pb-1">
              <strong>Katz Centrality (KC):</strong>  Measures the number of all nodes that can be connected through a path, while contributions of distant nodes are penalized.
            </li>
          </ul>
          <p>
            The purpose of these metrics are to provide a visualization for possible trends that may occurs within network graph.
          </p>
        </div>
      </div>
      <div class="row py-2" v-if="degree.length && closeness.length && betweeness.length && pagerank.length && katz.length && outdegree.length">
        <Histogram
          :data="degree"
          :numBins="10"
          :range="[Math.min(...degree), Math.max(...degree)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Degree Centrality"
          barColor='#78BCFF'
          class="col"
        />
        <Histogram
          :data="closeness"
          :numBins="10"
          :range="[Math.min(...degree), Math.max(...degree)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Closeness Centrality"
          barColor='#81DFA9'
          class="col"
        />
        <Histogram
          :data="betweeness"
          :numBins="10"
          :range="[Math.min(...betweeness), Math.max(...betweeness)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Betweeness Centrality"
          barColor='#f87979'
          class="col"
        />
        <Histogram
          :data="pagerank"
          :numBins="10"
          :range="[Math.min(...pagerank), Math.max(...pagerank)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Pagerank Centrality"
          barColor='#78BCFF'
          class="col"
        />
      </div>
      <div class="row py-2" v-if="katz.length && outdegree.length">
        <Histogram
          :data="katz"
          :numBins="10"
          :range="[Math.min(...katz), Math.max(...katz)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Katz Centrality"
          barColor='#81DFA9'
          class="col"
        />
        <Histogram
          :data="outdegree"
          :numBins="10"
          :range="[Math.min(...outdegree), Math.max(...outdegree)]"
          yAxis="Frequency"
          xAxis="Value"
          name="Outdegree Centrality"
          barColor='#f87979'
          class="col"
        />
        <div class="col"></div>
        <div class="col"></div>
      </div>
      <h2>Degree Distributions</h2>
      <div class="mx-1 row">
        <div>
          <p>
            Below are histograms containing the node values of the degree centrality metrics but converted into probabilities:
          </p>
          <ul>
            <li class="pb-1">
              <strong>Out-Degree Centrality:</strong> The number of outgoing edges for each node.
            </li>
            <li class="pb-1">
              <strong>In-Degree Centrality:</strong> The number of incoming edges for each node. 
            </li>
            <li class="pb-1">
              <strong>Degree Centrality:</strong> The total number of incoming and outgoing edges for each node.
            </li>
          </ul>
          <p>
            The purpose of these metrics are to provide a visualization for possible trends that may occurs within network graph 
            when it comes to degree centrality probability distributions.
          </p>
        </div>
      </div>
      <div class="row py-2" v-if="indegree.length && outdegree.length && degree.length">
        <Histogram
          :data="indegreeProb"
          :numBins="10"
          yAxis="Frequency"
          xAxis="Probability"
          name="In Degree"
          barColor='#78BCFF'
          class="col"
        />
        <Histogram
          :data="outdegreeProb"
          :numBins="10"
          yAxis="Frequency"
          xAxis="Probability"
          name="Out Degree"
          barColor='#81DFA9'
          class="col"
        />
        <Histogram
          :data="degreeProb"
          :numBins="10"
          yAxis="Frequency"
          xAxis="Probability"
          name="Degree"
          barColor='#C29AD3'
          class="col"
        />
        <div class="col"></div>
      </div>
    </div>
  </div>
  <hr>
  <h1>Severity Display</h1>
  <div class="mx-5 row">
   <div class="col-12 text-left">
      <div>
        <h2>Edge Severity Score Breakdown</h2>
        <p>
          To the right contains a data table containing all the base, exploitability, and impact scores
          for every edge/connection in your network. Additionally, the severity level is denoted as well beside
          each score.
        </p>
        <p>
          Your inputted network contains a total of <strong>{{ edges.length }}</strong> edges. 
          The severity breakdown of each edge weight from the computed vulnerability graph is below.
        </p>
        <div class="py-2">
          <h5>For Base Scores:</h5>
          <strong>{{ highBase.length }}</strong> edges are marked as <strong>high</strong> severity. (Base Score &#8805; 0.7)
          <br><strong>{{ mediumBase.length }}</strong> edges are marked as <strong>medium</strong> severity. (0.4 &#8804; Base Score &lt; 0.7)
          <br><strong>{{ lowBase.length }}</strong> edges are marked as <strong>low</strong> severity. (Base Score &lt; 0.4)
        </div>
        <div class="py-2">
          <h5>For Exploitability Scores:</h5>
          <strong>{{ highExploitability.length }}</strong> edges are marked as <strong>high</strong> severity. (Exploitability Score &#8805; 0.7)
          <br><strong>{{ mediumExploitability.length }}</strong> edges are marked as <strong>medium</strong> severity. (0.4 &#8804; Exploitability Score &lt; 0.7)
          <br><strong>{{ lowExploitability.length }}</strong> edges are marked as <strong>low</strong> severity. (Exploitability Score &lt; 0.4)          
        </div>
        <div class="py-2">
          <h5>For Impact Scores:</h5>
          <strong>{{ highImpact.length }}</strong> edges are marked as <strong>high</strong> severity. (Impact Score &#8805; 0.7)
          <br><strong>{{ mediumImpact.length }}</strong> edges are marked as <strong>medium</strong> severity. (0.4 &#8804; Impact Score &lt; 0.7)
          <br><strong>{{ lowImpact.length }}</strong> edges are marked as <strong>low</strong> severity. (Impact Score &lt; 0.4)          
        </div>
        <p class="pt-2"> 
          Nodes marked as <strong>High Severity</strong> must be corrected with the highest priority.
          <br>Nodes marked as <strong>Medium Severity</strong> must be corrected with high priority.
          <br>Nodes marked as <strong>Low Severity</strong> are encouraged, but not required, to be corrected.
        </p>
      </div>
    </div>
    <div class="col-12">
      <h2>Network Edge Severity Table</h2>
      <div>
        <table v-if="!loading" class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 7.5%">Edge</th>
              <th scope="col" style="width: 16.6%">Base Score</th>
              <th scope="col" style="width: 16.6%">Exploitability Score</th>
              <th scope="col" style="width: 16.6%">Impact Score</th>
            </tr>
          </thead> 
          <tbody>
            <tr v-for="edge in network.links" :key="edge.id">
              <td style="width: 5%; word-wrap: anywhere;">({{ edge.source }}, {{edge.target}})</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.base_score }} / {{GetSeverity(edge.base_score)}}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.exploitability_score }} / {{GetSeverity(edge.exploitability_score)}}</td>
              <td style="width: 16.6%; word-wrap: anywhere;">{{ edge.impact_score }} / {{GetSeverity(edge.impact_score)}}</td>
            </tr> 
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <hr>
  <h1>Recommendations</h1>
  <div class="mx-5 row">
    <div class="col-12">
      <div class="text-left">
        <h2>TOPSIS Recommendations</h2>
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
    <div class="col-12">
      <h2>TOPSIS Node Ranking</h2>
      <div>
        <table v-if="topsisResults" class="table table-hover">
          <thead>
            <tr>
              <th scope="col" style="width: 10%">ID</th>
              <th scope="col" style="width: 15%">Layer</th>
              <th scope="col" style="width: 15%">Product</th>
              <th scope="col" style="width: 15%">Vendor</th>
              <th scope="col" style="width: 20%">TOPSIS Score</th>
              <th scope="col" style="width: 15%">Ranking</th>
            </tr>
          </thead> 
          <tbody>
            <tr v-for="result in topsisResults" :key="result.id">
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
import DoughnutChart from '@/components/DoughnutChart.vue';
import NetworkGraph from '@/components/ModelDrivenNetworkGraph.vue';
import Histogram from '@/components/Histogram.vue';
export default {
  name: 'Model Driven Results - Printout',

  components: {
    ResultHeader,
    DoughnutChart,
    NetworkGraph,
    Histogram
  },

 data() {
    return {
      error: undefined,
      numHosts: 0,
      numVulnHosts: 0,
      nonVulnHostPerc: 0,
      vulnHostPerc: 0,
      compTime: 0,
      nvdDate: undefined,
      title: undefined,
      inputDate: undefined,
      nodes: [],
      edges: [],
      loading: true,
      loadingNVD: true,
      network: {
        nodes: undefined,
        links: undefined,
      },
      betweeness: [],
      closeness: [],
      degree: [],
      indegree: [],
      katz: [],
      outdegree: [],
      pagerank: [],
      indegreeSum: 1,
      outdegreeSum: 1,
      degreeSum: 1,
      numRecommend: 5,
      topsisResults: []
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    PrintResults() {
      window.print()
    },

    GetSeverity(x) {
      if (x >= 0.7) return 'High';
      if (x < 0.7 && x >= 0.4) return 'Medium';
      if (x < 0.4) return 'Low';
    },

    GetData() {
      this.loading = true;
      this.loadingNVD = true;
        http.get('/nvd/get_nvd_update_date').then((r) => {
          console.log(r);
          this.NVDDate = r.data.date;
          this.loadingNVD = false;
        }).catch((e) => {
          this.error = e;
        });
  
        http.get('/model_driven/get_network_title').then((r) => {
          // console.log(r);
          this.title = r.data.network_title;
        }).catch((e) => {
          this.error = e;
        });
  
        http.get('/model_driven/get_input_date').then((r) => {
          // console.log(r);
          this.inputDate = r.data.input_date;
        }).catch((e) => {
          this.error = e;
        });

      http.get('/model_driven/vulnerable_host_percentage').then((r) => {
        this.compTime = r.data.computation_time;
        this.nonVulnHostPerc = r.data.non_vulnerable_host_percentage;
        this.numHosts = r.data.number_hosts;
        this.numVulnHosts = r.data.number_vulnerable_hosts;
        this.vulnHostPerc = r.data.vulnerable_host_percentage;
      }).catch((e) => {
        this.error = e;
      });

      http.get('/model_driven/get_network_topology').then((r) => {     
        this.network = { links: r.data.edges, nodes: r.data.nodes };
        this.nodes = r.data.nodes;
        var unique = [];
        r.data.edges.forEach((e) => {
          var n = r.data.nodes.filter((x) => x.id === e.target)[0];
          if (!unique.includes(n.id)) {
            this.edges.push({
              id: n.id,
              layer: n.layer,
              vendor: n.vendor,
              product: n.product,
              base_score: e.base_score,
              exploitability_score: e.exploitability_score,
              impact_score: e.impact_score
            });
            unique.push(n.id);
          }
        });
        this.loading = false;
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
          })
      })

      http.get('/model_driven/centrality').then((r) => {
        console.log(r);

        this.betweeness = r.data.betweeness;
        this.closeness = r.data.closeness;
        this.degree = r.data.degree;
        this.indegree = r.data.indegree;
        this.katz = r.data.katz;
        this.outdegree = r.data.outdegree;
        this.pagerank = r.data.pagerank;

      });
    }
  },

  computed: {
    corpFW1() {
      return this.network.nodes.filter((n) => { return n.layer === 'corp_fw_1'});
    },

    corpDMZ() {
      return this.network.nodes.filter((n) => { return n.layer === 'corp_dmz'});
    },

    corpFW2() {
      return this.network.nodes.filter((n) => { return n.layer === 'corp_fw_2'});
    },

    corpLAN() {
      return this.network.nodes.filter((n) => { return n.layer === 'corp_lan'});
    },

    csFW1() {
      return this.network.nodes.filter((n) => { return n.layer === 'cs_fw_1'});
    },

    csDMZ() {
      return this.network.nodes.filter((n) => { return n.layer === 'cs_dmz'});
    },

    csFW2() {
      return this.network.nodes.filter((n) => { return n.layer === 'cs_fw_2'});
    },

    csLAN() {
      return this.network.nodes.filter((n) => { return n.layer === 'cs_lan'});
    },

   degreeProb() {
      var ratio = Math.max.apply(Math, this.degree);
      return this.degree.map(x => x /= ratio);
    },

    indegreeProb() {
      var ratio = Math.max.apply(Math, this.indegree);
      return this.indegree.map(x => x /= ratio);
    },

    outdegreeProb() {
      var ratio = Math.max.apply(Math, this.outdegree);
      return this.outdegree.map(x => x /= ratio);
    },

    highBase() {
      return this.edges.filter((e) => { return e.base_score >= 0.7});
    },

    mediumBase() {
      return this.edges.filter((e) => { return e.base_score < 0.7 && e.base_score >= 0.4});
    },

    lowBase() {
      return this.edges.filter((e) => { return e.base_score < 0.4});
    },

    highExploitability() {
      return this.edges.filter((e) => { return e.exploitability_score >= 0.7});
    },

    mediumExploitability() {
      return this.edges.filter((e) => { return e.exploitability_score < 0.7 && e.exploitability_score >= 0.4});
    },

    lowExploitability() {
      return this.edges.filter((e) => { return e.exploitability_score < 0.4});
    },

    highImpact() {
      return this.edges.filter((e) => { return e.impact_score >= 0.7});
    },

    mediumImpact() {
      return this.edges.filter((e) => { return e.impact_score < 0.7 && e.impact_score >= 0.4});
    },

    lowImpact() {
      return this.edges.filter((e) => { return e.impact_score < 0.4});
    },
  }
}
</script>
<style>
@media print {
  .noprint {
    visibility: hidden;
    display: none;
  }
}
</style>