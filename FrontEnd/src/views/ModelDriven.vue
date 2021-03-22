<template>
   <body>
      <h3 style="padding-left:10px"> Input Settings: Corporate Firewall, Corporate DMZ and Corporate LAN</h3>
      <h4> Corporate Firewall L1 Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate Firewall 1.</p>
      <table width=100% border="0" cellspacing="0" >
         <tbody>
            <tr>
               <td width="33%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select v-model="selectedVendor" @change="selectVendor">
                        <option v-for="(L1Vend,item) in L1VendorInput" :key="item" :value="item">{{L1Vend.label}}</option>
                     </select>
                  </div>
               </td>
               <td align="center" width="33%">
                  <div align="center">
                     <p>Coorporate Firewall L1 Product</p>
                     <select v-model="L1Product">
                        <option v-for="item in L1ProductInput" :key="item" :value="item">{{item}}</option>               
                     </select>
                  </div>
               </td>
               <td width="33%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>                     
                        <input type="text" v-model="NumberFireWall" placeholder="Number of Firewalls 1" />        
                  </div>
               </td>
            </tr>
            <table width="100%">
               <tbody>
               <tr width="100%" ><div v-if="selectedVendor != -1" align="center">
               <td>
               
               <!-- <option v-for="option in L1VendorInput[selectedVendor].options" :key="option" :value="option">{{option}}</option>                -->
               <!-- <label class="form-check-label" v-for="option in L1VendorInput[selectedVendor].options" :key="option" >{{option.options}}</label> -->
            <!-- <label class="form-check-label" v-for="item in L1VendorInput" :key="item" :value="item "  >{{item.options}}</label> -->
            <!-- <input type="checkbox" v-model="selectedOption"> -->
      <!-- <li :key="index" v-for="(agenda, index) in content.data.agendas"/>
      <Multiselect class="multiselect" align="center"
      v-model="L1Vendor"
      mode="multiple"
      placeholder="Select your Vulnerabilites"
      :options="L1VendorInput[selectedVendor].options"
      label="L1VendorInput[selectedVendor].options">
      </li> -->
      
				<Multiselect v-for="option in L1VendorInput[selectedVendor].options" :key="option"
            v class="multiselect" align="center"
            v-model="L1Vendor"
            mode="multiple"
            placeholder="Select your Vulnerabilites"
            :options="L1VendorInput[selectedVendor].options"
            label="L1VendorInput[selectedVendor].options">
            </multiselect>
         
                  <!-- <select v-model="selectedOption" v-if="selectedVendor != -1"> -->
                     <!-- <input type="checkbox" v-model="selectedOption" v-if="selectedVendor != -1"> -->
                     <!-- <option v-for="item in L1VendorInput" :key="item" :value="item">{{ item.options }}</option> -->
                  <!-- </select> -->
               </td></div>
               </tr>
               </tbody>
            </table>
         </tbody>
      </table>
      <h4> Corporate DMZ Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate DMZ Network. Use the "Add Server" button to add and "Remove Server" button to remove </p>
      <form>
         <input type="button" @click="addRow(index)" value="Add Server">
         <input type="button" @click="removeRow(index)" value="Remove Server">
      </form>
      <v-table id="AddServer" class="table-hover" width="100%" border="0" cellspacing="0" selectionMode="multiple"
        selectedClass="table-info">
         <tbody>
            <v-tr v-for="(row, index) in rows" :key="index" :row="row">
               <td width="25%">
                  <div align="center">
                     <p align="center">Server Type</p>
                     <select v-model="emailServer[index]">
                        <option v-for="item in emailServerInput" :key="item" :value="item">{{item}}</option>
                        
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Vendor</p>
                     <select v-model="serverVendor[index]">
                        <option v-for="item in serverVendorInput" :key="item" :value="item">{{item}}</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Product</p>
                     <select v-model="serverProduct[index]">
                        <option v-for="item in serverProductInput" :key="item" :value="item">{{item}}</option>                        
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Servers</p>
                         <input type="text" v-model="numberServer" placeholder="Number of Server" />      
                  </div>
               </td>
            </v-tr>
         </tbody>
      </v-table>
      <h4> Corporate Firewall L2 Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate Firewall L2.</p>
      <table width=100% border="0" cellspacing="0" >
         <tbody>
            <tr>
               <td width="33%">
                  <div align="center">
                     <p align="center">Corporate Firewall L2 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td align="center" width="33%">
                  <div align="center">
                     <p>Corporate Firewall L2 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="33%">
                  <div align="center">
                     <p>Number of Coporate Firewall L2</p>
                     <input type="text" v-model="numberServer" placeholder="Number of Corporate Firewall L2" />    
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4> Corporate LAN Settings</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate LAN Network.  Use the "Add Server" button to add and "Remove Server" button to remove </p>
      <form>
         <input type="button" class="add-row" value="Add Server">
         <input type="button" class="remove-row" value="Remove Server">
      </form>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr>
               <td width="25%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4>Control Systems Firewall L1 Settings:</h4>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr>
               <td width="25%">
                  <div align="center">
                     <p align="center">Control Systems Firewall L1 Settings</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4> Control Systems DMZ Settings:</h4>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr>
               <td width="25%">
                  <div align="center">
                     <p align="center">Control Systems DMZ Settings</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4>Control System Firewall 2 Settings:</h4>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr>
               <td width="25%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4>Control System LAN Settings:</h4>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr>
               <td width="25%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
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
import http from "../http-common";
import Multiselect from '@vueform/multiselect'
// import { ref } from 'vue';
export default {
   components: { Multiselect },
  data() {
   //   const coporateFirewall = ref([]);
   //   http.get('/produts').then((d) => { coporateFirewall.value = d.data });

    return {
      preview: false,
      
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
     selectedVendor:-1, 
     selectedOption:[],
      L1Vendor:[],
      NumberFireWall: 0,
      L1ProductInput: [
         "ASA5500",
         "ASA5505",
         "ASA5510",
         "ASA5520",
         "ASA5540",
         "ASA5550",
         "ASA5580",
         "ASA5585X" ],
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
      serverVendor:[],                                    
      progress: 0,
      output: "",
      emailServerInput: [
         "Gmail",
         "Outlook",],
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
               L1Vendor: this.L1Vendor,
               NumberFireWall: this.NumberFireWall,
               L1Product: this.L1Product,
               emailServer:this.emailServer,
               serverVendor:this.serverVendor,
               serverProduct:this.serverProduct,
               numberServer:this.numberServer
            };
        },
    },
    methods:{
      Submit() {
               this.Upload(this.input, (event) => {
                this.progress = Math.round(100 * event.loaded / event.total);
            })
            .then((response) => {
                console.log(response.data.message);
                // this.$router.push({name: 'Sandbox'});
            })
            
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
      ValidateServerProduct(){
         if (this.serverProduct!=""){
            return false;  // kbt false
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
    selectVendor: function(){
       this.selectedOption='';
    },
  }
};

       
</script>

<style>
   table, th, td {
   border: 1px solid rgb(5, 5, 5);
   border-collapse: collapse;
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
   padding-bottom:10px;
   }
   .multiselect{
   padding-top: 10px;
  color: black;
  text-decoration: none;
  display: block;
  text-align: center;
  widows: 50%;
  border-color:  black;
  }
  .multiselect:after {
  position: absolute;
  content: "";
  top: 10px;
  right: 5px;
  width: 0;
  height: 0;
  border: 6px solid transparent;
  border-color: rgb(3, 2, 2) transparent transparent transparent;
}
</style>