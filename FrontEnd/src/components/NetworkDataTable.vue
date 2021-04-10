<template>
<div>
  <h4>{{ title }}</h4>
  <div :style="`overflow-y: auto; height: ${height}px;`">
    <table v-if="data" class="table table-hover">
      <thead>
        <tr>
          <th @click="sort('id')" scope="col" style="width: 7.5%">ID<i :class="sortDirection('id')"></i></th>
          <th @click="sort('description')" scope="col" style="width: 35%">Description<i :class="sortDirection('description')"></i></th>
          <th @click="sort('base_score')" scope="col" style="width: 20%">Base Score<i :class="sortDirection('base_score')"></i></th>
          <th @click="sort('ranking')" scope="col" style="width: 10%">Ranking<i :class="sortDirection('ranking')"></i></th>
        </tr>
      </thead> 
        <tbody v-for="(node, index) in sortedData" :key="index">
          <tr>
            <td style="width: 7.5%">{{ node.id }}</td>
            <td style="width: 35%">{{ node.description }}</td>
            <td style="width: 20%">{{ node.base_score }}</td>
            <td style="width: 10%">{{ node.ranking }}</td>
          </tr> 
        </tbody>
    </table>
  </div>
</div>
</template>

<script>
export default {
  name: 'Network Data Table',

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
      currentSort: 'ranking',
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