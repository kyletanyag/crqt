<template>
  <body>
    <h3 style="padding-left:10px"> Input Settings: Corporate Firewall, Corporate DMZ and Corporate LAN</h3>

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
      <input type="button" class="btn btn-primary btn-lg active" style="margin-bottom:15px;" @click="saveNodes(), submit = !submit" value="Continue">
    </div>
    <!-- <button type="button" class="btn btn-secondary mx-2" @click="preview = !preview">Preview</button> -->
          
    <div v-if="submit">
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
      <div style="padding-left:15px; margin-top:20px">
        <input type="button" class="btn btn-primary btn-lg active" style="margin-bottom:15px;" @click="saveEdges(); Submit()" value="Submit">
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
      CorpDMZ: CorpDMZServerTypes,
      CorpLAN: CorpLANServerTypes,
      CSDMZ: CSDMZserverTypes,
      CSLan: CSLanSystemServerTypes,
      layerNames: NISTLayerNames,
      progress: 0,
      network_title: ""
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
      for (let layer = 1; layer <= 8; layer++) {
        for (let i = 0; i < this.$refs[`${layer}`].rowData.length; i++) {          
          this.$refs[`${layer}`].rowData[i].id = ID++;
          this.nodes.push(this.$refs[`${layer}`].rowData[i]);
          this.checkNodes(this.nodes[i])
        }
      }
    },
    checkNodes(Layer){
      console.log("Hello "+Layer)
      for(let i=0; i<=Layer.length;i++){
        
        if(Layer[i]==""){
          console.log("Blank Spaces")
        }
      }
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

    Submit() {
      if (!this.networkTitle) {
        const d = new Date();
        var hr = d.getHours() < 10 ? `0${d.getHours()}` : d.getHours();

        this.networkTitle = `Model-Driven_Network_${d.getFullYear()}${d.getMonth()+1}${d.getDate()}_${hr}${d.getMinutes()}`
      }
      
      this.Upload(this.network, (event) => {
        this.progress = Math.round(100 * event.loaded / event.total);
      })
      .then((response) => {
        console.log(response.data.message);
        // this.$router.push({name: 'Sandbox'});
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
  }
}; 
</script>

<style>
   table, th, td {
   border: 1px solid rgb(226, 226, 226);
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
   }

</style>
<style src="@vueform/multiselect/themes/default.css"></style>