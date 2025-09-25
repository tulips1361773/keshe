<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user'
import { onMounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const userStore = useUserStore()
    
    onMounted(async () => {
      // 初始化认证状态
      await userStore.initializeAuth()
    })
    
    return {}
  }
}
</script>

<style>
#app {
  min-height: 100vh;
}
</style>