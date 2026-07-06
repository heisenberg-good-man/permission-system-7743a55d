<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>个人中心</h1>
      <p>管理您的账户信息</p>
    </div>
    <div class="profile-container">
      <div class="left-panel">
        <div class="avatar-section">
          <div class="avatar">👤</div>
          <div class="user-name">张三</div>
          <div class="user-role">候选人</div>
        </div>
        <nav class="side-nav">
          <div class="nav-item active">基本信息</div>
          <div class="nav-item">简历管理</div>
          <div class="nav-item">投递记录</div>
          <div class="nav-item">消息通知</div>
          <div class="nav-item">账户设置</div>
        </nav>
      </div>
      <div class="right-panel">
        <div class="tab-content">
          <div class="section-card">
            <h3>基本信息</h3>
            <form class="info-form">
              <div class="form-row">
                <div class="form-group">
                  <label>姓名</label>
                  <input type="text" value="张三" />
                </div>
                <div class="form-group">
                  <label>邮箱</label>
                  <input type="email" value="zhangsan@example.com" />
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>手机号</label>
                  <input type="tel" value="13800138001" />
                </div>
                <div class="form-group">
                  <label>学历</label>
                  <select>
                    <option>本科</option>
                    <option>硕士</option>
                    <option>大专</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>工作经验</label>
                <select>
                  <option>3年</option>
                  <option>1-3年</option>
                  <option>3-5年</option>
                </select>
              </div>
              <div class="form-group">
                <label>自我介绍</label>
                <textarea rows="4">热爱技术，对前端开发有浓厚兴趣，具有良好的团队合作精神。</textarea>
              </div>
              <button type="submit" class="btn-save">保存修改</button>
            </form>
          </div>
          <div class="section-card">
            <h3>快捷操作</h3>
            <div class="quick-actions">
              <div class="action-item" @click="$router.push('/jobs')">
                <div class="action-icon">🔍</div>
                <div class="action-text">搜索职位</div>
              </div>
              <div class="action-item" @click="$router.push('/applications')">
                <div class="action-icon">📋</div>
                <div class="action-text">查看投递</div>
              </div>
              <div class="action-item">
                <div class="action-icon">📝</div>
                <div class="action-text">编辑简历</div>
              </div>
              <div class="action-item">
                <div class="action-icon">🔔</div>
                <div class="action-text">消息通知</div>
              </div>
            </div>
          </div>
          <div class="section-card">
            <h3>预留功能</h3>
            <div class="reserved-features">
              <div class="reserved-item">
                <span class="feature-icon">🔐</span>
                <span>登录注册 - 预留入口</span>
              </div>
              <div class="reserved-item">
                <span class="feature-icon">💳</span>
                <span>会员支付 - 预留入口</span>
              </div>
              <div class="reserved-item">
                <span class="feature-icon">🤖</span>
                <span>智能匹配 - 预留入口</span>
              </div>
              <div class="reserved-item">
                <span class="feature-icon">📊</span>
                <span>简历评分 - 预留入口</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.profile-page {
  padding: 20px 0;
}
.page-header {
  margin-bottom: 32px;
}
.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}
.page-header p {
  font-size: 16px;
  color: #999;
}
.profile-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
}
.left-panel {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.avatar-section {
  text-align: center;
  padding-bottom: 24px;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}
.avatar {
  font-size: 64px;
  margin-bottom: 12px;
}
.user-name {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 4px;
}
.user-role {
  font-size: 14px;
  color: #667eea;
}
.side-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.nav-item {
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}
.nav-item:hover {
  background: #f5f5f5;
}
.nav-item.active {
  background: #f0f5ff;
  color: #667eea;
  font-weight: 500;
}
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.section-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.section-card h3 {
  font-size: 18px;
  margin-bottom: 20px;
}
.info-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.form-group label {
  font-size: 14px;
  font-weight: 500;
}
.form-group input, .form-group select, .form-group textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
.form-group textarea {
  resize: vertical;
}
.btn-save {
  align-self: flex-end;
  padding: 12px 32px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #fafafa;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}
.action-item:hover {
  transform: translateY(-2px);
}
.action-icon {
  font-size: 32px;
  margin-bottom: 8px;
}
.action-text {
  font-size: 14px;
  color: #666;
}
.reserved-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.reserved-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #fff8e1;
  border-radius: 8px;
  font-size: 14px;
  color: #8d6e63;
}
.feature-icon {
  font-size: 20px;
}
</style>