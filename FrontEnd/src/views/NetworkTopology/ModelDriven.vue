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
      <edges :nodes="nodes" />
    </div>
  </body>
</template>


<script>
/* eslint-disable */ 
import http from "../../http-common";
import Multiselect from '@vueform/multiselect'
import ModelDrivenFirewall from '@/components/ModelDrivenFirewall.vue';
import ModelDrivenSetting from '@/components/ModelDrivenSetting.vue';
import Edges from '../../components/Edges.vue';
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
    Edges,
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
      firewalls: [],
      nodes:[],
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