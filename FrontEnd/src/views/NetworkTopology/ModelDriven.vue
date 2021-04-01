<template>
   <body>
      <h3 style="padding-left:10px"> Input Settings: Corporate Firewall, Corporate DMZ and Corporate LAN</h3>

      <model-driven-firewall title="Corporate Firewall L1" :vendors="L1VendorInput" layer="corp_fw_1" ref="1"/>

      <!-- <model-driven-firewall title="Corporate Firewall L1" :vendors="L1VendorInput" layer="corp_fw_1" ref="2"/> -->
      <model-driven-setting title="Corporate DMZ" :serverType="DMZServerType" 
      :vendorServer="serverVendorInput" layer="corp_dmz" @DataCall="addNodes" ref="2"/>
      <model-driven-firewall title="Corporate Firewall L2" :vendors="L2VendorInput" layer="corp_fw_2" ref="3"/>
      <model-driven-setting title="Corporate LAN" :serverType="LANServerVendorInput" 
      :vendorServer="serverVendorInput" layer="corp_lan" @DataCall="addNodes"/>


      <model-driven-firewall title="Control System Firewall L1" :vendors="L1VendorInput" layer="cs_fw_1"/>
      <model-driven-setting title="Control System DMZ" :serverType="CSDMZserverType" 
      :vendorServer="serverVendorInput" layer="cs_dmz" @DataCall="addNodes"/>
      <model-driven-firewall title="Control System Firewall L2" :vendors="L2VendorInput" layer="cs_fw_2"/>
      <model-driven-setting title="Control System LAN" :serverType="CSLanSystemServerType" 
      :vendorServer="serverVendorInput" layer="corp_lan" @DataCall="addNodes"/>

   <input type="button" @click="Submit()" value="Submit">
   
          <button type="button" class="btn btn-secondary mx-2" @click="preview = !preview">Preview</button>
          
          <div v-if="preview" class="card mx-2" :style="GetCardSize()">
            <div class="card-header">JSON Object Preview</div>
            <div class="card-body" style="overflow-y: auto;">
            
                <div>
                    {{ input }}
                </div>
            </div>
        </div>
   </body>
</template>


<script>
/* eslint-disable */ 
//  JSON OBJECT layer, nodes, edges
import http from "../../http-common";
import Multiselect from '@vueform/multiselect'
import ModelDrivenFirewall from '@/components/ModelDrivenFirewall.vue';
import ModelDrivenSetting from '@/components/ModelDrivenSetting.vue';
// import { ref } from 'vue';
export default {
   components: { 
      Multiselect,
      ModelDrivenFirewall,
      ModelDrivenSetting,
   },
  data() {
   //   const coporateFirewall = ref([]);
   //   http.get('/produts').then((d) => { coporateFirewall.value = d.data });
    return {
      ID:1,
      preview: false,
      nodeSelect: false,
      L1VendorInput:[
      {
        label:"Cisco",
        options:["Cisco1","Cisco2","Cisco3"]
      },
      {
        label:"Juniper",
        options:["Juniper1","Juniper2","Juniper"]
      },
      {
        label:"Microsoft",
        options:["Microsoft1","Microsoft2","Microsoft3"]
      }
    ],
      L2VendorInput:[
      {
        label:"Cisco",
        options:["Cisco1","Cisco2","Cisco3"]
      },
      {
        label:"Juniper",
        options:["Juniper1","Juniper2","Juniper"]
      },
      {
        label:"Microsoft",
        options:["Microsoft1","Microsoft2","Microsoft3"]
      }
    ],
     selectedVendor:undefined, 
     selectedOption:[],
      L1Vendor:[],
      NumberFireWall: 0,
      // L1ProductInput: [
      //    "ASA5500",
      //    "ASA5505",
      //    "ASA5510",
      //    "ASA5520",
      //    "ASA5540",
      //    "ASA5550",
      //    "ASA5580",
      //    "ASA5585X" ],
      L1Product:[],
      serverVendorInput: [
         "Cisco",
         "Juniper",
         "Microsoft",
         "Paloalto",
         "Linux",
         "Oracle",
         "Semens",
         "Emerson",
         "SchneiderElectric",], 
      LANServerVendorInput:[
         "Business Server",
         "Business Workstation",
         "Web Application Server"
      ],
      DMZserverVendor:[],                                    
      progress: 0,
      output: "",
      DMZServerType: [
         "Email Server",
         "Web Server",
         "FTP Server",
         "DNS Server",
         "WAP Server",
         "AUTHENTICATION Server"],
      emailServer:[],
      serverProductInput: [
         "windowsxp",
         "windows_xp",
         "windows_vista",
         "windows_7",
         "windows_server_2008",
         "windows_server_2012",
         "windows_server_2016",
         "windows_server_2003",
         "SQLServer",],
      serverProduct:[],
      rows: [1],
      coporateFirewall: [
         'Cisco',
         'Juniper',
         'Microsoft',
      ],
      CSDMZserverType:["Ext Business COMM Server",
                     "WWW Server",
                     "Database Server",
                     "Security Server",
                     "Authentication Server",
      ],
      CSLanSystemServer:[],
      CSLanSystemServerType:["Application Server",
                           "Historian",
                           "Database Server",
                           "Configuration Server",
                           "HMI Computers",
                           "Engineering Workstation",
      ],
      
            progress: 0,
            numberServer: 0,
    };
  },  
//   watch: {
//     serverProduct(){
//       // binding this to the data value in the email input
//       this.ValidateServerProduct();
//     }
//   },
    computed: {
        input() {
            return {
               selectedVendor: this.selectedVendor,
               NumberFireWall: this.NumberFireWall,
               L1Product: this.L1Product,
               emailServer:this.emailServer,
               serverVendor:this.serverVendor,
               serverProduct:this.serverProduct,
               numberServer:this.numberServer
            };
        },
        nodes() {
           
           var nodes = [];
           for (let i = 0; i < this.NumberFireWall; i++) {
              nodes.push( {
                 layer: 'corp_fw_1',
                 id: i,
                 vendor: 'Cisco', // Changes to be consitent with var
                 product: this.L1Product,
                 vulnerabilites: 'x'
              })
           }
           return {
              nodes
           };
        }
    },
    methods:{
   Submit() {
      //console.log(this.$refs.a.rowData)
      console.log('Got event!')
      var ID =1;
      var layerVal = '';
      for(var layers = 1; layers<=3; layers++ ) {
        layerVal = String(layers);
        console.log("Layer: "+ this.$refs[layerVal].rowData.length)
         
        for(var i; i < this.$refs[layerVal].rowData.length; i++) {
          this.$refs[layerVal].rowData[i].id = ID,
          console.log(this.$refs[layerVal])
        }
      }
      var nodes = [];
            //for (let i = 0; i < n.length; i++) {
              //n[i].id = this.ID++    
              //this.$refs.a.rowData[0].id=ID,        
              nodes.push( 
                 
               this.$refs.a.rowData
               
               //   layer: n[0],
               //   id: n.id,
               //   type: n.type,
               //   vendor:n.vendor, // Changes to be consitent with var
               //   product: n.product,
               //   vulnerabilites: 'x'
              )
           //}
           console.log(nodes)
           return {
              nodes
           };
        
            //    this.Upload(this.input, (event) => {
            //    this.progress = Math.round(100 * event.loaded / event.total);
            // })
            // .then((response) => {
            //     console.log(response.data.message);
            //     // this.$router.push({name: 'Sandbox'});
            // })
            
        },
   Upload(data, onUploadProgress) {
            return http.post("/network_topology_model_driven_input", data , { onUploadProgress });
        }, 
   addRow: function(_index){
         this.rows.splice(_index+1,0, this.rows[_index]);
    },
    removeRow: function(_index){
      //console.log(row);d
      this.rows.splice(_index-1, 1);
    },
   addNodes(n) {
      console.log('Got event!')
      //console.log(n);
      var nodes = [];
            //for (let i = 0; i < n.length; i++) {
              //n[i].id = this.ID++            
              nodes.push( 
                 
               n
               //   layer: n[0],
               //   id: n.id,
               //   type: n.type,
               //   vendor:n.vendor, // Changes to be consitent with var
               //   product: n.product,
               //   vulnerabilites: 'x'
              )
           //}
           console.log(nodes)
           return {
              nodes
           };
        }
   },
    
    GetCardSize() {
            return {
                'width' :100,
                'height' : 100
            };
        },
   ValidateServerProduct(){
   if (this.serverProduct!=""){
      return false;  // kbt false
   }
    },  
    selectVendor: function(selectedVendor){
       this.selectedVendor = selectedVendor;
       this.selectedOption='';
    },
  
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