<template>
<div>
    <qr-code :username="'ktany001'"></qr-code>
    <data-driven-input></data-driven-input>
    <!-- <user-data-table title="Unregistered Users" :users="d"></user-data-table> -->
    <!-- <user-data-table title="All Users" :users="d" :approve="false"></user-data-table> -->
</div> 
</template>


<script>
import DataDrivenInput from '../components/DataDrivenInput.vue'
import UserDataTable from '../components/UserDataTable.vue'
import QRCode from './QRCode.vue'

export default {
/* eslint-disable */ 
    name: 'Sandbox',

    components: {
        'qr-code': QRCode,
        DataDrivenInput,
        UserDataTable,
    },

    data() {
        return {
            d: [
                {
                    name: 'Kyle',
                    email: 'ktany001@odu.edu',
                    username: 'ObtainTheGrain69'
                }
            ],
        }
    },
}
</script>
