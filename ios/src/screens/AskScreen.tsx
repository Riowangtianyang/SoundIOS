import React, {useState, useRef} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Animated,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import {colors, spacing, borderRadius, shadows} from '../theme';

// 消息类型
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

// 快捷问题
const QuickQuestions: React.FC<{onPress: (q: string) => void}> = ({onPress}) => {
  const questions = [
    '今天我都聊了哪些重要事情？',
    '有没有遗漏的待办事项？',
    '本周沟通情况如何？',
    '生成今日日报',
  ];

  return (
    <View style={styles.quickQuestions}>
      <Text style={styles.quickTitle}>试试这样问</Text>
      <View style={styles.questionList}>
        {questions.map((q, index) => (
          <TouchableOpacity
            key={index}
            style={styles.questionChip}
            onPress={() => onPress(q)}>
            <Text style={styles.questionText}>{q}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
};

// 消息气泡
const MessageBubble: React.FC<{message: Message}> = ({message}) => {
  const isUser = message.role === 'user';

  return (
    <View
      style={[
        styles.messageBubble,
        isUser ? styles.userBubble : styles.assistantBubble,
      ]}>
      <Text
        style={[
          styles.messageText,
          isUser ? styles.userText : styles.assistantText,
        ]}>
        {message.content}
      </Text>
      <Text style={styles.messageTime}>
        {message.timestamp.toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        })}
      </Text>
    </View>
  );
};

const AskScreen: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<ScrollView>(null);

  const handleSend = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // TODO: 调用 API
    // 模拟 AI 回复
    setTimeout(() => {
      const responses = [
        '根据今天的对话记录，你主要和张总进行了项目需求讨论，确认了功能模块和时间节点。还没有完成的待办是发送项目方案，需要在今天18:00前完成。',
        '好的，我来帮你生成今日日报：\n\n📊 今日沟通总结：\n• 与张总讨论项目需求（已确认）\n• 团队周会（开发进度正常）\n• 供应商报价确认（待跟进）\n\n📋 待办事项：\n• 发送项目方案（高优先级）\n• 确认供应商报价\n• 准备演示文稿',
      ];
      const randomResponse =
        responses[Math.floor(Math.random() * responses.length)];

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: randomResponse,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleQuickQuestion = (question: string) => {
    setInputText(question);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={90}>
        {/* 标题 */}
        <View style={styles.header}>
          <Text style={styles.title}>问 AI</Text>
          <Text style={styles.subtitle}>查询你的记忆，生成分析</Text>
        </View>

        {/* 消息区域 */}
        <ScrollView
          ref={scrollRef}
          style={styles.messageList}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.messageListContent}>
          {messages.length === 0 ? (
            <QuickQuestions onPress={handleQuickQuestion} />
          ) : (
            <>
              {messages.map(message => (
                <MessageBubble key={message.id} message={message} />
              ))}
              {isTyping && (
                <View style={styles.typingIndicator}>
                  <Text style={styles.typingText}>AI 正在思考...</Text>
                </View>
              )}
            </>
          )}
        </ScrollView>

        {/* 输入框 */}
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            value={inputText}
            onChangeText={setInputText}
            placeholder="问我任何关于你的对话记录..."
            placeholderTextColor={colors.text.muted}
            multiline
            maxLength={500}
          />
          <TouchableOpacity
            style={[
              styles.sendButton,
              !inputText.trim() && styles.sendButtonDisabled,
            ]}
            onPress={handleSend}
            disabled={!inputText.trim()}>
            <Text
              style={[
                styles.sendButtonText,
                !inputText.trim() && styles.sendButtonTextDisabled,
              ]}>
              →
            </Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.primary,
  },

  keyboardView: {
    flex: 1,
  },

  header: {
    paddingHorizontal: spacing['2xl'],
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border.subtle,
  },

  title: {
    fontSize: 28,
    fontWeight: '700',
    color: colors.text.primary,
  },

  subtitle: {
    fontSize: 14,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },

  messageList: {
    flex: 1,
  },

  messageListContent: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    flexGrow: 1,
  },

  quickQuestions: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },

  quickTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text.secondary,
    marginBottom: spacing.lg,
  },

  questionList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: spacing.sm,
  },

  questionChip: {
    backgroundColor: colors.background.secondary,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.full,
    borderWidth: 1,
    borderColor: colors.border.default,
  },

  questionText: {
    fontSize: 14,
    color: colors.text.secondary,
  },

  messageBubble: {
    maxWidth: '80%',
    padding: spacing.md,
    borderRadius: borderRadius.lg,
    marginBottom: spacing.sm,
  },

  userBubble: {
    backgroundColor: colors.primary.main,
    alignSelf: 'flex-end',
    borderBottomRightRadius: spacing.xs,
  },

  assistantBubble: {
    backgroundColor: colors.background.secondary,
    alignSelf: 'flex-start',
    borderBottomLeftRadius: spacing.xs,
  },

  messageText: {
    fontSize: 15,
    lineHeight: 22,
  },

  userText: {
    color: colors.background.primary,
  },

  assistantText: {
    color: colors.text.primary,
  },

  messageTime: {
    fontSize: 11,
    color: colors.text.muted,
    marginTop: spacing.xs,
    alignSelf: 'flex-end',
  },

  typingIndicator: {
    backgroundColor: colors.background.secondary,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.md,
    alignSelf: 'flex-start',
  },

  typingText: {
    fontSize: 14,
    color: colors.text.tertiary,
    fontStyle: 'italic',
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.border.subtle,
    backgroundColor: colors.background.primary,
  },

  input: {
    flex: 1,
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    paddingTop: spacing.sm,
    fontSize: 15,
    color: colors.text.primary,
    maxHeight: 100,
    marginRight: spacing.sm,
  },

  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.primary.main,
    alignItems: 'center',
    justifyContent: 'center',
  },

  sendButtonDisabled: {
    backgroundColor: colors.background.elevated,
  },

  sendButtonText: {
    fontSize: 22,
    color: colors.background.primary,
    fontWeight: '600',
  },

  sendButtonTextDisabled: {
    color: colors.text.muted,
  },
});

export default AskScreen;