<template>
  <body>
    <h3 style="padding-left:10px"> Input Settings: Corporate Firewall, Corporate DMZ and Corporate LAN</h3>
    <h5 style="padding-left:10px" >Please input all the correct settings for each server and firewall</h5>
    <p></p>
    <p></p>
    <p></p>
    <p>Title of Network: <input style="padding-left:10px" v-model="networkTitle" placeholder="Title of Network" type="text"></p>
    <p>If you would like to upload previously saved settings, please upload the saved file: 
    <input style="padding-left:10px" type="file" @change="selectFile"></p>

    <model-driven-firewall title="Corporate Firewall L1" :vendors="firewalls" layer="corp_fw_1" ref="1"/>
    <model-driven-setting title="Corporate DMZ" :serverTypes="CorpDMZ" 
      :vendors="servers" layer="corp_dmz" ref="2"/>
    <model-driven-firewall title="Corporate Firewall L2" :vendors="firewalls" layer="corp_fw_2" ref="3"/>
    <model-driven-setting title="Corporate LAN" :serverTypes="CorpLAN" 
      :vendors="servers" layer="corp_lan" ref="4"/>
    <model-driven-firewall title="Control System Firewall L1" :vendors="firewalls" layer="cs_fw_1" ref="5"/>
    <model-driven-setting title="Control System DMZ" :serverTypes="CSDMZ" 
      :vendors="servers" layer="cs_dmz" ref="6"/>
    <model-driven-firewall title="Control System Firewall L2" :vendors="firewalls" layer="cs_fw_2" ref="7"/>
    <model-driven-setting title="Control System LAN" :serverTypes="CSLan" 
      :vendors="servers" layer="cs_lan" ref="8"/>
    <div style="padding-left:15px; margin-top:20px">
      <input type="button" class="btn btn-primary btn-lg active" style="margin-bottom:15px;" @click="saveNodes()" value="Continue">
    </div>
    <!-- <button type="button" class="btn btn-secondary mx-2" @click="preview = !preview">Preview</button> -->
          
    <div v-if="submit">
      <input type='checkbox' @click='checkAll()' v-model='isCheckAll'> Check All
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
        <input type="button" class="btn btn-primary btn-lg active mx-2" @click="saveEdges(); Submit()" value="Submit">
        <button type="button" class="btn btn-secondary btn-lg mx-2" @click="preview = !preview">Preview</button>
        <button type="button" class="btn btn-success btn-lg mx-2" @click="Save">Save</button>
        <a id="downloadAnchorElem" style="display:none"></a>
      </div>
      <div v-if="preview" class="card mx-2 mb-2">
        <div class="card-header font-weight-bold">
          JSON Object Preview
        </div>
        <div class="card-body" style="overflow-y: auto;">
          <div>
            {{ network }}
          </div>
        </div>
      </div>
      <div class="progress">
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
  </body>
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
      this.edges =[]
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
   /* table, th, td {
   border: 1px solid rgba(86, 98, 143, 0.603);
   border-collapse: collapse;
   margin-left:7px;
   }
   th, td {
   padding: 2px;
    
   }
   h4{
   padding-left: 5px;
   padding-top: 10px;
   }
   p{
   font-size: 17px;
   font-weight: 550;
   padding-left: 10px;
   padding-bottom:5px;
   } */

</style>
<style src="@vueform/multiselect/themes/default.css"></style>