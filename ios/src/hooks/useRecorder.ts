/**
 * 录音 Hook
 */
import { useState, useCallback } from 'react';
import { recorderService } from '../services/recorder';
import { recordingsAPI } from '../services/api';

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
      const response = await recordingsAPI.upload({
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

export default useRecorder;