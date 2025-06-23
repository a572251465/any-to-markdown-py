
# Vue3应用发布平台开发指南

## 项目初始化配置

### 1. Vite配置文件 (vite.config.js)

```javascript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],
  
  // ✅ 关键配置：支持动态base路径
  base: process.env.NODE_ENV === 'production' 
    ? (process.env.VITE_APP_BASE_URL || './') 
    : '/',
  
  // ✅ 路径别名配置
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@views': resolve(__dirname, 'src/views'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@api': resolve(__dirname, 'src/api')
    }
  },
  
  // ✅ 构建配置
  build: {
    // 输出目录
    outDir: 'dist',
    
    // 静态资源目录
    assetsDir: 'assets',
    
    // ⚠️ 重要：确保资源路径正确
    rollupOptions: {
      output: {
        // 分包策略 - 避免单文件过大
        manualChunks: {
          'vendor-vue': ['vue', 'vue-router', 'pinia'],
          'vendor-ui': ['element-plus', '@element-plus/icons-vue'],
          'vendor-utils': ['axios', 'dayjs', 'lodash-es']
        },
        
        // 文件命名 - 包含hash避免缓存问题
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.');
          const extType = info[info.length - 1];
          
          if (/\.(png|jpe?g|gif|svg|webp)(\?.*)?$/i.test(assetInfo.name)) {
            return `assets/images/[name]-[hash][extname]`;
          }
          if (/\.(woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name)) {
            return `assets/fonts/[name]-[hash][extname]`;
          }
          if (/\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/i.test(assetInfo.name)) {
            return `assets/media/[name]-[hash][extname]`;
          }
          
          return `assets/${extType}/[name]-[hash][extname]`;
        }
      }
    },
    
    // 压缩配置
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  
  // ✅ 开发服务器配置
  server: {
    port: 3000,
    open: true,
    
    // 代理配置 - 开发时使用
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  }
});
```

### 2. 路由配置 (router/index.js)

```javascript
import { createRouter, createWebHistory } from 'vue-router';

// ✅ 动态获取base路径的函数
function getBasePath() {
  if (process.env.NODE_ENV === 'development') {
    return '/';
  }
  
  // 生产环境：从环境变量获取或自动推断
  if (import.meta.env.VITE_APP_BASE_URL) {
    return import.meta.env.VITE_APP_BASE_URL;
  }
  
  // 自动推断：从当前URL中提取项目和场景路径
  const path = window.location.pathname;
  const segments = path.split('/').filter(Boolean);
  
  if (segments.length >= 2) {
    // 假设URL格式为 /project/scene/...
    return `/${segments[0]}/${segments[1]}/`;
  }
  
  return '/';
}

const router = createRouter({
  // ✅ 使用动态base路径
  history: createWebHistory(getBasePath()),
  
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/dashboard',
      name: 'Dashboard', 
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/Profile.vue'),
      meta: { requiresAuth: true }
    },
    // ✅ 404页面必须配置
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue')
    }
  ]
});

// ✅ 路由守卫 - 权限检查
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 需要权限但未登录，重定向到登录页面
    const currentPath = window.location.pathname;
    window.location.href = `/admin/login?redirect=${encodeURIComponent(currentPath)}`;
    return;
  }
  
  next();
});

export default router;
```

### 3. 环境变量配置

#### .env.development
```bash
# 开发环境配置
VITE_APP_TITLE=开发环境
VITE_APP_BASE_URL=/
VITE_APP_API_BASE_URL=http://localhost:8080/api
VITE_APP_UPLOAD_URL=http://localhost:8080/api/upload
```

#### .env.production
```bash
# 生产环境配置（部署时会被动态替换）
VITE_APP_TITLE=生产环境
VITE_APP_BASE_URL=./
VITE_APP_API_BASE_URL=/api
VITE_APP_UPLOAD_URL=/api/upload
```

#### env.d.ts (TypeScript项目)
```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string;
  readonly VITE_APP_BASE_URL: string;
  readonly VITE_APP_API_BASE_URL: string;
  readonly VITE_APP_UPLOAD_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## API请求配置

### 4. HTTP请求封装 (utils/request.js)

```javascript
import axios from 'axios';

// ✅ 动态API base URL
function getApiBaseUrl() {
  if (process.env.NODE_ENV === 'development') {
    return import.meta.env.VITE_APP_API_BASE_URL || 'http://localhost:8080/api';
  }
  
  // 生产环境使用相对路径
  return import.meta.env.VITE_APP_API_BASE_URL || '/api';
}

// 创建axios实例
const request = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// ✅ 请求拦截器 - 自动添加token
request.interceptors.request.use(
  (config) => {
    // 从多个位置尝试获取token
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    console.error('请求拦截器错误:', error);
    return Promise.reject(error);
  }
);

// ✅ 响应拦截器 - 统一错误处理
request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API请求错误:', error);
    
    if (error.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 401:
          // 权限过期，清除token并跳转登录
          clearAuthToken();
          const currentPath = window.location.pathname;
          window.location.href = `/admin/login?redirect=${encodeURIComponent(currentPath)}`;
          break;
          
        case 403:
          ElMessage.error('权限不足');
          break;
          
        case 404:
          ElMessage.error('请求的资源不存在');
          break;
          
        case 500:
          ElMessage.error('服务器内部错误');
          break;
          
        default:
          ElMessage.error(data?.message || '请求失败');
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接');
    } else {
      ElMessage.error('请求配置错误');
    }
    
    return Promise.reject(error);
  }
);

// ✅ Token管理函数
function getAuthToken() {
  // 优先从URL参数获取（首次访问）
  const urlParams = new URLSearchParams(window.location.search);
  const urlToken = urlParams.get('token');
  
  if (urlToken) {
    // 保存到localStorage并清理URL
    localStorage.setItem('authToken', urlToken);
    const url = new URL(window.location);
    url.searchParams.delete('token');
    window.history.replaceState({}, '', url);
    return urlToken;
  }
  
  // 从localStorage获取
  return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
}

function clearAuthToken() {
  localStorage.removeItem('authToken');
  sessionStorage.removeItem('authToken');
}

export default request;
```

## 状态管理配置

### 5. Pinia Store配置 (stores/auth.js)

```javascript
import { defineStore } from 'pinia';
import request from '@/utils/request';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    permissions: [],
    isAuthenticated: false
  }),
  
  actions: {
    // ✅ 应用启动时初始化权限
    async initAuth() {
      try {
        const token = this.getTokenFromUrl() || this.getTokenFromStorage();
        
        if (!token) {
          this.redirectToLogin();
          return false;
        }
        
        // 验证token有效性
        const userInfo = await request.get('/auth/user-info');
        
        this.user = userInfo.user;
        this.permissions = userInfo.permissions;
        this.token = token;
        this.isAuthenticated = true;
        
        // 保存token到localStorage
        localStorage.setItem('authToken', token);
        
        return true;
      } catch (error) {
        console.error('权限初始化失败:', error);
        this.clearAuth();
        this.redirectToLogin();
        return false;
      }
    },
    
    getTokenFromUrl() {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get('token');
      
      if (token) {
        // 清理URL参数
        const url = new URL(window.location);
        url.searchParams.delete('token');
        window.history.replaceState({}, '', url);
      }
      
      return token;
    },
    
    getTokenFromStorage() {
      return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    },
    
    clearAuth() {
      this.user = null;
      this.token = null;
      this.permissions = [];
      this.isAuthenticated = false;
      localStorage.removeItem('authToken');
      sessionStorage.removeItem('authToken');
    },
    
    redirectToLogin() {
      const currentPath = window.location.pathname + window.location.search;
      window.location.href = `/admin/login?redirect=${encodeURIComponent(currentPath)}`;
    },
    
    hasPermission(permission) {
      return this.permissions.includes(permission);
    }
  }
});
```

## 应用初始化

### 6. main.js配置

```javascript
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

import App from './App.vue';
import router from './router';
import { useAuthStore } from '@/stores/auth';

// ✅ 全局错误处理
window.addEventListener('error', (event) => {
  console.error('全局错误:', event.error);
  
  // 发送错误报告到后端（可选）
  if (import.meta.env.PROD) {
    fetch('/api/errors/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: event.error?.message,
        stack: event.error?.stack,
        url: window.location.href,
        timestamp: new Date().toISOString()
      })
    }).catch(console.error);
  }
});

// 创建应用实例
const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(ElementPlus);

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// ✅ 权限初始化后再挂载应用
async function initApp() {
  try {
    const authStore = useAuthStore();
    
    // 初始化权限
    await authStore.initAuth();
    
    // 使用路由
    app.use(router);
    
    // 挂载应用
    app.mount('#app');
    
    console.log('应用初始化成功');
  } catch (error) {
    console.error('应用初始化失败:', error);
    
    // 显示错误页面或重定向到登录
    document.body.innerHTML = `
      <div style="text-align: center; padding: 50px;">
        <h2>应用加载失败</h2>
        <p>请刷新页面重试，或联系管理员</p>
        <button onclick="window.location.reload()">刷新页面</button>
      </div>
    `;
  }
}

initApp();
```

## 静态资源处理

### 7. 静态资源引用规范

```javascript
// ✅ 正确的图片引用方式
// 方式1：使用import（推荐）
import logoImg from '@/assets/images/logo.png';

// 在模板中使用
<template>
  <img :src="logoImg" alt="Logo" />
</template>

// 方式2：使用new URL（动态引用）
function getImageUrl(name) {
  return new URL(`/src/assets/images/${name}`, import.meta.url).href;
}

// ❌ 错误的引用方式
// 不要直接使用相对路径字符串
<img src="./assets/images/logo.png" alt="Logo" />
```

### 8. CSS中的资源引用

```css
/* ✅ 正确的CSS资源引用 */
.background {
  /* 使用相对路径，Vite会自动处理 */
  background-image: url('@/assets/images/bg.jpg');
}

.icon {
  /* 字体图标 */
  background-image: url('@/assets/fonts/icons.woff2');
}

/* ❌ 避免使用绝对路径 */
.wrong {
  background-image: url('/src/assets/images/bg.jpg');
}
```

## 调试和测试

### 9. 本地调试配置

```javascript
// utils/debug.js
export const DEBUG = {
  // 当前环境信息
  env: import.meta.env.MODE,
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
  
  // 路径信息
  basePath: import.meta.env.BASE_URL,
  apiBase: import.meta.env.VITE_APP_API_BASE_URL,
  
  // 调试函数
  log: (...args) => {
    if (import.meta.env.DEV) {
      console.log('[DEBUG]', ...args);
    }
  },
  
  // 路径测试
  testPaths() {
    console.log('=== 路径调试信息 ===');
    console.log('Base URL:', import.meta.env.BASE_URL);
    console.log('Current URL:', window.location.href);
    console.log('API Base:', import.meta.env.VITE_APP_API_BASE_URL);
    console.log('Router Base:', this.$router?.options?.history?.base);
  }
};

// 开发环境下暴露到全局
if (import.meta.env.DEV) {
  window.DEBUG = DEBUG;
}
```

### 10. 构建前检查脚本

```json
// package.json
{
  "scripts": {
    "dev": "vite",
    "build": "npm run type-check && vite build",
    "preview": "vite preview",
    "type-check": "vue-tsc --noEmit",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix",
    
    "pre-build": "npm run lint && npm run type-check",
    "build:check": "npm run pre-build && vite build && npm run post-build",
    "post-build": "node scripts/build-check.js"
  }
}
```

```javascript
// scripts/build-check.js
import fs from 'fs';
import path from 'path';

console.log('🔍 检查构建结果...');

const distPath = path.resolve('dist');
const indexPath = path.join(distPath, 'index.html');

// 检查关键文件是否存在
const requiredFiles = ['index.html', 'assets'];
for (const file of requiredFiles) {
  const filePath = path.join(distPath, file);
  if (!fs.existsSync(filePath)) {
    console.error(`❌ 缺少关键文件: ${file}`);
    process.exit(1);
  }
}

// 检查index.html中的资源路径
if (fs.existsSync(indexPath)) {
  const htmlContent = fs.readFileSync(indexPath, 'utf-8');
  
  // 检查是否包含绝对路径（可能导致部署问题）
  if (htmlContent.includes('src="/') && !htmlContent.includes('src="./')) {
    console.warn('⚠️  index.html中可能包含绝对路径，请检查base配置');
  }
  
  console.log('✅ 构建检查通过');
} else {
  console.error('❌ index.html文件不存在');
  process.exit(1);
}
```

## 部署前检查清单

### 11. 部署检查清单

```markdown
## 🚀 部署前检查清单

### 基础配置
- [ ] vite.config.js中base配置为相对路径 `./`
- [ ] 路由使用createWebHistory且base路径动态获取
- [ ] 环境变量正确配置
- [ ] API请求使用相对路径

### 权限集成
- [ ] 应用启动时正确初始化权限
- [ ] Token从URL参数和localStorage正确获取
- [ ] 401/403错误正确处理并跳转登录

### 资源引用
- [ ] 图片使用import或new URL方式引用
- [ ] CSS中使用相对路径引用资源
- [ ] 字体文件路径正确

### 路由配置
- [ ] 配置了404页面
- [ ] 路由守卫正确实现
- [ ] 深层路由可以直接访问

### 构建优化
- [ ] 代码分割配置合理
- [ ] 生产环境移除console.log
- [ ] 文件名包含hash避免缓存问题

### 测试验证
- [ ] 本地build后预览正常
- [ ] 不同路由直接访问正常
- [ ] API请求正常
- [ ] 权限验证正常
```

## 常见问题排查

### 12. 问题排查指南

```javascript
// utils/diagnostics.js
export function runDiagnostics() {
  console.log('=== 应用诊断信息 ===');
  
  // 环境信息
  console.log('环境:', import.meta.env.MODE);
  console.log('Base URL:', import.meta.env.BASE_URL);
  console.log('API Base:', import.meta.env.VITE_APP_API_BASE_URL);
  
  // 当前路径信息
  console.log('当前URL:', window.location.href);
  console.log('路径名:', window.location.pathname);
  console.log('搜索参数:', window.location.search);
  
  // Token信息
  const token = localStorage.getItem('authToken');
  console.log('Token存在:', !!token);
  console.log('Token长度:', token?.length || 0);
  
  // 路由信息
  console.log('路由器配置:', window.__VUE_DEVTOOLS_GLOBAL_HOOK__?.Vue?.config || 'N/A');
  
  // 网络检查
  fetch('/api/health')
    .then(() => console.log('✅ API连接正常'))
    .catch(() => console.log('❌ API连接失败'));
}

// 开发环境下暴露诊断函数
if (import.meta.env.DEV) {
  window.runDiagnostics = runDiagnostics;
}
```

遵循这些规范和配置，您的Vue3应用就能在发布平台上稳定运行！关键是要确保路径配置正确、权限集成到位、资源引用规范。
