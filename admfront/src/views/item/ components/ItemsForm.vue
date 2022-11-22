<template>
  <div>
    <el-form :model="addForm" :rules="addRules" ref="add" label-width="100px">
      <el-form-item label="用户名" prop="item_name">
        <el-input v-model="addForm.item_name"></el-input>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "ItemsForm",
  props:['editForm'],
  data() {
    return {
      addForm: {item_name: ''},
      addRules: {
        item_name: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 1, max: 16, message: '长度在 1 到 16 个字符', trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    submitForm() {
      let flag = null
      this.$refs['add'].validate(valid => {
        flag = !!valid;
      })
      return flag
    },
    resetForm() {
      this.$refs['add'].resetFields()
    }
  },
  // watch: {
  //   editForm: {
  //     handler(newVal, oldVal){
  //       console.log(oldVal)
  //       console.log(newVal)
  //
  //     },
  //     immediate: true, //immediate:true代表如果在 wacth 里声明了之后，就会立即先去执行里面的handler方法，如果为 false，不会在绑定的时候就执行。
  //     deep: true //deep，默认值是 false，代表是否深度监听。
  //   }
  // },
  created() {
    if (this.editForm !== undefined){
      this.addForm = this.editForm
    }
  }
}
</script>

<style scoped>

</style>