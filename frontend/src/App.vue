<template>
  <div class="app">
    <header class="header">
      <div class="header-content">
        <div class="logo" @click="$router.push('/')">招聘平台</div>
        <nav class="nav">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/jobs" class="nav-link">职位列表</router-link>
          <router-link to="/jobs/create" class="nav-link">发布职位</router-link>
          <router-link to="/jobs/manage" class="nav-link">管理职位</router-link>
          <router-link to="/applications" class="nav-link">投递记录</router-link>
          <router-link to="/candidates" class="nav-link">候选人管理</router-link>
          <router-link to="/interviews" class="nav-link">面试管理</router-link>
          <router-link to="/offers" class="nav-link">Offer管理</router-link>
          <router-link to="/profile" class="nav-link">个人中心</router-link>
        </nav>
      </div>
    </header>
    <main class="main">
      <router-view></router-view>
    </main>
    <footer class="footer">
      <div class="footer-content">招聘平台 © 2026</div>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
}
.nav {
  display: flex;
  gap: 24px;
}
.nav-link {
  color: rgba(255,255,255,0.9);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}
.nav-link:hover {
  color: white;
}
.nav-link.router-link-active {
  color: white;
  font-weight: 500;
}
.main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 20px;
}
.footer {
  background: #333;
  color: #999;
  padding: 20px 0;
  text-align: center;
  font-size: 14px;
}
</style>