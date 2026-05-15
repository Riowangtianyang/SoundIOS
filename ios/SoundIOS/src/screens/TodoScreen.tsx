import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import {colors, spacing, borderRadius, shadows} from '../theme';

// 待办项组件
const TodoItem: React.FC<{
  title: string;
  description?: string;
  dueDate?: string;
  priority: 1 | 2 | 3;
  status: 'pending' | 'completed';
  source?: string;
  onToggle: () => void;
}> = ({title, description, dueDate, priority, status, source, onToggle}) => {
  const priorityColors = {
    1: colors.accent.main,
    2: colors.primary.main,
    3: colors.text.tertiary,
  };

  return (
    <TouchableOpacity
      style={[styles.todoItem, status === 'completed' && styles.todoItemCompleted]}
      onPress={onToggle}>
      <TouchableOpacity
        style={[
          styles.checkbox,
          status === 'completed' && styles.checkboxChecked,
        ]}
        onPress={onToggle}>
        {status === 'completed' && (
          <Text style={styles.checkmark}>✓</Text>
        )}
      </TouchableOpacity>
      <View style={styles.todoContent}>
        <Text
          style={[
            styles.todoTitle,
            status === 'completed' && styles.todoTitleCompleted,
          ]}>
          {title}
        </Text>
        {description && (
          <Text style={styles.todoDescription}>{description}</Text>
        )}
        <View style={styles.todoMeta}>
          <View
            style={[
              styles.priorityBadge,
              {backgroundColor: priorityColors[priority] + '20'},
            ]}>
            <Text style={[styles.priorityText, {color: priorityColors[priority]}]}>
              {priority === 1 ? '高' : priority === 2 ? '中' : '低'}
            </Text>
          </View>
          {dueDate && (
            <Text style={styles.dueDate}>📅 {dueDate}</Text>
          )}
          {source && (
            <Text style={styles.source}>来自: {source}</Text>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
};

// 筛选标签
const FilterTag: React.FC<{
  label: string;
  active: boolean;
  count?: number;
  onPress: () => void;
}> = ({label, active, count, onPress}) => (
  <TouchableOpacity
    style={[styles.filterTag, active && styles.filterTagActive]}
    onPress={onPress}>
    <Text style={[styles.filterText, active && styles.filterTextActive]}>
      {label}
      {count !== undefined && ` (${count})`}
    </Text>
  </TouchableOpacity>
);

const TodoScreen: React.FC = () => {
  const [filter, setFilter] = useState<'all' | 'today' | 'pending'>('all');

  const todos = [
    {
      id: 1,
      title: '给客户发送项目方案',
      description: '包含最新的功能报价和时间表',
      priority: 1 as const,
      status: 'pending' as const,
      dueDate: '今天 18:00',
      source: '与张总沟通',
    },
    {
      id: 2,
      title: '准备周三演示文稿',
      description: '针对新功能的演示',
      priority: 2 as const,
      status: 'pending' as const,
      dueDate: '周三',
    },
    {
      id: 3,
      title: '确认供应商报价',
      priority: 2 as const,
      status: 'completed' as const,
      source: '与李经理沟通',
    },
    {
      id: 4,
      title: '安排下周团队培训',
      priority: 3 as const,
      status: 'pending' as const,
    },
    {
      id: 5,
      title: '整理本周周报',
      priority: 2 as const,
      status: 'pending' as const,
      dueDate: '周五',
    },
  ];

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* 标题 */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>待办事项</Text>
          <Text style={styles.subtitle}>从对话中自动提取</Text>
        </View>
        <TouchableOpacity style={styles.addButton}>
          <Text style={styles.addButtonText}>+</Text>
        </TouchableOpacity>
      </View>

      {/* 筛选器 */}
      <View style={styles.filters}>
        <FilterTag
          label="全部"
          count={todos.length}
          active={filter === 'all'}
          onPress={() => setFilter('all')}
        />
        <FilterTag
          label="今日"
          active={filter === 'today'}
          onPress={() => setFilter('today')}
        />
        <FilterTag
          label="待完成"
          count={todos.filter(t => t.status === 'pending').length}
          active={filter === 'pending'}
          onPress={() => setFilter('pending')}
        />
      </View>

      {/* 待办列表 */}
      <ScrollView
        style={styles.todoList}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.todoListContent}>
        {todos.map(todo => (
          <TodoItem
            key={todo.id}
            title={todo.title}
            description={todo.description}
            priority={todo.priority}
            status={todo.status}
            dueDate={todo.dueDate}
            source={todo.source}
            onToggle={() => {}}
          />
        ))}
      </ScrollView>

      {/* 底部提示 */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          💡 待办事项从对话中自动提取，你可以手动添加或删除
        </Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.primary,
  },

  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: spacing['2xl'],
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
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

  addButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.primary.main,
    alignItems: 'center',
    justifyContent: 'center',
    ...shadows.glow,
  },

  addButtonText: {
    fontSize: 28,
    fontWeight: '400',
    color: colors.background.primary,
    marginTop: -2,
  },

  filters: {
    flexDirection: 'row',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    gap: spacing.sm,
  },

  filterTag: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.full,
  },

  filterTagActive: {
    backgroundColor: colors.primary.main,
  },

  filterText: {
    fontSize: 14,
    color: colors.text.secondary,
    fontWeight: '500',
  },

  filterTextActive: {
    color: colors.background.primary,
  },

  todoList: {
    flex: 1,
  },

  todoListContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing['4xl'],
  },

  todoItem: {
    flexDirection: 'row',
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },

  todoItemCompleted: {
    opacity: 0.6,
  },

  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: colors.text.tertiary,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.md,
    alignSelf: 'flex-start',
    marginTop: 2,
  },

  checkboxChecked: {
    backgroundColor: colors.secondary.main,
    borderColor: colors.secondary.main,
  },

  checkmark: {
    color: colors.background.primary,
    fontSize: 14,
    fontWeight: '700',
  },

  todoContent: {
    flex: 1,
  },

  todoTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: colors.text.primary,
  },

  todoTitleCompleted: {
    textDecorationLine: 'line-through',
    color: colors.text.tertiary,
  },

  todoDescription: {
    fontSize: 14,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },

  todoMeta: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    gap: spacing.sm,
    marginTop: spacing.sm,
  },

  priorityBadge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
    borderRadius: borderRadius.sm,
  },

  priorityText: {
    fontSize: 11,
    fontWeight: '600',
  },

  dueDate: {
    fontSize: 12,
    color: colors.text.tertiary,
  },

  source: {
    fontSize: 12,
    color: colors.primary.light,
    fontStyle: 'italic',
  },

  footer: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    borderTopWidth: 1,
    borderTopColor: colors.border.subtle,
  },

  footerText: {
    fontSize: 13,
    color: colors.text.tertiary,
    textAlign: 'center',
  },
});

export default TodoScreen;