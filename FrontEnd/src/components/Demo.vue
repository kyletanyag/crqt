<template>
    <div>
        <vue-csv-import
            v-model="csv"
            :fields="
            {a: {required: true, label: 'Id'}, 
             b: {required: true, label: 'Description'},
             c: {required: true, label: 'Logic'},
             d: {required: true, label: 'Direction'}}"
        >
            <!-- <vue-csv-errors></vue-csv-errors> -->
            <vue-csv-toggle-headers></vue-csv-toggle-headers>
            <vue-csv-input></vue-csv-input>
            <vue-csv-map></vue-csv-map>
            <vue-csv-submit :url="'/'"></vue-csv-submit>
        </vue-csv-import>
        <div>
            {{ csv }}
        </div>
    </div>
</template>

<script>
 /* eslint-disable */
// import VueCsvErrors from './vue-csv-import/VueCsvErrors.vue';
import VueCsvImport from './vue-csv-import/VueCsvImport.vue';
import VueCsvInput from './vue-csv-import/VueCsvInput.vue';
import VueCsvMap from './vue-csv-import/VueCsvMap.vue';
import VueCsvSubmit from './vue-csv-import/VueCsvSubmit.vue';
import VueCsvToggleHeaders from './vue-csv-import/VueCsvToggleHeaders.vue';

export default {
    name: 'Demo',

    components: {
        // VueCsvErrors,
        VueCsvImport,
        VueCsvMap,
        VueCsvToggleHeaders,
        VueCsvSubmit,
        VueCsvInput
    },

    data() {
        return {
            csv: null,
        };
    },
}
</script>
        VueCsvInput
