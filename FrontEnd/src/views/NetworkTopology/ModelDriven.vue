<template>
  <div class="text-left mx-5">
    <h1 class="text-center">Model-Driven Input</h1>
    <div class="my-4">
      <h2>Background:</h2>
      <p>

      </p>
    </div>
    <hr>
    <div class="my-4">
      <h3>JSON File Upload:</h3>
      <p>
        If you would like to upload a previously built network topology, please upload the JSON file here: 
      </p>
      <input class="form-control-file pb-2" type="file" @change="selectFile" accept="application/JSON"> 
      <button class="btn btn-primary" @click="Submit">Upload</button>
    </div>
    <hr>
    <div class="my-4">
      <h3> Build Your Own Network Topology: </h3>
      <div class="my-3">
        <h4>Title of Network:</h4>
        <p>
          Please type the name of your network topology that you are building. This will be useful
          if you decide to save your network or network results later on.
        </p>
        <input v-model="network_title" placeholder="Title of Network" type="text">
      </div>
      <div class="my-3">
        <h3>Select Network Nodes:</h3>
        <p>
          In this section, you will select the different network components for each layer that defines your network topology.
        </p>
        <model-driven-firewall class="pb-3" title="Corporate Firewall 1" :vendors="firewalls" layer="corp_fw_1" ref="1"/>
        <model-driven-setting title="Corporate DMZ" :serverTypes="CorpDMZ" 
          :vendors="servers" layer="corp_dmz" ref="2"/>
        <model-driven-firewall title="Corporate Firewall 2" :vendors="firewalls" layer="corp_fw_2" ref="3"/>
        <model-driven-setting title="Corporate LAN" :serverTypes="CorpLAN" 
          :vendors="servers" layer="corp_lan" ref="4"/>
        <model-driven-firewall title="Control System Firewall 1" :vendors="firewalls" layer="cs_fw_1" ref="5"/>
        <model-driven-setting title="Control System DMZ" :serverTypes="CSDMZ" 
          :vendors="servers" layer="cs_dmz" ref="6"/>
        <model-driven-firewall title="Control System Firewall 2" :vendors="firewalls" layer="cs_fw_2" ref="7"/>
        <model-driven-setting title="Control System LAN" :serverTypes="CSLan" 
          :vendors="servers" layer="cs_lan" ref="8"/>
        <div style="padding-left:15px; margin-top:20px">
          <input type="button" class="btn btn-primary btn-lg active" style="margin-bottom:15px;" @click="saveNodes()" value="Continue">
        </div>
      </div>
    </div>
    <!-- <button type="button" class="btn btn-secondary mx-2" @click="preview = !preview">Preview</button> -->
          
    <div v-if="submit">
      <h3>Define Network Connections:</h3>
      <p>
        In this section, you will define all different network connections between layers for each node.
        <br>
        If you are unsure how to define to your network connections, you can select the checkbox below have
        all nodes connected to each other.
      </p>
      <div class="mb-2 mx-5">
        <input class="form-check-input" type='checkbox' @click='checkAll()' v-model='isCheckAll'> <strong> Check All</strong>
      </div>
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_fw_1')" :layerNodes2="filterNodes('corp_dmz')" 
        :layerName1="layerNames[0]" :layerName2="layerNames[1]" ref="9" />
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_dmz')" :layerNodes2="filterNodes('corp_fw_2')" 
        :layerName1="layerNames[1]" :layerName2="layerNames[2]" ref="10" />
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_fw_2')" :layerNodes2="filterNodes('corp_lan')" 
        :layerName1="layerNames[2]" :layerName2="layerNames[3]" ref="11" />
      <model-driven-connection 
        :layerNodes1="filterNodes('corp_lan')" :layerNodes2="filterNodes('cs_fw_1')" 
        :layerName1="layerNames[3]" :layerName2="layerNames[4]" ref="12" />
      <model-driven-connection 
        :layerNodes1="filterNodes('cs_fw_1')" :layerNodes2="filterNodes('cs_dmz')" 
        :layerName1="layerNames[4]" :layerName2="layerNames[5]" ref="13" />
      <model-driven-connection 
        :layerNodes1="filterNodes('cs_dmz')" :layerNodes2="filterNodes('cs_fw_2')" 
        :layerName1="layerNames[5]" :layerName2="layerNames[6]" ref="14" />
      <model-driven-connection 
        :layerNodes1="filterNodes('cs_fw_2')" :layerNodes2="filterNodes('cs_lan')" 
        :layerName1="layerNames[6]" :layerName2="layerNames[7]" ref="15" />
      <div class="pl-2 pt-3">
        <input type="button" class="btn btn-primary btn-lg mx-2" @click="saveEdges(); Submit()" value="Submit">
        <button type="button" class="btn btn-secondary btn-lg mx-2" @click="preview = !preview">Preview</button>
        <button type="button" class="btn btn-success btn-lg mx-2" @click="Save">Save</button>
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
/* eslint-disable */ 
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
    })

    http.get('/product_query_by_type/server').then((r) => {
      // console.log(r);
      r.data.query.forEach((e) => {
        if (r.data.error) console.log(r.data.error);
        this.servers.push(e)
      });
    })
  },

  data() {
    return {
      firewalls: [],
      servers: [],
      nodes:[],
      edges:[],
      submit: false,
      missingField: false,
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
      this.missingField = false;
      for (let layer = 1; layer <= 8; layer++) {
        for (let i = 0; i < this.$refs[`${layer}`].rowData.length; i++) {    

          this.$refs[`${layer}`].rowData[i].id = ID++;
          this.nodes.push(this.$refs[`${layer}`].rowData[i]);
          if(this.$refs[`${layer}`].rowData[i].id % 2 ==0){
            if(this.$refs[`${layer}`].rowData[i].vendor==null || this.$refs[`${layer}`].rowData[i].product==null ||
              this.$refs[`${layer}`].rowData[i].type==null){
                console.log(this.$refs[`${layer}`].rowData[i])
              this.missingField = true;
            }
          }
          else{
            if(this.$refs[`${layer}`].rowData[i].vendor==null || this.$refs[`${layer}`].rowData[i].product==null){
                console.log(this.$refs[`${layer}`].rowData[i])
              this.missingField = true;
            }
          }
        }
      }
      console.log(this.missingField)
      if (this.missingField == false) {
         this.submit = !this.submit
      } else {
        this.submit = !this.submit  /// TAKE THIS OUT WHEN DONE TESTING
        // alert('Please make sure to fill out all fields'); // UNCOMMENT WHEN DONE TESTING
        this.missingField = false;
        console.log(this.missingField)
      }
      ///this.checkNodes()
    },

    filterNodes(layerName) {
      return this.nodes.filter((n) => {
        return n.layer == layerName;
      });
    },

    saveEdges() {
      this.edges = [];
      // defines edges from remote attack to all 1st layer nodes
      this.edges.push({
        currNode: 0,
        nextNode: this.filterNodes('corp_fw_1').map(n => n.id)
      });

      for (let conn = 9; conn <= 15; conn++) {
        for (let i = 0; i < this.$refs[`${conn}`].rowData.length; i++) {
          this.edges.push(this.$refs[`${conn}`].rowData[i])
        }
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
        console.log(obj)
        this.nodes = obj.vertices;
        this.edges = obj.arcs;
        this.network_title = obj.network_title
      });

      reader.readAsText(file);
    },

    Submit() {
      if (!this.networkTitle) {
        const d = new Date();
        var hr = d.getHours() < 10 ? `0${d.getHours()}` : d.getHours();

        this.networkTitle = `Model-Driven_Network_${d.getFullYear()}${d.getMonth()+1}${d.getDate()}_${hr}${d.getMinutes()}`
      }
      
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
    },

    Upload(data, onUploadProgress) {
      return http.post("/network_topology_model_driven_input", data , { onUploadProgress });
    }, 
    
    GetCardSize() { // Needs to be fixed.
      return {
        'width' : 100,
        'height' : 100
      };
    },

    Save() {
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.network, undefined, 2));
      var dlAnchorElem = document.getElementById('downloadAnchorElem');
      dlAnchorElem.setAttribute("href", dataStr);
      dlAnchorElem.setAttribute("download", `${this.network.network_title.toLowerCase()}.json`);
      dlAnchorElem.click();
    },
  }
}; 
</script>

<style>
</style>
<style src="@vueform/multiselect/themes/default.css"></style>