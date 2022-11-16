<template>
  <el-container>
      <!--menu 缩放，根据isCollapsed 的布尔  -->
      <el-aside :width="isCollapsed ? '64px' : '200px'">
        <!--在el-menu中 :router="true" ，开启路由 一旦开启路由后，点击el-menu-item菜单项就会按照index跳转 -->
        <!--把 default-active 和 $route.path 关联 就会按照路径uri 菜单高亮 -->
        <el-menu
            router
            background-color="#1F2D3D"
            text-color="#BFCBD9"
            active-text-color="#409EFF"
            :collapse="isCollapsed"
            :default-active="$route.path"
        >
          <!-- v-for 生成menu -->
          <el-submenu :index="item.id + ''" v-for="item in menulist" :key="item.id">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>{{ item.name }}</span>
            </template>
            <el-menu-item :index="c.path" v-for="c in item.children" :key="c.id">{{ c.name }}</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
      <div class="logo">
<!--        <img src="../assets/img/head.jpeg" alt="logo"/>-->
<!--        <div class="title">Adm运维系统管理平台</div>-->
        <div>
          <i :class="isCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'" @click="isCollapsed = !isCollapsed"></i>
        </div>
      </div>
      <div class="info">
        <!--        <el-button type="info" @click="logout">退出</el-button>-->
        <el-dropdown @command="handleCommand">
          <span class="el-dropdown-link">{{ user.username }}<i class="el-icon-arrow-down el-icon--right"></i></span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="chpwd">修改密码</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <!-- 修改密码对话框 -->
      <el-dialog title="修改密码" :visible.sync="chpwdDialogVisible" @close="resetForm">
        <el-form :model="chpwdForm" :rules="chpwdRules" ref="chpwd" label-width="100px">
          <el-form-item label="用户名">{{ user.username }}</el-form-item>
          <el-form-item label="旧密码" prop="oldPassword">
            <el-input type="password" v-model="chpwdForm.oldPassword"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="password">
            <el-input type="password" v-model="chpwdForm.password"></el-input>
          </el-form-item>
          <el-form-item label="确认新密码" prop="checkPass">
            <el-input type="password" v-model="chpwdForm.checkPass"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="chpwdDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="changePassword">确 定</el-button>
        </span>
      </el-dialog>
    </el-header>
        <el-main>
        <!-- 子路由嵌套 -->
        <router-view></router-view>
      </el-main>
      </el-container>
    </el-container>
</template>

<script>
export default {
  name: "HomeView.vue",
  data() {
    const validatePass = (rule, value, callback) => {
      if (value !== this.chpwdForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    };
    return {
      menulist: [],
      user: {},
      isCollapsed: false,
      chpwdDialogVisible: false,
      chpwdForm: {},
      chpwdRules: {
        oldPassword: [
          {required: true, message: '请输入旧密码', trigger: 'blur'},
          {min: 6, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入新密码', trigger: 'blur'},
          {min: 6, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur'}
        ],
        checkPass: [
          {required: true, message: '请输入新密码', trigger: 'blur'},
          {validator: validatePass, trigger: 'blur'}
        ]
      },
    }
  },
  created() {
    this.getMenuList()
    this.getUserInfo()
  },
  methods: {
    logout() {
      window.localStorage.removeItem('token')
      this.$router.push('/login')
    },
    async getMenuList() {
      const {data: response} = await this.$http.get('users/meta/menulist/')
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.menulist = response // 菜单项数组
    },
    async getUserInfo() {
      const {data: response} = await this.$http.get('users/meta/whoami/')
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.user = response.user
    },
    handleCommand(command) {
      if (command === 'logout') {
        this.logout()
      } else if (command === 'chpwd') {
        this.chpwdDialogVisible = true
      }
    },
    changePassword() {
      this.$refs.chpwd.validate(async (valid) => {
        if (valid) {
          const {data: response} = await
              this.$http.post(`users/meta/chpwd/`, this.chpwdForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.chpwdDialogVisible = false
          this.$message('密码修改成功')
        }
      })
    },
    resetForm() {
      this.$refs.chpwd.resetFields()
    },
  }
}
</script>

<style lang="less" scoped>
.el-container {
  background-color: #fff;
  height: 100%;
}

.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 5px;

  .logo {
    display: flex;
    align-items: center;

    img {
      width: 40px;
    }

    .title {
      font-size: 20px;
      margin-left: 5px;
    }

    i {
      font-size: 25px;
      margin-left: 5px;
    }
  }
}

.el-aside {
  background-color: #304156;
}

.el-main {
  background-color: #f0f2f4;
}

.el-menu {
  border-right: none; // 消除菜单右侧白线
}
</style>