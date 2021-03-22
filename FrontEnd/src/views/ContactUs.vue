<template>
  <div style="width: 600px">
    <table-lite
    :has-checkbox="true"
    :is-loading="table.isLoading"
    :is-re-search="table.isReSearch"
    :columns="table.columns"
    :rows="table.rows"
    :total="table.totalRecordCount"
    :sortable="table.sortable"
    :messages="table.messages"
    @do-search="doSearch"
    @is-finished="tableLoadingFinish"
    @return-checked-rows="updateCheckedRows"
></table-lite>
  </div>
</template>

<script>
import TableLite from "vue3-table-lite";
export default {
  name: 'Demo',
  data() {
    return {
      params: {
        data: [
          ['Index', 'Data1', 'Data2', 'Data3'],
          [1, 'b3ba90', '7c95f7', '9a3853'],
          [2, 'ec0b78', 'ba045d', 'ecf03c'],
          [3, '63788d', 'a8c325', 'aab418']
        ],
        header: 'column',
        border: true,
        columnWidth: [{column: 0, width: 60}]
      }
    }
  },
  components: { TableLite }
}
</script>