/**
 * AI 个人记忆助手 - 主题配置
 * Neural Warmth 设计语言
 */

// 主色调 - 深色主题 + 温暖点缀
export const colors = {
  // 背景层次
  background: {
    primary: '#0D0D12',      // 最深背景
    secondary: '#15151D',    // 卡片背景
    tertiary: '#1E1E28',    // 悬浮层
    elevated: '#262631',    // 抬升元素
  },

  // 主色 - 琥珀/金色（温暖）
  primary: {
    main: '#F5A623',         // 主色
    light: '#FFD180',        // 浅色
    dark: '#C77B1A',         // 深色
    glow: 'rgba(245, 166, 35, 0.3)', // 发光效果
  },

  // 强调色 - 珊瑚/橙色（活力）
  accent: {
    main: '#FF6B6B',         // 珊瑚红
    light: '#FF8E8E',        // 浅色
    dark: '#D64545',         // 深色
  },

  // 辅助色 - 薄荷绿（清新）
  secondary: {
    main: '#4ECDC4',         // 薄荷绿
    light: '#7EDDD6',        // 浅色
    dark: '#3BA99C',        // 深色
  },

  // 文字颜色
  text: {
    primary: '#FFFFFF',      // 主文字
    secondary: '#A8A8B3',   // 次要文字
    tertiary: '#6B6B76',    // 辅助文字
    muted: '#4A4A55',       // 暗淡文字
  },

  // 功能色
  status: {
    success: '#4ECDC4',     // 成功
    warning: '#F5A623',     // 警告
    error: '#FF6B6B',       // 错误
    info: '#7B68EE',        // 信息
  },

  // 渐变
  gradient: {
    primary: 'linear-gradient(135deg, #F5A623 0%, #FF6B6B 100%)',
    secondary: 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)',
    background: 'linear-gradient(180deg, #0D0D12 0%, #15151D 100%)',
    card: 'linear-gradient(145deg, #1E1E28 0%, #15151D 100%)',
  },

  // 节点颜色（用于图谱）
  nodes: {
    person: '#F5A623',       // 人物节点
    event: '#4ECDC4',        // 事件节点
    topic: '#7B68EE',        // 主题节点
    todo: '#FF6B6B',        // 待办节点
  },

  // 边框
  border: {
    subtle: 'rgba(255, 255, 255, 0.06)',
    default: 'rgba(255, 255, 255, 0.1)',
    emphasis: 'rgba(255, 255, 255, 0.2)',
  },
};

// 字体配置
export const typography = {
  // 字体族
  fontFamily: {
    display: 'System',      // 标题字体
    body: 'System',         // 正文字体
    mono: 'Menlo',          // 等宽字体
  },

  // 字号
  fontSize: {
    xs: 10,
    sm: 12,
    md: 14,
    lg: 16,
    xl: 18,
    '2xl': 22,
    '3xl': 28,
    '4xl': 36,
    '5xl': 48,
  },

  // 字重
  fontWeight: {
    light: '300',
    regular: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },

  // 行高
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },

  // 字间距
  letterSpacing: {
    tight: '-0.02em',
    normal: '0',
    wide: '0.02em',
    wider: '0.05em',
  },
};

// 间距
export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  '2xl': 24,
  '3xl': 32,
  '4xl': 40,
  '5xl': 48,
  '6xl': 64,
};

// 圆角
export const borderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  '2xl': 24,
  full: 9999,
};

// 阴影
export const shadows = {
  sm: '0 2px 8px rgba(0, 0, 0, 0.3)',
  md: '0 4px 16px rgba(0, 0, 0, 0.4)',
  lg: '0 8px 32px rgba(0, 0, 0, 0.5)',
  glow: '0 0 20px rgba(245, 166, 35, 0.3)',
  glowStrong: '0 0 40px rgba(245, 166, 35, 0.5)',
};

// 动画
export const animation = {
  // 时长
  duration: {
    fast: 150,
    normal: 300,
    slow: 500,
    slower: 800,
  },

  // 缓动函数
  easing: {
    spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    smooth: 'cubic-bezier(0.4, 0, 0.2, 1)',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
};

// Z-Index 层
export const zIndex = {
  base: 0,
  dropdown: 100,
  sticky: 200,
  modal: 300,
  toast: 400,
  tooltip: 500,
};

export default {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  animation,
  zIndex,
};