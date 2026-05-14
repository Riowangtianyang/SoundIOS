/**
 * API 服务 - 与后端 Mac 服务器通信
 */

// 后端服务器地址（需要配置 frp 内网穿透）
const API_BASE_URL = 'http://YOUR_MAC_IP:8000/api';

// 请求封装
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// 录音相关 API
export const recordingsAPI = {
  // 获取录音列表
  list: () =>
    request<{
      recordings: Array<{
        id: number;
        audio_path: string;
        duration: number;
        status: string;
        created_at: string;
      }>;
    }>('/recordings'),

  // 获取单个录音
  get: (id: number) =>
    request<{
      id: number;
      audio_path: string;
      duration: number;
      status: string;
      transcript?: {
        text: string;
        segments: Array<{start: number; end: number; text: string}>;
      };
    }>(`/recordings/${id}`),

  // 上传录音
  upload: (file: {uri: string; name: string; type: string}) => {
    const formData = new FormData();
    formData.append('file', file as any);

    return request<{
      id: number;
      status: string;
    }>('/recordings', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    });
  },

  // 删除录音
  delete: (id: number) =>
    request<{message: string}>(`/recordings/${id}`, {
      method: 'DELETE',
    }),
};

// 日记相关 API
export const diaryAPI = {
  // 获取日记列表
  list: () =>
    request<{
      diaries: Array<{
        id: number;
        date: string;
        summary: string;
        mood_score: number;
      }>;
    }>('/diaries'),

  // 获取指定日期日记
  getByDate: (date: string) =>
    request<{
      id?: number;
      date: string;
      summary: string;
      details?: string;
      mood_score?: number;
    }>(`/diaries/date/${date}`),
};

// 待办相关 API
export const todosAPI = {
  // 获取待办列表
  list: (params?: {status?: string; priority?: number}) => {
    const queryString = params
      ? '?' + new URLSearchParams(params as any).toString()
      : '';
    return request<{
      todos: Array<{
        id: number;
        title: string;
        description?: string;
        due_date?: string;
        priority: number;
        status: string;
      }>;
    }>(`/todos${queryString}`);
  },

  // 创建待办
  create: (todo: {
    title: string;
    description?: string;
    due_date?: string;
    priority?: number;
  }) =>
    request<{
      id: number;
      title: string;
      status: string;
    }>('/todos', {
      method: 'POST',
      body: JSON.stringify(todo),
    }),

  // 更新待办
  update: (id: number, updates: Partial<{title: string; status: string}>) =>
    request<{id: number}>(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    }),

  // 删除待办
  delete: (id: number) =>
    request<{message: string}>(`/todos/${id}`, {
      method: 'DELETE',
    }),
};

// 人物相关 API
export const personsAPI = {
  // 获取人物列表
  list: () =>
    request<{
      persons: Array<{
        id: number;
        name: string;
        relationship_type: string;
        notes?: string;
        personality_tags: string[];
      }>;
    }>('/persons'),

  // 创建人物
  create: (person: {
    name: string;
    relationship_type?: string;
    notes?: string;
  }) =>
    request<{id: number; name: string}>('/persons', {
      method: 'POST',
      body: JSON.stringify(person),
    }),

  // 更新人物
  update: (
    id: number,
    updates: Partial<{
      name: string;
      relationship_type: string;
      notes: string;
      personality_tags: string[];
    }>
  ) =>
    request<{id: number}>(`/persons/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    }),
};

// 问AI相关 API
export const chatAPI = {
  // 发送消息
  send: (messages: Array<{role: string; content: string}>, returnAudio = false) =>
    request<{
      response: string;
    }>('/chat', {
      method: 'POST',
      body: JSON.stringify({messages, return_audio: returnAudio}),
    }),

  // 获取上下文
  getContext: (personId?: number) => {
    const queryString = personId ? `?person_id=${personId}` : '';
    return request<{
      person?: any;
      memories: Array<{id: number; content: string; category: string}>;
    }>(`/chat/context${queryString}`);
  },

  // 获取可用语音列表
  getVoices: () =>
    request<{
      voices: Record<string, string>;
    }>('/chat/voices'),
};

// 导出所有 API
export default {
  recordings: recordingsAPI,
  diary: diaryAPI,
  todos: todosAPI,
  persons: personsAPI,
  chat: chatAPI,
};