<template>
<el-tree
          class="tree-tap"
          :data="deaplist"
          show-checkbox
          node-key="deptid"
          ref="treeForm"
          check-strictly
          :check-on-click-node="true"
          :props="defaultProps"
          @check-change="handleNodeClick"
        ></el-tree>

</template>
<script>
export default {
  data() {
    return {
      deaplist: [{
        deptname: '第十一监察检查室', deptid: 1, children: [
          { deptname: '第十2监察检查室', deptid: 2 },
          { deptname: '第十3监察检查室', deptid: 3 }
        ] },
      {
        deptname: '第十4监察检查室', deptid: 4, children: [
          { deptname: '第十5监察检查室', deptid: 5 },
          { deptname: '第十6监察检查室', deptid: 6 }
        ] }],
      // deaplist1: [{deptname: '第十一监察检查室'},{deptname: '驻苏州银行组'}...
      defaultProps: {
        label: 'deptname',
        id: 'deptid'
      }
    }
  },
  methods:
    {
      handleNodeClick(data, checked, node) {
        if (checked) {
          console.log(data.deptid)
          this.$refs.treeForm.setCheckedKeys([data.deptid])
        }
      }

    }
}
</script>

