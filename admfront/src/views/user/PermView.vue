<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>权限列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-input placeholder="请输入内容" v-model="search">
            <el-button slot="append" icon="el-icon-search" @click="getList(1)"></el-button>
          </el-input>
        </el-col>
        <el-col :span="12">
          <!-- en -->
        </el-col>
      </el-row>
      <el-table border style="width: 100%" :data="dataList">
        <el-table-column type="index"></el-table-column>
        <!--        <el-table-column prop="id" label="id"></el-table-column>-->
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="codename" label="codename"></el-table-column>
        <el-table-column prop="content_type.app_label" label="应用"></el-table-column>
        <el-table-column prop="content_type.model" label="模型"></el-table-column>
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
  name: "PermView.vue",
  data() {
    return {
      search: '',
      dataList: [],
      pagination: {page: 1, size: 20, total: 0},

    }
  },
  created() {
    this.getList()
  },
  methods: {
    handleCurrentChange(val) {
      this.pagination.page = val
      this.getList()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.getList()
    },
    async getList(page) {
      if (page) {
        this.pagination.page = page
      }
      const {data: response} = await this.$http.get('users/perms/',
          {params: {'page': this.pagination.page, 'size': this.pagination.size, 'search': this.search}})
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.dataList = response.results
      this.pagination = response.pagination
    },
  }
}
</script>

<style scoped>

</style>