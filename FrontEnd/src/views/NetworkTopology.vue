<template>
   <body>
      
      <h3 style="padding-left:10px"> Input Settings: Corporate Firewall, Corporate DMZ and Corporate LAN</h3>
      <h4 style="padding-left:10px"> If you would like to upload a CSV file, click the button below.</h4>
      <form class="form-inline my-2 my-lg-0" action="/Sandbox" style="padding-left:10px">
                        <button type="submit">CSV File Upload</button>
                    </form>
      <h4> Corporate Firewall L1 Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate Firewall 1.</p>
      <table width=100% border="0" cellspacing="0" >
         <tbody>
            <tr>
               <td width="33%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select v-model="L1Vendor">
                        <option value="Cisco">Cisco</option>
                        <option value="Juniper">Juniper</option>
                        <option value="Microsoft">Microsoft</option>
                        <option value="Paloalto">PALOALTO</option>
                        <option value="Linux">Linux</option>
                        <option value="Oracle">ORACLE</option>
                        <option value="Semens">Semens</option>
                        <option value="Emerson">Linux</option>
                        <option value="SchneiderElectric">Schneider-Electric</option>
                     </select>
                  </div>
               </td>
               <td align="center" width="33%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select v-model="L1Product">
                        <option value="ASA5500">Cisco</option>
                        <option value="ASA5505">Juniper</option>
                        <option value="ASA5510">Microsoft</option>
                        <option value="ASA5520">PALOALTO</option>
                        <option value="ASA5540">Linux</option>
                        <option value="ASA5550">ORACLE</option>
                        <option value="ASA5580">Semens</option>
                        <option value="ASA5585X">Linux</option>
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
                    {{ input }}
         </tbody>
      </table>
      <h4> Corporate DMZ Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate DMZ Network. Use the "Add Server" button to add and "Remove Server" button to remove </p>
      <form>
         <input type="button" @click="addRow(index)" value="Add Server">
         <input type="button" class="add-row" value="Remove Server">
      </form>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr v-for="(row, index) in rows" :key="index">
               <td width="25%">
                  <div align="center">
                     <p align="center">Server Type</p>
                     <select v-model="emailServer">
                        <option value="Gmail">Gmail</option>
                        <option value="Outlook">Outlook</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Vendor</p>
                     <select v-model="serverVendor">
                        <option value="Cisco">Cisco</option>
                        <option value="Juniper">Juniper</option>
                        <option value="Microsoft">Microsoft</option>
                        <option value="Paloalto">PALOALTO</option>
                        <option value="Linux">Linux</option>
                        <option value="Oracle">ORACLE</option>
                        <option value="Semens">Semens</option>
                        <option value="Emerson">Linux</option>
                        <option value="SchneiderElectric">Schneider-Electric</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Server Product</p>
                     <select v-model="serverProduct">
                        <option value="windowsxp">windowsxp</option>
                        <option value="windows_xp">windows_xp</option>
                        <option value="windows_vista">windows_vista</option>
                        <option value="windows_7">windows_7</option>
                        <option value="windows_server_2008">windows_server_2008</option>
                        <option value="windows_server_2012">windows_server_2012</option>
                        <option value="windows_server_2016">windows_server_2016</option>
                        <option value="windows_server_2003">windows_server_2003</option>
                        <option value="SQLServer">SQL_Server</option>
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
         <input type="button" class="add-row" value="Remove Server">
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

import http from "../http-common";
export default {

  data() {
    return {
      
      L1Vendor:"",
      NumberFireWall: 0,
      L1Product: "",
      progress: 0,
      output: "",
      emailServer:"",
      serverProduct:[],
      rows: [1]
    };
  },  
  watch: {
    serverProduct(){
      // binding this to the data value in the email input
      this.ValidateServerProduct();
    }
  },
    computed: {
        input() {
            return {
                L1Vendor: this.L1Vendor,
                NumberFireWall: this.NumberFireWall,
                L1Product: this.L1Product,
                emailServer:this.emailServer,
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
    ValidateServerProduct(){
      if (this.serverProduct!=""){
         
      }
    },
  
   //  removeRow: function(row){
   //    //console.log(row);d
   //    this.rows.$remove(row);
   //  }
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