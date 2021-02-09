<template>
<div>
    <div class="col d-flex justify-content-center my-2">
        <div class="card">
            <div class="card-header">Data-Driven Input</div>
            <div class="card-body text-left">
                <h5 class="card-title">Two Input files required:</h5>
                <div>
                    <p class="pr-3 font-weight-bold">Vertex.CSV file</p>
                    <vue-csv-import v-model="vertices"
                        :fields="{
                            id: {required: true, label: 'id'},
                            description: {required: true, label: 'description'},
                            logic: {required: true, label: 'logic'},
                            direction: {required: true, label: 'direction'}}"
                    >
                        <vue-csv-toggle-headers></vue-csv-toggle-headers>
                        <vue-csv-errors></vue-csv-errors>
                        <vue-csv-input></vue-csv-input>
                        <vue-csv-map></vue-csv-map>
                    </vue-csv-import>
                </div>
                <div>
                    <p class="pr-3 font-weight-bold">Arcs.CSV file</p>
                    <vue-csv-import v-model="arcs"
                        :fields="{
                            currNode: {required: true, label: 'current_node'},
                            nextNode: {required: true, label: 'next_node'},
                            direction: {required: true, label: 'direction'}}"
                    >
                        <vue-csv-toggle-headers></vue-csv-toggle-headers>
                        <vue-csv-errors></vue-csv-errors>
                        <vue-csv-input></vue-csv-input>
                        <vue-csv-map></vue-csv-map>
                    </vue-csv-import>
                </div>
                <button type="submit" class="btn btn-primary" @click="submit">Submit</button>
                <div class="progress">
                    <div class="progress-bar progress-bar-info"
                        role="progressnbar"
                        :style="{ width: progress + '%' }"
                    >
                        {{ progress}}%
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col d-flex justify-content-center my-2">
        <div class="card">
            <div class="card-header">JSON Object Preview</div>
            <div class="card-body">
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
    // VueCsvSubmit,
    VueCsvMap,
    VueCsvInput,
    VueCsvErrors,
    VueCsvImport
} from 'vue-csv-import';

import http from "../http-common";
// import UploadFiles from '../components/UploadFiles.vue';

export default {
    name: 'DataDrivenInput',

    components: {
        VueCsvToggleHeaders,
        // VueCsvSubmit,
        VueCsvMap,
        VueCsvInput,
        VueCsvErrors,
        VueCsvImport
        // UploadFiles
    },

    data() {
        return {
            vertices: null,
            arcs: null,
            progress: 0,
        };
    },

    computed: {
        network() {
            return {
                vertices: this.vertices,
                arcs: this.arcs
            };
        },
    },

    methods: {
        submit() {
            // post('upload', this.network).then((r) => {console.log(r)});
            this.upload(this.network, (event) => {
                this.progress = Math.round(100 * event.loaded / event.total);
            })
            .then((response) => {
                console.log(response);
            })
            .catch(() => {
                this.progress.percentage = 0;
                console.log('Could not upload data!');
            })
        },

        upload(data, onUploadProgress) {
            return http.post("/upload", data , {
                headers: {
                    "Content-Type": "application/json"
                },
                onUploadProgress
            });
        },
    },
}
</script>
