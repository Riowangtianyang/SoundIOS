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