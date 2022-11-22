<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>项目组</el-breadcrumb-item>
      <el-breadcrumb-item>项目计划</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="12">

        </el-col>
        <el-col :span="12">
          <el-select v-model="selected_item" multiple filterable placeholder="请选择" @change="getList(1)">
            <el-option
                v-for="item in options"
                :key="item.id"
                :label="item.item_name"
                :value="item.id">
            </el-option>
          </el-select>
        </el-col>
      </el-row>
      <el-table border style="width: 100%" :data="dataList">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="plan_name" label="计划名"></el-table-column>
        <el-table-column label="操作">

        </el-table-column>
      </el-table>
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[20, 50, 100]"
          :page-size="pagination.size"
          layout="total, prev, pager, next, jumper, sizes"
          :total="pagination.total"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "ItemPlansView",
  data() {
    return {
      dataList: [],
      pagination: {page: 1, size: 20, total: 0},
      options: [],
      selected_item: [],
    }
  },
  created() {
    this.getItems()
  },
  methods: {
    async getList(page) {
      if (page) {
        this.pagination.page = page
      }
      let selected_value = this.selected_item.join(',')
      const {data: response} = await this.$http.get('items/item_plan/',
          {params: {'page': this.pagination.page, 'size': this.pagination.size, 'search': this.search,
              'item_name': selected_value}})
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.dataList = response.results
      this.pagination = response.pagination
    },
    async getItems() {
      const {data: response} = await this.$http.get('items/item_plan/items/')
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.options = response
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.getList()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.getList()
    },
  }
}
</script>

<style scoped>

</style>