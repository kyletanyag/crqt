<template>
   <body>
      <h3 style="padding-left:10px"> Input Settings: Corporate Firewall, Corporate DMZ and Corporate LAN</h3>
      <h4 style="padding-left:10px"> If you would like to upload a CSV file, click the button below.</h4>
         <!-- HOLDEN REMOVED THIS BECAUSE HE MADE A NEW LINK. KEEPING THIS IN CASE YOU WANT TO REUSE THE FORMATTING.
         <form class="form-inline my-2 my-lg-0" action="/Sandbox" style="padding-left:10px">
            <button type="submit">CSV File Upload</button>
                  </form> -->
      <router-link to="/Sandbox" tag="button">CSV Upload</router-link>
      <data-driven-input></data-driven-input>
      <h4> Corporate Firewall L1 Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate Firewall 1.</p>
      <table width=100% border="0" cellspacing="0" >
         <tbody>
            <tr>
               <td width="33%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select v-model="L1Vendor">
                        <option v-for="item in L1VendorInput" :key="item" :value="item">{{item}}</option>
                     </select>
                  </div>
               </td>
               <td align="center" width="33%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
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
                  <!-- {{ input }} -->
         </tbody>
      </table>
      <h4> Corporate DMZ Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate DMZ Network. Use the "Add Server" button to add and "Remove Server" button to remove </p>
      <form>
         <input type="button" @click="addRow(index)" value="Add Server">
         <input type="button" @click="removeRow(index)" value="Remove Server">
      </form>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr v-for="(row, index) in rows" :key="index">
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
                     <select v-model="serverProduct">
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
            </tr>
         </tbody>
      </table>
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
 
   <input type="button" @click="Submit()" value="Submit">
  
   </body>
</template>

<script>
import DataDrivenInput from '../components/DataDrivenInput.vue';
/* eslint-disable */ 
import http from "../http-common";
// import { ref } from 'vue';
export default {
  components: { DataDrivenInput },

  data() {
   //   const coporateFirewall = ref([]);
   //   http.get('/produts').then((d) => { coporateFirewall.value = d.data });

    return {
      
      L1VendorInput:['Cisco',
         'Juniper',
         'Microsoft',],
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
               serverProduct:this.serverProduct
            };
        },
    },
    methods:{
      Submit() {
               this.Upload(this.input, (event) => {                  
                this.progress = Math.round(100 * event.loaded / event.total);
         })
         
      },
      Upload(data, onUploadProgress) {
            return http.post("/upload", data , { onUploadProgress });
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
</style>