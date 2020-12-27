<template>
  <div class="dashboard-container">
    <div class="dashboard-text">Hi, {{ name }}</div>
    <div><h3>{{ tipMessage }}</h3></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      tipMessage: '早上好,来杯☕️吧～'
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
