<template>
  <div class="app-container">
    <el-form ref="editSelf" :model="editSelf" :rule="editRules">
      <el-form-item label="邮箱" prop="email" label-width="40%">
        <el-input v-model="editSelf.email" autocomplete="off" style="width: 400px" />
      </el-form-item>
      <el-form-item label="昵称" prop="nick_name" label-width="40%">
        <el-input v-model="editSelf.nick_name" style="width: 400px" />
      </el-form-item>
      <el-form-item label="密码" prop="password" label-width="40%">
        <el-input v-model="editSelf.password" show-password placeholder="不修改密码无需填写" style="width: 400px" />
      </el-form-item>
    </el-form>
    <div slot="footer" style="margin-left: 70%">
      <el-button type="primary" round @click="postEditSelf">确 定</el-button>
      <el-button type="info" round @click="cancel">取 消</el-button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    const checkEmail = (rule, value, callback) => {
      const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      if (!value) {
        return callback(new Error('邮箱不能为空'))
      }
      setTimeout(() => {
        if (mailReg.test(value)) {
          callback()
        } else {
          callback(new Error('请输入正确的邮箱格式'))
        }
      }, 100)
    }
    return {
      editSelf: {
        email: '',
        nick_name: '',
        password: '',
        avatar: ''
      },
      editRules: {
        email: [
          { required: true, message: '请输入email', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }
        ],
        password: [
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ],
        nick_name: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.$store.dispatch('user/getInfo').then((data) => {
      this.editSelf = data
    })
  },
  methods: {
    cancel() {
      this.$router.go(-1)
    },
    postEditSelf() {
      this.$store.dispatch('user/editSelf', this.editSelf).then(() => {
        this.$message({
          message: '用户信息修改成功',
          type: 'success'
        })
      }).catch(() => {
        this.listLoading = false
      })
    }
  }
}
</script>
