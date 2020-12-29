<template>
  <div class="app-container">
    <div class="search">
      <el-input v-model="search" style="width: 20%;float: right;margin-right: 5%" placeholder="请输入搜索内容" prefix-icon="el-icon-search" @change="searchDetail" />
    </div>
    <el-table
      v-loading="listLoading"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
      :data="records"
      border
      highlight-current-row
    >
      <el-table-column type="index" :index="indexMethod" width="50" />
      <el-table-column label="操作对象" prop="operate_object" width="100" />
      <el-table-column
        label="操作类型"
        prop="operate_type"
        width="100"
        :filters="filterTypes"
        :filter-method="typeHandler"
        filter-placement="bottom-end"
      >
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.operate_type ==='新增'?'success':scope.row.operate_type==='删除'?'danger':'warning' "
            disable-transitions
          >{{ scope.row.operate_type }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="详情" prop="operate_detail" width="800">
        <template slot-scope="scope">
          {{ scope.row.operate_detail|Detail }}
        </template>
      </el-table-column>
      <el-table-column label="操作用户" prop="operate_username" width="100" />
      <el-table-column label="操作IP" prop="operate_ip" width="100" />
      <el-table-column label="操作时间" width="200">
        <template slot-scope="scope">
          {{ scope.row.operate_time|Time }}
        </template>
      </el-table-column>
    </el-table>
    <div class="block">
      <el-pagination
        class="mt-20 text-right"
        align="right"
        :hide-on-single-page="hidePage"
        background
        layout="total,sizes,prev,pager,next,jumper"
        :current-page.sync="pagination.currentPage"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { getRecords } from '@/api/record'
export default {
  filters: {
    Time(value) {
      // 时间格式的转换
      const dateExchange = new Date(value).toJSON()
      return new Date(+new Date(dateExchange) + 8 * 3600 * 1000).toISOString().replace(/T/g, ' ').replace(/\.[\d]{3}Z/, '')
    },
    Detail(value) {
      // 修改详情展示
      if (value === '') {
        return value
      }
      const detail = JSON.parse(value)
      if (detail.length >= 1) {
        // 说明是修改数据
        let totalDetail = ''
        // 数据格式化
        for (let i = 0; i < detail.length; i++) {
          totalDetail += detail[i].name + ':' + ' ' + detail[i].old + ' ' + '=>' + ' ' + detail[i].new + '\n'
        }
        return totalDetail
      } else {
        // 说明是新增或删除数据
        let totalDetail = ''
        // 数据格式化
        for (const i in detail) {
          totalDetail += i + ':' + ' ' + detail[i] + '\n'
        }
        return totalDetail
      }
    }
  },
  data() {
    return {
      listLoading: true,
      records: [],
      hidePage: false,
      pagination: {
        currentPage: 1,
        total: 0,
        pageSize: 10
      },
      filterTypes: [{ text: '新增', value: '新增' }, { text: '修改', value: '修改' }, { text: '删除', value: '删除' }],
      search: ''
    }
  },
  created() {
    this.loadRecords(this.search)
  },
  methods: {
    loadRecords(searchInfo) {
      // 初始化数据
      this.listLoading = true
      const { pagination } = this
      getRecords(pagination.currentPage, pagination.pageSize, searchInfo).then(response => {
        this.records = response.records
        this.listLoading = false
        pagination.total = response.total
      })
    },
    handlePageChange() {
      // table改变, 重新加载数据
      this.loadRecords(this.search)
    },
    handleSizeChange(newPageSize) {
      // 页数大小改变
      const { pagination } = this
      pagination.pageSize = newPageSize
      this.handlePageChange(pagination.currentPage = 1)
    },
    indexMethod(index) {
      // 索引改变
      return index + (this.pagination.currentPage - 1) * this.pagination.pageSize + 1
    },
    typeHandler(value, row) {
      return row.operate_type === value
    },
    searchDetail() {
      this.loadRecords(this.search)
    }
  }
}
</script>
<style>
  .el-table .cell {
    white-space: pre-line;
  }
</style>
