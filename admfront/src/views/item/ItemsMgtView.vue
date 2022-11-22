<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>项目组</el-breadcrumb-item>
      <el-breadcrumb-item>项目管理</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="12">

        </el-col>
        <el-col :span="12">
          <el-button type="primary" @click="addDialogVisible = true">增加项目</el-button>
        </el-col>
      </el-row>
      <el-table border style="width: 100%" :data="dataList">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="item_name" label="项目名"></el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button v-if="row.id !== 1" @click="handleEdit(row)" type="success" icon="el-icon-edit" size="mini">
            </el-button>
            <el-button v-if="row.id !== 1" @click="handleDel(row.id)" type="danger" icon="el-icon-delete" size="mini">
            </el-button>
          </template>
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
    <!-- 添加项目 -->
    <el-dialog title="增加项目" :visible.sync="addDialogVisible" @close="resetForm('add')">
      <itemsForm ref="add"></itemsForm>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="postAdd">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改项目 -->
    <el-dialog title="修改" :visible.sync="editDialogVisible" @close="resetForm('edit')">
      <itemsForm ref="edit" :editForm="editForm"></itemsForm>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="edit">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import itemsForm from "@/views/item/ components/ItemsForm";

export default {
  name: "ItemsMgtView",
  components: {itemsForm},
  data() {
    return {
      dataList: [],
      addDialogVisible: false,
      editDialogVisible: false,
      pagination: {page: 1, size: 20, total: 0},
      editForm: {},
    }
  },
  created() {
    this.getList()
  },
  methods: {
    resetForm(name) {
      this.$refs[name].resetForm()
    },
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
      const {data: response} = await this.$http.get('items/item_mgt/',
          {params: {'page': this.pagination.page, 'size': this.pagination.size, 'search': this.search}})
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.dataList = response.results
      this.pagination = response.pagination
    },
    async postAdd() {
      // this.$refs['add'].validate(async (valid) => {
      //   if (valid) {
      //     const {data: response} = await this.$http.post('items/item_mgt/', this.addForm)
      //     if (response.code) {
      //       return this.$message.error(response.message)
      //     }
      //     this.addDialogVisible = false
      //     await this.getList()
      //   }
      // })
      const valid = this.$refs['add'].submitForm()
      if (valid) {
        const formData = this.$refs['add'].addForm
        const {data: response} = await this.$http.post('items/item_mgt/', formData)
        if (response.code) {
          return this.$message.error(response.message)
        }
        this.addDialogVisible = false
        await this.getList()
      }
    },
    handleEdit(row) {
      this.editForm = row
      this.editDialogVisible = true
    },
    async edit() {
      const {id} = this.$refs['edit'].addForm
      const valid = this.$refs['edit'].submitForm()
      if (valid) {
        const formData = this.$refs['edit'].addForm
        const {data: response} = await this.$http.patch(`items/item_mgt/${id}/`, formData)
        if (response.code) {
          return this.$message.error(response.message)
        }
         this.editDialogVisible = false
        await this.getList()
      }
    },
    handleDel(id) {
      this.$msgbox.confirm('删除该项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(async () => {
        const {data: response} = await this.$http.delete(`items/item_mgt/${id}/`)
        if (response.code) {
          return this.$message.error(response.message)
        }
        await this.getList()
      })
    },
  }
}
</script>

<style scoped>

</style>