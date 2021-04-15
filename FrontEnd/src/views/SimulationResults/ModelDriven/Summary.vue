<template>
<div>
  <result-header 
    title="Summary"
    nextPage="Model Driven Results - Network Visualization"
    defaultPage="Model Driven Results"
  />
  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>
  <div class="mx-5 text-left row">
    <div class="col">
      <div>
        <h2>Network Breakdown</h2>
        <p>
          You have entered your network topology titled: <strong>{{ title }}</strong> on <strong>{{ inputDate }}</strong>. 
          It took <strong>{{ compTime }}</strong> second(s) to compute the generated metrics. 
        </p>
        <p>
          The computed metrics use NVD Vulnerability data updated as recent as <strong>{{ NVDDate }}</strong>.
        </p>
        <p>
          Your inputted network contains a total of <strong>{{ nodes.length }}</strong> nodes and <strong>{{ edges.length }}</strong> edges.
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
      <doughnut-chart
        name="Network Topology Layer Breakdown"
      />
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
import ResultHeader from '@/components/ResultHeader.vue';
import DoughnutChart from '@/components/DoughnutChart.vue';

export default {
  name: 'Model Driven Results - Summary',

  components: {
    ResultHeader,
    DoughnutChart
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
      loading: true
    }
  },

  created() {
    this.GetData();
  },

  methods: {
    GetData() {
      this.loading = true;

      http.get('/model_driven/get_network_topology').then((r) => {
        this.edges = r.data.edges;
        this.nodes = r.data.nodes;
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

      http.get('/nvd/get_nvd_update_date').then((r) => {
        // console.log(r);
        this.NVDDate = r.data.date;
      }).catch((e) => {
        this.error = e;
      });

      http.get('get_network_title').then((r) => {
        // console.log(r);
        this.title = r.data.network_title;
      }).catch((e) => {
        this.error = e;
      });

      http.get('get_input_date').then((r) => {
        // console.log(r);
        this.inputDate = r.data.input_date;
      }).catch((e) => {
        this.error = e;
      });
    }
  },

  computed: {
    corpFW1() {
      return this.nodes.filter((n) => { return n.layer === 'corp_fw_1'});
    },

    corpDMZ() {
      return this.nodes.filter((n) => { return n.layer === 'corp_dmz'});
    },

    corpFW2() {
      return this.nodes.filter((n) => { return n.layer === 'corp_fw_2'});
    },

    corpLAN() {
      return this.nodes.filter((n) => { return n.layer === 'corp_lan'});
    },

    csFW1() {
      return this.nodes.filter((n) => { return n.layer === 'cs_fw_1'});
    },

    csDMZ() {
      return this.nodes.filter((n) => { return n.layer === 'cs_dmz'});
    },

    csFW2() {
      return this.nodes.filter((n) => { return n.layer === 'cs_fw_2'});
    },

    csLAN() {
      return this.nodes.filter((n) => { return n.layer === 'cs_lan'});
    }
  }
}
</script>
<style>
</style> 