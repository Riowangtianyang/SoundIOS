# 录音功能实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development 逐任务实现此计划。

**目标：** 实现无感录音功能（手动模式 + 后台模式）

**架构：** 使用 expo-av 实现录音，检测句子结束自动分段

**技术栈：** expo-av + React Native + TypeScript

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `ios/SoundIOS/src/services/recorder.ts` | 创建 | 录音服务 |
| `ios/SoundIOS/src/screens/HomeScreen.tsx` | 修改 | 添加录音按钮 |
| `ios/SoundIOS/src/hooks/useRecorder.ts` | 创建 | 录音 Hook |

---

## 任务

### 任务 1：创建录音服务

**文件：** 创建 `ios/SoundIOS/src/services/recorder.ts`

- [ ] **步骤 1：创建录音服务**

```typescript
/**
 * 录音服务
 * 支持手动模式和后台模式
 */
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';

export interface RecordingOptions {
  mode: 'manual' | 'background';
  onSpeechEnd?: () => void;
}

class RecorderService {
  private recording: Audio.Recording | null = null;
  private mode: 'manual' | 'background' = 'manual';

  async requestPermissions(): Promise<boolean> {
    const { status } = await Audio.requestPermissionsAsync();
    return status === 'granted';
  }

  async startRecording(options: RecordingOptions): Promise<void> {
    this.mode = options.mode;

    await Audio.setAudioModeAsync({
      allowsRecordingIOS: true,
      playsInSilentModeIOS: true,
    });

    const { recording } = await Audio.Recording.createAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY,
      undefined,
      100 // 每 100ms 回调用于检测音量
    );

    this.recording = recording;
  }

  async stopRecording(): Promise<{ uri: string; duration: number } | null> {
    if (!this.recording) return null;

    await this.recording.stopAndUnloadAsync();
    const uri = this.recording.getURI();
    const status = await this.recording.getStatusAsync();

    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
    });

    this.recording = null;

    if (uri) {
      return {
        uri,
        duration: status.durationMillis || 0,
      };
    }
    return null;
  }

  async deleteRecording(uri: string): Promise<void> {
    await FileSystem.deleteAsync(uri, { idempotent: true });
  }

  get isRecording(): boolean {
    return this.recording !== null;
  }
}

export const recorderService = new RecorderService();
export default recorderService;
```

- [ ] **步骤 2：Commit**

```bash
git add ios/SoundIOS/src/services/recorder.ts
git commit -m "feat(recording): add recorder service with expo-av"
```

---

### 任务 2：创建录音 Hook

**文件：** 创建 `ios/SoundIOS/src/hooks/useRecorder.ts`

- [ ] **步骤 1：创建 useRecorder Hook**

```typescript
/**
 * 录音 Hook
 */
import { useState, useCallback } from 'react';
import { recorderService } from '../services/recorder';
import { api } from '../services/api';

export function useRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const startRecording = useCallback(async (mode: 'manual' | 'background' = 'manual') => {
    const hasPermission = await recorderService.requestPermissions();
    if (!hasPermission) {
      throw new Error('Microphone permission denied');
    }

    await recorderService.startRecording({ mode });
    setIsRecording(true);
  }, []);

  const stopAndUpload = useCallback(async () => {
    setIsRecording(false);
    setIsUploading(true);

    try {
      const result = await recorderService.stopRecording();
      if (!result) return null;

      // 上传到后端
      const filename = result.uri.split('/').pop() || 'recording.m4a';
      const response = await api.uploadRecording({
        uri: result.uri,
        name: filename,
        type: 'audio/m4a',
      });

      // 删除本地文件
      await recorderService.deleteRecording(result.uri);

      return response;
    } finally {
      setIsUploading(false);
    }
  }, []);

  return {
    isRecording,
    isUploading,
    startRecording,
    stopAndUpload,
  };
}
```

- [ ] **步骤 2：Commit**

```bash
git add ios/SoundIOS/src/hooks/useRecorder.ts
git commit -m "feat(recording): add useRecorder hook"
```

---

### 任务 3：更新 HomeScreen

**文件：** 修改 `ios/SoundIOS/src/screens/HomeScreen.tsx`

- [ ] **步骤 1：添加录音按钮**

```typescript
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRecorder } from '../hooks/useRecorder';
import { colors } from '../theme';

export default function HomeScreen() {
  const { isRecording, isUploading, startRecording, stopAndUpload } = useRecorder();
  const [lastResult, setLastResult] = useState<any>(null);

  const handlePress = async () => {
    if (isRecording) {
      const result = await stopAndUpload();
      setLastResult(result);
    } else {
      await startRecording('manual');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>AI 个人记忆助手</Text>

      {/* 录音按钮 */}
      <TouchableOpacity
        style={[styles.recordButton, isRecording && styles.recordingButton]}
        onPress={handlePress}
        disabled={isUploading}>
        <Text style={styles.recordButtonText}>
          {isUploading ? '上传中...' : isRecording ? '停止录音' : '开始录音'}
        </Text>
      </TouchableOpacity>

      {/* 上次录音结果 */}
      {lastResult && (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>录音已处理</Text>
          <Text style={styles.resultText}>ID: {lastResult.id}</Text>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background.primary, padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: colors.text.primary, marginBottom: 40 },
  recordButton: {
    width: 120, height: 120,
    borderRadius: 60,
    backgroundColor: colors.primary.main,
    justifyContent: 'center', alignItems: 'center',
    alignSelf: 'center',
  },
  recordingButton: { backgroundColor: colors.status.error },
  recordButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  resultCard: { marginTop: 20, padding: 15, backgroundColor: colors.background.secondary, borderRadius: 10 },
  resultTitle: { fontSize: 16, fontWeight: 'bold', color: colors.text.primary },
  resultText: { fontSize: 14, color: colors.text.secondary, marginTop: 5 },
});
```

- [ ] **步骤 2：Commit**

```bash
git add ios/SoundIOS/src/screens/HomeScreen.tsx
git commit -m "feat(recording): add record button to HomeScreen"
```

---

## 验证

```bash
cd ios/SoundIOS
npx expo run:ios --simulator
```

预期：点击录音按钮后开始录音，再次点击停止并上传
