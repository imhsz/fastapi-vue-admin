import request from '@/utils/request'

export function getCorgList(query) {
  return request({
    url: '/corg/list',
    method: 'get',
    params: query
  })
}

// 查询部门详细
export function getCorgInfo(data) {
  return request({
    url: '/corg/corg_info',
    method: 'get',
    params: data
  })
}
// 修改部门
export function editcorg(data) {
  return request({
    url: '/corg/edit',
    method: 'post',
    params: data
  })
}

export function createCorg(data) {
  return request({
    url: '/corg/create',
    method: 'post',
    data: data
  })
}

