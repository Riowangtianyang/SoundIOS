# iOS App 初始化实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development 逐任务实现此计划。

**目标：** 让 iOS App 能运行并连接后端 API

**架构：** 使用 Expo 创建 React Native 项目，配置本地开发服务器连接

**技术栈：** Expo + React Native + TypeScript + axios

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `ios/SoundIOS/` | 创建 | Expo 项目目录 |
| `ios/SoundIOS/src/` | 创建 | 源码目录 |
| `ios/SoundIOS/app.json` | 修改 | Expo 配置 |
| `ios/SoundIOS/src/services/api.ts` | 创建 | API 服务 |
| `ios/SoundIOS/package.json` | 创建 | 依赖配置 |

---

## 任务

### 任务 1：创建 Expo 项目

- [ ] **步骤 1：创建 Expo 项目**

```bash
cd /Users/wangyang/Documents/GitHub/Personal/SoundIOS/ios
npx create-expo-app SoundIOS --template blank-typescript
```

- [ ] **步骤 2：复制源码**

```bash
cp -r /Users/wangyang/Documents/GitHub/Personal/SoundIOS/ios/src SoundIOS/
cp /Users/wangyang/Documents/GitHub/Personal/SoundIOS/ios/package.json SoundIOS/
```

- [ ] **步骤 3：安装依赖**

```bash
cd SoundIOS
npm install
```

- [ ] **步骤 4：生成 iOS 原生项目**

```bash
npx expo prebuild --platform ios
```

- [ ] **步骤 5：Commit**

```bash
git add ios/SoundIOS
git commit -m "feat(ios): init Expo project with screens and services"
```

---

### 任务 2：配置 API 服务

**文件：** 创建 `ios/SoundIOS/src/services/api.ts`

- [ ] **步骤 1：创建 API 服务文件**

```typescript
/**
 * SoundIOS API 服务
 */

const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    return response.json();
  }

  // 录音相关
  async uploadRecording(file: { uri: string; name: string; type: string }) {
    const formData = new FormData();
    formData.append('file', file as any);
    return this.request('/recordings', {
      method: 'POST',
      headers: { 'Content-Type': 'multipart/form-data' },
      body: formData,
    });
  }

  async getRecordings() {
    return this.request<{ recordings: any[] }>('/recordings');
  }

  // 待办相关
  async getTodos() {
    return this.request<{ todos: any[] }>('/todos');
  }

  async createTodo(data: { title: string; priority?: number }) {
    return this.request('/todos', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // 日记相关
  async getDiaries() {
    return this.request<{ diaries: any[] }>('/diaries');
  }

  // 人物相关
  async getPersons() {
    return this.request<{ persons: any[] }>('/persons');
  }

  // AI 对话
  async chat(messages: { role: string; content: string }[]) {
    return this.request<{ response: string }>('/chat', {
      method: 'POST',
      body: JSON.stringify({ messages }),
    });
  }

  async getChatContext(personId?: number) {
    const query = personId ? `?person_id=${personId}` : '';
    return this.request(`/chat/context${query}`);
  }

  // 健康检查
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch('http://localhost:8000/health');
      const data = await response.json();
      return data.status === 'healthy';
    } catch {
      return false;
    }
  }
}

export const api = new ApiService();
export default api;
```

- [ ] **步骤 2：Commit**

```bash
git add ios/SoundIOS/src/services/api.ts
git commit -m "feat(ios): add API service for backend communication"
```

---

### 任务 3：配置 App 入口

**文件：** 修改 `ios/SoundIOS/App.tsx`

- [ ] **步骤 1：更新 App.tsx**

```typescript
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { View, Text, StyleSheet } from 'react-native';

import HomeScreen from './src/screens/HomeScreen';
import DiaryScreen from './src/screens/DiaryScreen';
import TodoScreen from './src/screens/TodoScreen';
import PersonScreen from './src/screens/PersonScreen';
import AskScreen from './src/screens/AskScreen';
import { colors } from './src/theme';

const Tab = createBottomTabNavigator();

const TabIcon: React.FC<{ label: string; focused: boolean }> = ({ label, focused }) => {
  const icons: Record<string, string> = {
    首页: '🎙',
    日记: '📖',
    待办: '✓',
    人物: '👥',
    AI: '💬',
  };

  return (
    <View style={styles.iconContainer}>
      <Text style={styles.iconEmoji}>{icons[label] || '•'}</Text>
      <Text style={[styles.iconText, focused && styles.iconFocused]}>{label}</Text>
    </View>
  );
};

function App(): React.JSX.Element {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={{
            tabBarActiveTintColor: colors.primary.main,
            tabBarInactiveTintColor: colors.text.tertiary,
            tabBarStyle: {
              backgroundColor: colors.background.secondary,
              borderTopColor: colors.border.subtle,
              height: 85,
              paddingBottom: 25,
              paddingTop: 10,
            },
            headerShown: false,
          }}>
          <Tab.Screen
            name="Home"
            component={HomeScreen}
            options={{
              tabBarLabel: '首页',
              tabBarIcon: ({ focused }) => <TabIcon label="首页" focused={focused} />,
            }}
          />
          <Tab.Screen
            name="Diary"
            component={DiaryScreen}
            options={{
              tabBarLabel: '日记',
              tabBarIcon: ({ focused }) => <TabIcon label="日记" focused={focused} />,
            }}
          />
          <Tab.Screen
            name="Todo"
            component={TodoScreen}
            options={{
              tabBarLabel: '待办',
              tabBarIcon: ({ focused }) => <TabIcon label="待办" focused={focused} />,
            }}
          />
          <Tab.Screen
            name="Person"
            component={PersonScreen}
            options={{
              tabBarLabel: '人物',
              tabBarIcon: ({ focused }) => <TabIcon label="人物" focused={focused} />,
            }}
          />
          <Tab.Screen
            name="Ask"
            component={AskScreen}
            options={{
              tabBarLabel: 'AI',
              tabBarIcon: ({ focused }) => <TabIcon label="AI" focused={focused} />,
            }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  iconContainer: { alignItems: 'center', justifyContent: 'center', gap: 2 },
  iconEmoji: { fontSize: 20 },
  iconText: { fontSize: 10, color: '#999', fontWeight: '500' },
  iconFocused: { color: '#FF9500' },
});

export default App;
```

- [ ] **步骤 2：Commit**

```bash
git add ios/SoundIOS/App.tsx
git commit -m "feat(ios): configure App entry with navigation"
```

---

## 验证

```bash
cd ios/SoundIOS
npx expo start --ios
# 或
npx expo run:ios --simulator
```

预期：App 在模拟器中启动，显示底部 Tab 导航
