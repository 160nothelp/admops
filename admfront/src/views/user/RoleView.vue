<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-input placeholder="请输入内容" v-model="search">
            <el-button slot="append" icon="el-icon-search" @click="getList(1)"></el-button>
          </el-input>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" @click="addDialogVisible = true">增加角色</el-button>
        </el-col>
      </el-row>
      <el-table :data="dataList" border style="width: 100%">
        <el-table-column type="index"></el-table-column>
<!--        <el-table-column prop="id" label="id"></el-table-column>-->
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button type="info" icon="el-icon-setting" size="mini" @click="handleSetPerm(row)"></el-button>
            <el-button type="success" icon="el-icon-edit" size="mini" @click="handleEdit(row)"></el-button>
            <el-button type="danger" icon="el-icon-delete" size="mini" @click="handleDel(row.id)"></el-button>
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
    <!-- 授权 -->

    <el-dialog title="角色授权" :visible.sync="addPermDialogVisible" @close="resetTree">
      <!-- node-key="id"，this.$refs[‘tree’].getCheckedKeys()时，返回选中节点的id -->
      <!-- :props="defaultProps"，指定显示用的label的属性和子节点的属性 -->
      <!-- :default-checked-keys="selectedIds" 默认勾选的key的数组，指定显示用的label的属性和子节点的属性 -->
      <!-- this.$refs.tree.getCheckedKeys() 获得被选择的复选框 -->
      <el-tree
          :data="permList"
          show-checkbox
          accordion
          node-key="id"
          ref="tree"
          highlight-current
          :props="defaultProps"
          :default-checked-keys="selectedIds"
      >
      </el-tree>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addPermDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addPerm">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 增加 -->
    <el-dialog title="增加" :visible.sync="addDialogVisible" @close="resetForm('add')">
      <el-form :model="addForm" :rules="addRules" ref="add" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="add">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改 -->
    <el-dialog title="增加" :visible.sync="editDialogVisible" @close="resetForm('edit')">
      <el-form :model="editForm" :rules="addRules" ref="edit" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="editForm.name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="edit">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "RoleView.vue",
  data() {
    return {
      search: '',
      dataList: [],
      addDialogVisible: false,
      editDialogVisible: false,
      addPermDialogVisible: false,
      permList: [],
      selectedIds: [],
      defaultProps: {
        children: 'children',
        label: 'name'
      },
      currentRole: {},
      pagination: {page: 1, size: 20, total: 0},
      addRules: {
        name: [
          {required: true, message: '请输入名称', trigger: 'blur'},
          {min: 1, max: 16, message: '长度在 1 到 16 个字符', trigger: 'blur'},
        ],
      },
      addForm: {},
      editForm: {},
    }
  },
  created() {
    this.getList()
  },
  methods: {
    resetForm(name) {
      this.$refs[name].resetFields()
    },
    resetTree() {
      this.currentRole = {}
      this.selectedIds = []
      this.permList = []
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
      const {data: response} = await this.$http.get('users/roles/',
          {params: {'page': this.pagination.page, 'size': this.pagination.size, 'search': this.search}})
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.dataList = response.results
      this.pagination = response.pagination
    },
    add() {
      this.$refs["add"].validate(async (valid) => {
        if (valid) {
          const {data: response} = await this.$http.post('users/roles/', this.addForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.addDialogVisible = false
          await this.getList()
        }
      })
    },
    handleDel(id) {
      this.$msgbox.confirm('删除该角色, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(async () => {
        const {data: response} = await this.$http.delete(`users/roles/${id}/`)
        if (response.code) {
          return this.$message.error(response.message)
        }
        await this.getList()
      })
    },
    handleEdit(row) {
      this.editForm = row
      this.editDialogVisible = true
    },
    async handleSetPerm(row) {
      const {id} = row
      const {data: response} = await this.$http.get(`users/roles/${id}/perms/`)
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.permList = response.allPerms
      this.selectedIds = response.permissions
      this.currentRole = row
      this.addPermDialogVisible = true
    },
    edit() {
      const {id} = this.editForm
      this.$refs["edit"].validate(async (valid) => {
        if (valid) {
          const {data: response} = await this.$http.patch(`users/roles/${id}/`, this.editForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.editDialogVisible = false
          await this.getList()
        }
      })
    },
    async addPerm() {
      const permissions = this.$refs['tree'].getCheckedKeys()
      const {id} = this.currentRole
      const {data: response} = await this.$http.patch(`users/roles/${id}/`, {'permissions': permissions})
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.addPermDialogVisible = false
    }
  }
}
</script>

<style scoped>

</style>