<template>
<div>
  <div class="row">
    <h1> {{ tableTitle }} </h1>
    <button type="button" class="btn btn-primary ml-4" v-if="exportOn"
      @click="downloadTableAsCsv"> Export to CSV </button>
  </div>
  <hr />
  <div class="row mt-3 mb-3" v-if="showData">
    <div class="col">
      <div class="input-group mb-3">
        <input type="text"
          class="form-control"
          v-model="filterTerms"
          placeholder="filter the results"
          aria-label="filter the results">
        <div class="input-group-append">
          <span class="input-group-text">showing {{ filteredCount }} of {{ totalCount }}</span>
          <button type="button"
            class="btn btn-outline-secondary"
            @click="performFilter">filter</button>
          <button type="button"
            class="btn btn-outline-secondary"
            @click="clearFilterTerms">clear</button>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <table class="table" v-if="showData" id="export">
            <thead>
              <tr>
                <th scope="col" v-for="(n, i) in dataColumns" :key="i">{{ n.title }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(result, i) in filteredData" :key="i">
                <td v-for="(n, ni) in dataColumns" :key="ni">
                  {{ result[n.prop] }}
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else>
            <p class="alert alert-warn">There are no search results to display.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>

import { toRaw, ref } from 'vue';
import { filter } from 'lodash';
import titleize from '../utilities/titleize';
import { download, tableAsCsv } from '../utilities/table-as-csv';

const filterTerms = ref('');
const allowFilter = ref(true);

export default {
  name: 'ObjectArrayAsTable',

  setup() {
    return {
      filterTerms,
      allowFilter,
    };
  },

  data() {
  },

  props: {
    data: Array,
    tableTitle: String,
    exportOn: {
      type: Boolean,
      default: true,
    },
  },

  methods: {
    clearFilterTerms() {
      this.filterTerms = '';
    },

    performFilter() {
      if (this.filterTerms) {
        this.allowFilter = true;
      }
    },

    downloadTableAsCsv() {
      // the id has to match the id element in the html above
      const tbl = document.getElementById('export');

      console.log(tbl);

      const data = tableAsCsv(tbl);
      download(data, `${this.tableTitle}.csv`, 'text/csv');
    },
  },

  computed: {
    filteredData() {
      if (!this.allowFilter) {
        return this.data;
      }

      return filter(this.data, (f) => {
        const s = JSON.stringify(f);
        const t = this.filterTerms.split(' ');

        for (let i = 0; i < t.length; i += 1) {
          if (s.toLowerCase().indexOf(t[i].toLowerCase()) >= 0) {
            return true;
          }
        }
        return false;
      });
    },

    filteredCount() {
      return this.filteredData.length;
    },

    totalCount() {
      return this.data.length;
    },

    showData() {
      return this.data && this.data.length > 0;
    },

    dataColumns() {
      const r = toRaw(this.data[0]);
      return Object.keys(r).map((k) => ({
        prop: k,
        title: titleize(k),
      }));
    },
  },
};
</script>
