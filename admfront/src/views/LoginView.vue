<template>
  <div class="login_container">
    <div class="login_box">
      <div class="avatar_box">
        <img src="../assets/img/logo.png" alt="logo"/>
      </div>
      <el-form class="login_form" :rules="loginRules" :model="loginForm" ref="loginFormRef">
        <el-form-item>
          <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="el-icon-user"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-input
              type="password"
              v-model="loginForm.password"
              placeholder="请输入密码"
              prefix-icon="el-icon-s-custom"
              @keyup.enter.native="login"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="login">登录</el-button>
          <el-button type="info" @click="resetLoginForm">重制</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginView.vue",
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 3, max: 16, message: '长度在 3 到 10 个字符', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 6, max: 16, message: '长度在 6 到 16 个字符', trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    resetLoginForm() {
      this.$refs.loginFormRef.resetFields() // Form的resetFields方法重置
    },
    login() {
      this.$refs.loginFormRef.validate(async (valid) => {
        if (valid) {
          const { data: response } = await this.$http.post('login/', this.loginForm)
          // data:{access: '', ...} 解构出来 把data的值解给response
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.$message('登录成功')
          window.localStorage.setItem('token', response.access)
          await this.$router.push('/home')
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.login_container {
  background-color: #2b4b6b;
  height: 100%;
}

.login_box {
  width: 450px;
  height: 300px;
  background-color: #fff;
  border-radius: 5px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  .avatar_box {
    height: 130px;
    width: 130px;
    padding: 10px;
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);

    img {
      width: 100%;
      height: 100%;
      border-radius: 35%;
    }
  }

  .login_form {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
  }
}
</style>