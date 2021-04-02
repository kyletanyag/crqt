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
      :vendors="servers" layer="corp_lan" ref="8"/>
    <div style="padding-left:15px; margin-top:20px">
      <input type="button" class="btn btn-primary btn-lg active" style="margin-bottom:15px;" @click="Submit(),submit = !submit" value="Submit">
    </div>
    <!-- <button type="button" class="btn btn-secondary mx-2" @click="preview = !preview">Preview</button> -->
          
    <div v-if="submit" class="card mx-2" :style="GetCardSize()">
      <!-- <div v-for="(row, index) in nodes" :key="index" :row="row"> -->
        <edges :node1="filterNodes('corp_fw_1')" :node2="filterNodes('corp_dmz')" :layer1="layers[0]" :layer2="layers[1]" ref="1"/>
        <!-- <edges :node1="Layer2Nodes" :node2="Layer3Nodes" :layer1="layers[1]" :layer2="layers[2]" ref="2"/>
        <edges :node1="Layer3Nodes" :node2="Layer4Nodes" :layer1="layers[2]" :layer2="layers[3]" ref="3"/>
        <edges :node1="Layer4Nodes" :node2="Layer5Nodes" :layer1="layers[3]" :layer2="layers[4]" ref="4"/>
        <edges :node1="Layer5Nodes" :node2="Layer6Nodes" :layer1="layers[4]" :layer2="layers[5]" ref="5"/>
        <edges :node1="Layer6Nodes" :node2="Layer7Nodes" :layer1="layers[5]" :layer2="layers[6]" ref="6"/>
        <edges :node1="Layer7Nodes" :node2="Layer8Nodes" :layer1="layers[6]" :layer2="layers[7]" ref="7"/> -->

      <!-- </div> -->

      <div style="padding-left:15px; margin-top:20px">
          <input type="button" class="btn btn-primary btn-lg active" style="margin-bottom:15px;" @click="saveEdges()" value="Submit">
      </div>
    </div>
  </body>
</template>


<script>
/* eslint-disable */ 
import http from "../../http-common";
import Multiselect from '@vueform/multiselect'
import ModelDrivenFirewall from '@/components/ModelDrivenFirewall.vue';
import ModelDrivenSetting from '@/components/ModelDrivenSetting.vue';
// import Edges from '../../components/Edges.vue';
import 
{   
  CorpDMZServerTypes,
  CorpLANServerTypes,
  CSDMZserverTypes,
  CSLanSystemServerTypes
} from '@/utilities/server-types.js';
export default {
  components: { 
    Multiselect,
    ModelDrivenFirewall,
    ModelDrivenSetting,
    // Edges,
  },
  created() {
    http.get('/product_query_by_type/firewall').then((r) => {
      console.log(r);
      r.data.query.forEach((e) => {
        if (r.data.error) console.log(r.data.error);
        this.firewalls.push(e)
      });
    })
    http.get('/product_query_by_type/server').then((r) => {
      console.log(r);
      r.data.query.forEach((e) => {
        if (r.data.error) console.log(r.data.error);
        this.servers.push(e)
      });
    })
  },
  data() {
    return {
      layers:["Firewall 1", "Corporate DMZ Settings", "Firewall 2", "Corporate LAN Settings", "Control Sytem Firewall 1", "Control System DMZ Settings", "Control System Firewall 2","Control System LAN Settings"],
      Edges:[],
      Layer1Nodes:[],
      Layer2Nodes:[],
      Layer3Nodes:[],
      Layer4Nodes:[],
      Layer5Nodes:[],
      Layer6Nodes:[],
      Layer7Nodes:[],
      Layer8Nodes:[],
      firewalls: [],
      nodes:[],
      vertices:[],
      arcs:[],
      servers: [],
      submit: false,
      CorpDMZ: CorpDMZServerTypes,
      CorpLAN: CorpLANServerTypes,
      CSDMZ: CSDMZserverTypes,
      CSLan: CSLanSystemServerTypes,
      progress: 0,
    };
  },  
  computed: {
    network(){
  
        return{
          vertices: this.nodes,
          arcs: this.edges}
     },

  },
  methods:{
    Submit() {
      var ID = 1;
      this.nodes=[]
      for(var layer = 1; layer <= 8; layer++) {
        for(var i = 0; i < this.$refs[layer].rowData.length; i++) {
          this.$refs[layer].rowData[i].id = ID++;
          this.nodes.push(this.$refs[layer].rowData[i]);
        }
      }
      console.log(this.nodes);
      
      // this.Upload(this.input, (event) => {
      //   this.progress = Math.round(100 * event.loaded / event.total);
      // })
      // .then((response) => {
      //   console.log(response.data.message);
      //   // this.$router.push({name: 'Sandbox'});
      // });
    },
    filterNodes(layerName){
      return this.nodes.filter((n)=>{
        return n.layer==layerName;
      });
    },
    saveEdges(){
      this.Edges =[]
      for(var layer = 1; layer <= 8; layer++) {
        for(var i = 0; i < this.$refs[layer].edges.length; i++) {
          this.Edges.push(this.$refs[layer].edges)
        }
      }
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
   border: 1px solid rgb(5, 5, 5);
   border-collapse: collapse;
   margin-left:7px;
   }
   th, td {
   padding: 5px;
   text-align: left;    
   }
   h4{
   padding-left: 10px;
   padding-top: 30px;
   }
   p{
   padding-left: 10px;
   padding-bottom:5px;
   }

</style>
<style src="@vueform/multiselect/themes/default.css"></style>