<template>
  <div class="app-container">
    <el-table :data="corglist" border style="width: 100%" row-key="id" default-expand-all :tree-props:="{children: 'children', hasChildren: 'haschildren'}"><!-- :data="用于存放请求数据回来的数组"  -->
      <el-table-column type="index" width="50" />
      <el-table-column prop="corg_name" label="部门名称" width="200" />
      <el-table-column prop="idx" label="排序" align="center" width="50" />
      <el-table-column prop="create_time" label="创建时间" align="center" width="250" />
      <el-table-column prop="remarks" label="备注" align="center" width="150" />
      <el-table-column
        label="状态"
        :filters="[{ text: '已激活', value: '已激活' }, { text: '未激活', value: '未激活' }]"
        :filter-method="filterTag"
        filter-placement="bottom-end"
        align="center"
        width="200">
        <template slot-scope="scope">
          <el-tag :type="scope.row.state === true ? 'primary' : 'danger'" disable-transitions>{{ scope.row.state === true ? '已激活':'未激活' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
          >编辑
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-add"
            @click="handleAdd(scope.row)"
          >新增
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :title="title" :visible.sync="dialogFormedit">
      <el-form ref="corgForm" :model="corg" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="24">
            <el-form-item label="上级部门" prop="parent_id">
              <Treeselect v-if="!isEdit" v-model="corg.parent_id" :options="corgOptions" :normalizer="normalizer" :show-count="true" placeholder="选择上级部门" />
              <el-input v-else v-model="corg.parent_name" placeholder="请输入部门名称" disabled="disabled" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门名称" prop="corg_name">
              <el-input v-model="corg.corg_name" placeholder="请输入部门名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="备注" prop="remarks">
              <el-input v-model="corg.remarks" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="排序" prop="idx">
              <el-input v-model="corg.idx" placeholder="请输入排序" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="state">
              <el-switch
                v-model="corg.state"
                active-color="#00A854"
                inactive-color="#ff4949"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="diaglog-footer">
        <el-button @click="dialogFormedit = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getCorgList, getCorgInfo, createCorg } from '@/api/corg'
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

export default {
  components: { Treeselect },
  data() {
    return {
      loading: true,
      corglist: [],
      corgOptions: [],
      title: '',
      isEdit: false,
      dialogFormedit: false,
      corg: {},
      state: '1',
      rules: {
        parent_id: [
          { required: true, message: '上级部门不能为空', trigger: 'blur' }
        ],
        corg_name: [
          { required: true, message: '部门名称不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getlist()
  },
  methods: {
    getlist() {
      this.loading = true
      getCorgList().then(response => {
        this.corglist = response.data
        this.listloading = false
      })
    },
    normalizer(node) {
      if (node.children && !node.children.length) {
        delete node.children
      }
      return {
        id: node.id,
        label: node.corg_name,
        children: node.children
      }
    },
    getTreeSelect() {
      getCorgList().then(response => {
        this.corgOptions = response.data
      })
    },
    filterTag(value, row) {
      if (value === '已激活') {
        return row.state === true
      } else {
        return row.state === false
      }
    },
    reset() {
      this.corg = {
        id: undefined,
        parent_id: undefined,
        corg_name: undefined,
        idx: undefined,
        remarks: undefined,
        state: true
      }
    },
    handleAdd(row) {
      this.title = '添加部门'
      this.dialogFormedit = true
      this.reset()
      this.getTreeSelect()
      if (row !== undefined) {
        this.corg.parent_id = row.id
      }
      this.isEdit = false
      this.open = true
    },
    handleUpdate(row) {
      this.dialogFormedit = true
      getCorgInfo({ corg_id: row.id }).then(response => {
        this.corg = response.data
        this.title = '修改部门'
        this.isEdit = true
      })
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs['corgForm'].validate(valid => {
        if (valid) {
          createCorg(this.corg).then(response => {
            if (response.code === 200) {
              this.dialogFormedit = false
              this.getlist()
            } else {
              this.msgError(response.message)
            }
          })
        }
      })
    }
  }
}
</script>
