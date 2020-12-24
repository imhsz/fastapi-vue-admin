import Cookies from 'js-cookie'

const TokenKey = 'access_token'
const OperatorKey = 'Operator'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function setOperator(username) {
  return Cookies.set(OperatorKey, username)
}

export function getOperator() {
  return Cookies.get(OperatorKey)
}
