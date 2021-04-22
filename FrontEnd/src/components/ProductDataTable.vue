<template>
<div>
  <div class="card mt-4" >
    <div class="card-header font-weight-bold">{{ title }}</div>
    <div :style="`overflow-y: auto; height: ${height}px;`">
      <table v-if="data" class="table table-hover">
        <thead>
          <tr>
            <th @click="sort('vendor')" scope="col">Vendor<i :class="sortDirection('vendor')"></i></th>
            <th @click="sort('product')" scope="col">Product<i :class="sortDirection('product')"></i></th>
            <th @click="sort('type')" scope="col">Type<i :class="sortDirection('type')"></i></th>
            <th scope="col">Action</th>
          </tr>
        </thead> 
          <tbody v-for="(item, index) in sortedData" :key="index">
            <tr>
              <td >{{ item.vendor }}</td>
              <td >{{ item.product }}</td>
              <td>{{ item.type }}</td>
              <td>
                <button @click="DeleteProduct(item.vendor, item.product, item.type)" class="btn btn-danger btn-sm mx-1">Delete</button>
                <button class="btn btn-info btn-sm mx-1">
                  <a :href="`http://localhost:2000/search/${item.vendor.toLowerCase()}/${item.product.toLowerCase()}`" target="_blank" class="text-white">Info</a>
                </button>
              </td>
            </tr> 
          </tbody>
      </table>
    </div>
  </div>
</div>
</template>

<script>
import http from '@/http-common.js';
export default {
  name: 'Product Data Table',

  props: {
    title: String,
    data: {
      type: Array,
      required: true,
    },
    height: {
      type: Number,
      default: 240,
    }
  },

  data() {
    return {
      currentSort: 'vendor',
      currentSortDir: 'asc',
    }
  },

  computed: {
    sortedData() {
      if (!this.data) return 0;
      return this.data.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    }
  },

  methods: {
    sort(s) {
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir ==='asc' ? 'desc':'asc';
      }
      this.currentSort = s;
    },

    sortDirection(s) {
      if (this.currentSortDir === 'asc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-asc';
      else if (this.currentSortDir === 'desc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-desc';
      else
        return 'fa fa-fw fa-sort';
    },

    DeleteProduct(v, p, t) {
      http.get(`/product_remove/${v}/${p}/${t}`).then((r) => {
        console.log(r);
      });
      this.$emit('delete');
    },
  },
}
</script>
<style>
table thead tr th {
  text-align: center;
  position: sticky;
  top: 0px;
  background-color: rgb(255, 255, 255);
  color: rgb(0, 0, 0);
 }
</style>