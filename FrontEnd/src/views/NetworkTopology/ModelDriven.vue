<template>
  <div class="text-left mx-5">
    <h1 class="text-center">Model-Driven Input</h1>
    <div class="my-4">
      <h2>Instructions:</h2>
      <p>

      </p>
    </div>
    <hr>
    <div class="my-4">
      <h2>JSON File Upload:</h2>
      <p>
        If you would like to upload a previously built network topology, please upload the JSON file here: 
      </p>
      <input class="form-control-file pb-2" type="file" @change="selectFile" accept="application/JSON"> 
      <button class="btn btn-primary" @click="progress = 0; edgesDone = true; Submit()">Upload</button>
      <div class="progress my-4" style="width: 40%">
        <div class="progress-bar progress-bar-info"
          role="progressbar"
          :style="{ width: progress + '%' }"
          :aria-valuenow="progress"
          aria-valuemin="0"
          aria-valuemax="100"
        >
          {{progress}}%
        </div>
      </div>
    </div>
    <hr>
    <div class="my-4">
      <h2> Build Your Own Network Topology: </h2>
      <div class="my-3">
        <h3>Title of Network:</h3>
        <p>
          Please type the name of your network topology that you are building. This will be useful
          if you decide to save your network or network results later on. If left blank, we will 
          provide a network name for you.
        </p>
        <input v-model="network_title" placeholder="Title of Network" type="text" onkeypress="return event.charCode != 32">
      </div>
      <hr>
      <div id="network_input_top"></div>
      <div class="my-3" v-show="!nodesDone">
        <h3>Select Network Nodes:</h3>
        <p>
          In this section, you will select the different network components for each layer that defines your network topology.
        </p>
        <model-driven-firewall class="pb-3" title="Corporate Firewall 1" :vendors="firewalls" layer="corp_fw_1" ref="1"/>
        <hr>
        <model-driven-setting title="Corporate DMZ" :serverTypes="CorpDMZ" 
          :vendors="servers" layer="corp_dmz" ref="2"/>
          <hr>
        <model-driven-firewall title="Corporate Firewall 2" :vendors="firewalls" layer="corp_fw_2" ref="3"/>
        <hr>
        <model-driven-setting title="Corporate LAN" :serverTypes="CorpLAN" 
          :vendors="servers" layer="corp_lan" ref="4"/>
          <hr>
        <model-driven-firewall title="Control System Firewall 1" :vendors="firewalls" layer="cs_fw_1" ref="5"/>
        <hr>
        <model-driven-setting title="Control System DMZ" :serverTypes="CSDMZ" 
          :vendors="servers" layer="cs_dmz" ref="6"/>
          <hr>
        <model-driven-firewall title="Control System Firewall 2" :vendors="firewalls" layer="cs_fw_2" ref="7"/>
        <hr>
        <model-driven-setting title="Control System LAN" :serverTypes="CSLan" 
          :vendors="servers" layer="cs_lan" ref="8"/>
        <div style="padding-left:15px; margin-top:20px">
          <button class="btn btn-primary btn-lg pb-2" @click="saveNodes()"> 
            Continue &nbsp;<i class="fa fa-arrow-right"></i>
          </button>
        </div>
        <hr>          
      </div>
    </div>
    <div  v-show="nodesDone">
      <div class="pl-1 py-2">
        <button class="btn btn-primary btn-lg" @click="nodesDone = !nodesDone"><i class="fa fa-arrow-left"></i>&nbsp;Back</button>
      </div>
      <h2>Define Network Connections:</h2>
      <p style="width: 75%">
        In this section, you will define all network connections between nodes at each layer. 
        <strong>Note: Nodes can only connect to nodes at the next layer. </strong> 
        <br>
        For example, a node in the Corporate Firewall 1 layer can only connect to nodes
        in the Corporate DMZ layer.
      </p>
      <div class="pb-4">
        <p>
          If you are unsure how to define to your network connections, you can select the checkbox below have
          all nodes connected to each other. 
          <br>
          <strong>Note: By connecting all nodes together, you may
          experience long computational times and delay in getting your results.</strong>
        </p>
        <tr>
          <td class="pr-5">
            <strong>Overall network connection options: </strong>
          </td>
          <td>
            <input class="form-check-input" type='checkbox' @click='checkAll()' v-model='isCheckAll'> <strong> Connect All</strong>
          </td>
        </tr>
      </div>
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_fw_1')" :layerNodes2="filterNodes('corp_dmz')" 
        :layerName1="layerNames[0]" :layerName2="layerNames[1]" ref="9" />
        <hr>
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_dmz')" :layerNodes2="filterNodes('corp_fw_2')" 
        :layerName1="layerNames[1]" :layerName2="layerNames[2]" ref="10" />
        <hr>
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_fw_2')" :layerNodes2="filterNodes('corp_lan')" 
        :layerName1="layerNames[2]" :layerName2="layerNames[3]" ref="11" />
        <hr>
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_lan')" :layerNodes2="filterNodes('cs_fw_1')" 
        :layerName1="layerNames[3]" :layerName2="layerNames[4]" ref="12" />
        <hr>
      <model-driven-connection 
        :layerNodes1="filterNodes('cs_fw_1')" :layerNodes2="filterNodes('cs_dmz')" 
        :layerName1="layerNames[4]" :layerName2="layerNames[5]" ref="13" />
        <hr>
      <model-driven-connection 
        :layerNodes1="filterNodes('cs_dmz')" :layerNodes2="filterNodes('cs_fw_2')" 
        :layerName1="layerNames[5]" :layerName2="layerNames[6]" ref="14" />
        <hr>
      <model-driven-connection 
        :layerNodes1="filterNodes('cs_fw_2')" :layerNodes2="filterNodes('cs_lan')" 
        :layerName1="layerNames[6]" :layerName2="layerNames[7]" ref="15" />
      <div class="pl-2 pt-3">
        <input type="button" class="btn btn-primary btn-lg mx-2" @click="saveEdges();Submit()" value="Submit">
        <button type="button" class="btn btn-secondary btn-lg mx-2" @click="saveEdges();GetNetworkTitle(); preview = !preview">Preview</button>
        <button type="button" class="btn btn-success btn-lg mx-2" @click="saveEdges(); Save()">Save</button>
        <a id="downloadAnchorElem" style="display:none"></a>
      </div>
      <div v-if="preview" class="card mx-2 mt-4 mb-2">
        <div class="card-header font-weight-bold">
          JSON Object Preview
        </div>
        <div class="card-body" style="overflow-y: auto;">
          <div>
            {{ network }}
          </div>
        </div>
      </div>
      <div class="progress my-4" style="width: 80%">
        <div class="progress-bar progress-bar-info"
          role="progressbar"
          :style="{ width: progress + '%' }"
          :aria-valuenow="progress"
          aria-valuemin="0"
          aria-valuemax="100"
        >
          {{progress}}%
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import http from "../../http-common";
import ModelDrivenFirewall from '@/components/ModelDrivenFirewall.vue';
import ModelDrivenSetting from '@/components/ModelDrivenSetting.vue';
import ModelDrivenConnection from '../../components/ModelDrivenConnection.vue';
import 
{   
  CorpDMZServerTypes,
  CorpLANServerTypes,
  CSDMZserverTypes,
  CSLanSystemServerTypes,
  NISTLayerNames
} from '@/utilities/nist-constants.js';

export default {

  components: { 
    ModelDrivenFirewall,
    ModelDrivenSetting,
    ModelDrivenConnection,
  },

  created() {
    http.get('/product_query_by_type/firewall').then((r) => {
      // console.log(r);
      r.data.query.forEach((e) => {
        if (r.data.error) console.log(r.data.error);
        this.firewalls.push(e)
      });
    });

    http.get('/product_query_by_type/server').then((r) => {
      // console.log(r);
      r.data.query.forEach((e) => {
        if (r.data.error) console.log(r.data.error);
        this.servers.push(e)
      });
    });
  },

  data() {
    return {
      firewalls: [],
      servers: [],
      nodes:[],
      edges:[],
      nodesDone: false,
      edgesDone: false,
      CorpDMZ: CorpDMZServerTypes,
      CorpLAN: CorpLANServerTypes,
      CSDMZ: CSDMZserverTypes,
      CSLan: CSLanSystemServerTypes,
      layerNames: NISTLayerNames,
      progress: 0,
      network_title: "",
      preview: false,
      isCheckAll: false,
      selectedNodes:[],
    };
  },  
  computed: {
    network() {
      const d = new Date();
      return {
        network_title: this.network_title,
        date: `${d.getMonth()+1}/${d.getDate()}/${d.getFullYear()}`,
        vertices: this.nodes,
        arcs: this.edges
      };
    },
  },

  methods:{
    saveNodes() {
      var ID = 1;
      this.nodes = []
      let missingField = false;
      for (let layer = 1; layer <= 8; layer++) {
        if (!this.$refs[`${layer}`].checkSelection) {
          missingField = true;
          break;
        }
        for (let i = 0; i < this.$refs[`${layer}`].rowData.length; i++) {    
          this.$refs[`${layer}`].rowData[i].id = ID++;
          this.nodes.push(this.$refs[`${layer}`].rowData[i]);
        }
      }

      if (missingField) {
        // this.nodesDone = !this.nodesDone  /// TAKE THIS OUT WHEN DONE TESTING
        alert('Please make sure to fill out all fields'); /// UNCOMMENT WHEN DONE TESTING
      } else {
        this.nodesDone = true;
      }
      this.Scroll();
    },

    filterNodes(layerName) {
      return this.nodes.filter((n) => {
        return n.layer == layerName;
      });
    },

    saveEdges() {
      this.edges = [];
      let missingField = false;

      for (let conn = 9; conn <= 15; conn++) {
        if (!this.$refs[`${conn}`].checkSelection) {
          missingField = true;
          break;
        }    
        for (let i = 0; i < this.$refs[`${conn}`].rowData.length; i++) {
          this.edges.push(this.$refs[`${conn}`].rowData[i])
        }
      }

      if (missingField) {
        // this.edgesDone = !this.edgesDone  /// TAKE THIS OUT WHEN DONE TESTING
        alert('Please make sure to check at least one box per section.'); /// UNCOMMENT WHEN DONE TESTING
      } else {
        this.edgesDone = true;
        this.edges.filter((n) => { return n.nextNode.length > 0; });
      }
    },

    checkAll() {
      this.isCheckAll = !this.isCheckAll;
      for (let conn = 9; conn <= 15; conn++) {
        this.isCheckAll ? this.$refs[`${conn}`].checkAll() : this.$refs[`${conn}`].uncheckAll();
      }
    },

    selectFile(event) {
      var file = event.target.files[0]
      var reader = new FileReader();

      reader.onload = ((event) => {
        var obj = JSON.parse(event.target.result);
        // console.log(obj)
        this.nodes = obj.vertices;
        this.edges = obj.arcs;
        this.network_title = obj.network_title
      });

      reader.readAsText(file);
    },

    GetNetworkTitle() {
      if (this.network_title == "") {
        const d = new Date();
        var hr = d.getHours() < 10 ? `0${d.getHours()}` : d.getHours();

        this.network_title = `Model-Driven_Network_${d.getFullYear()}${d.getMonth()+1}${d.getDate()}_${hr}${d.getMinutes()}`
      }
    },

    Submit() {
      if (this.edgesDone) {
        this.GetNetworkTitle();

        this.Upload(this.network, (event) => {
          this.progress = Math.round(100 * event.loaded / event.total);
        })
        .then(() => {
          this.$emit('uploadedData');
        })
        .catch(() => {
          this.progress = 0;
          console.log('Could not upload data!');
        });
      }
    },

    Upload(data, onUploadProgress) {
      return http.post("/network_topology_model_driven_input", data , { onUploadProgress });
    }, 
    
    Scroll() {
      document.getElementById('network_input_top').scrollIntoView({behavior: 'smooth'});
    },

    Save() {
      this.GetNetworkTitle();
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.network, undefined, 2));
      var dlAnchorElem = document.getElementById('downloadAnchorElem');
      dlAnchorElem.setAttribute("href", dataStr);
      dlAnchorElem.setAttribute("download", `${this.network_title.toLowerCase()}.json`);
      dlAnchorElem.click();
    },
  }
}; 
</script>

<style>
</style>
<style src="@vueform/multiselect/themes/default.css"></style>