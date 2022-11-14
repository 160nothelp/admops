<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-input placeholder="请输入内容" v-model="search">
            <el-button slot="append" icon="el-icon-search" @click="getList(1)"></el-button>
          </el-input>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" @click="addDialogVisible = true">增加用户</el-button>
        </el-col>
      </el-row>
      <el-table border style="width: 100%" :data="dataList">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="username" label="登录名"></el-table-column>
        <el-table-column prop="is_active" label="激活">
          <template #default="{ row }">
            <el-switch v-model="row.is_active" :disabled="row.id === 1" @change="handleChange(row)"></el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="is_superuser" label="管理员">
          <template #default="{ row }">
            <el-switch v-model="row.is_superuser" :disabled="row.id === 1" @change="handleChange(row)"></el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="电话"></el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button v-if="row.id !== 1" @click="handleEdit(row)" type="success" icon="el-icon-edit" size="mini"></el-button>
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
    <!-- 添加用户 -->
    <el-dialog title="增加用户" :visible.sync="addDialogVisible" @close="resetForm('add')">
      <el-form :model="addForm" :rules="addRules" ref="add" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="addForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="addForm.password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" v-model="addForm.checkPass"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="addForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="addForm.email"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="postAdd">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改用户 -->
    <el-dialog title="修改" :visible.sync="editDialogVisible" @close="resetForm('edit')">
      <el-form :model="editForm" :rules="addRules" ref="edit" label-width="100px">
        <el-form-item label="用户名" prop="username">{{ editForm.username }}
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="editForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email"></el-input>
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
  name: "UserView",
  data() {
    const validatePass = (rule, value, callback) => {
      if (value !== this.addForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    };
    const validateEmail = (rule, value, callback) => {
      if (value) {
        const email = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
        if (email.test(value)) {
          callback()
        } else {
          callback(new Error('邮箱格式不正确'))
        }
      } else {
        callback()
      }

    }
    const validatePhone = (rule, value, callback) => {
      if (value) {
        const phone = /^[9][0-9]{9}$/
        if (phone.test(value)) {
          callback()
        } else {
          callback(new Error('非ph手机不支持'))
        }
      } else {
        callback()
      }
    }
    return {
      search: '',
      addDialogVisible: false,
      editDialogVisible: false,
      addForm: {username: '', password: '', checkPass: '', phone: '', email: ''},
      editForm: {username: '', phone: '', email: '', id: ''},
      dataList: [],
      pagination: {page: 1, size: 20, total: 0},
      addRules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 3, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 6, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur'}
        ],
        checkPass: [
          {required: true, message: '请再次输入确认密码', trigger: 'blur'},
          {validator: validatePass, trigger: 'blur'}
        ],
        email: [
          {validator: validateEmail, trigger: 'blur'}
        ],
        phone: [
          {validator: validatePhone, trigger: 'blur'}
        ]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    resetForm(name) {
      this.$refs[name].resetFields()
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
      const {data: response} = await this.$http.get('users/mgt/',
          {params: {'page': this.pagination.page, 'size': this.pagination.size, 'search': this.search}})
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.dataList = response.results
      this.pagination = response.pagination
    },
    postAdd() {
      this.$refs["add"].validate(async (valid) => {
        if (valid) {
          const {data: response} = await this.$http.post('users/mgt/', this.addForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.addDialogVisible = false
          await this.getList()
        }
      })
    },
    handleEdit(row) {
      this.editForm.username = row.username
      this.editForm.phone = row.phone
      this.editForm.email = row.email
      this.editForm.id = row.id
      this.editDialogVisible = true
    },
    handleDel(id) {
      this.$msgbox.confirm('删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(async () => {
        const {data: response} = await this.$http.delete(`users/mgt/${id}/`)
        if (response.code) {
          return this.$message.error(response.message)
        }
        await this.getList()
      })
    },
    edit() {
      const {id} = this.editForm
      this.$refs['edit'].validate(async valid => {
        if (valid) {
          const {data: response} = await this.$http.patch(`users/mgt/${id}/`, this.editForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.editDialogVisible = false
          await this.getList()
        }
      })
    },
    async handleChange(row) {
      await this.$http.patch(`users/mgt/${row.id}/`, {
        is_active: row.is_active
      })
    }
  }
}
</script>

<style scoped>

</style>