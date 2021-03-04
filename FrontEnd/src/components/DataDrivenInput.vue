<template>
<div class="row">
    <div class="col d-flex justify-content-center">
        <div class="card mx-2" id="maincard">
            <div class="card-header font-weight-bold">Data-Driven Input</div>
            <div class="card-body text-left">
                <h5 class="card-title">Two Input files required:</h5>
                <div class="pr-3 py-2">
                    <h6 class="font-weight-bold">Vertex.CSV file</h6>
                    <vue-csv-import v-model="vertices"
                        :fields="{
                            id: {required: true, label: 'ID'},
                            description: {required: true, label: 'Description'},
                            logic: {required: true, label: 'Logic'}}"
                    >
                        <vue-csv-input @change="progress = 0"></vue-csv-input>
                        <vue-csv-toggle-headers></vue-csv-toggle-headers>
                        <vue-csv-errors></vue-csv-errors>
                        <vue-csv-map></vue-csv-map>
                    </vue-csv-import>
                </div>
                <div class="pr-3 py-2">
                    <h6 class="font-weight-bold">Arcs.CSV file</h6>
                    <vue-csv-import v-model="arcs"
                        :fields="{
                            currNode: {required: true, label: 'Current Node'},
                            nextNode: {required: true, label: 'Next Node'}}"
                    >
                        <vue-csv-input @change="progress = 0"></vue-csv-input>
                        <vue-csv-toggle-headers></vue-csv-toggle-headers>
                        <vue-csv-errors></vue-csv-errors>
                        <vue-csv-map></vue-csv-map>
                    </vue-csv-import>
                </div>
                <div class="pr-3 py-2">
                    <h6 class="font-weight-bold">Derivation Node Probability</h6>
                    <input v-model.number="simConfig" placeholder="0.8" step="0.1" min="0" max="1" type="number" maxlength="2"
                        onkeyup="if(this.value > 1) this.value = 1; else if(this.value < 0) this.value = 0;">
                </div>
                <div class="text-center py-2">
                    <button type="button" class="btn btn-secondary mx-2" @click="preview = !preview">Preview</button>
                    <button type="submit" class="btn btn-primary" @click="Submit">Submit</button>
                </div>
                <div v-if="progress > 0" class="progress">
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
        </div>
        <div v-if="preview" class="card mx-2" :style="GetCardSize()">
            <div class="card-header">JSON Object Preview</div>
            <div class="card-body" style="overflow-y: auto;">
                <div>
                    {{ network }}
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>

import {
    VueCsvToggleHeaders,
    VueCsvMap,
    VueCsvInput,
    VueCsvErrors,
    VueCsvImport
} from 'vue-csv-import';

import http from "../http-common";

export default {
    name: 'DataDrivenInput',

    components: {
        VueCsvToggleHeaders,
        VueCsvMap,
        VueCsvInput,
        VueCsvErrors,
        VueCsvImport
    },

    data() {
        return {
            vertices: null,
            arcs: null,
            progress: 0,
            preview: false,
            simConfig: 0.8
        };
    },

    computed: {
        network() {
            return {
                vertices: this.vertices,
                arcs: this.arcs,
                sim_config: this.simConfig > 1 ? 1 : this.simConfig < 0 ? 0 : this.simConfig
            };
        },
    },

    methods: {
        Submit() {
            if (this.network.vertices === null || this.network.arcs === null) {
                alert('Missing CSV file(s)! Please make sure both CSV files have been selected.');
                return;
            } else if (this.network.sim_config === '') {
                alert('Error with Derivation Node Probability input. Please recheck input.');
                return;
            }
            this.Upload(this.network, (event) => {
                this.progress = Math.round(100 * event.loaded / event.total);
            })
            .then((response) => {
                console.log(response.data.message);
            })
            .catch(() => {
                this.progress.percentage = 0;
                console.log('Could not upload data!');
            })
        },

       Upload(data, onUploadProgress) {
            return http.post("/network_topology_data_driven_input", data , { onUploadProgress });
        }, 

        GetCardSize() {
            return {
                'width' : document.getElementById('maincard').offsetWidth + 'px',
                'height' : document.getElementById('maincard').offsetHeight + 'px'
            };
        },

        ValidateInput(n) {
            if(n > 1) 
                return 1; 
            else if(n < 0) 
                return 0;
        }
    },
}
</script>