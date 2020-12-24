import request from '@/utils/request'

export function getRecords(pageNo, pageSize, searchInfo) {
  return request({
    url: '/record/all_records',
    method: 'get',
    params: { page_no: pageNo,
      page_size: pageSize,
      search_info: searchInfo }
  })
}
