import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import {colors, spacing, borderRadius, shadows} from '../theme';

const {width} = Dimensions.get('window');

// 日期卡片组件
const DateCard: React.FC<{
  date: string;
  day: string;
  isSelected: boolean;
  onPress: () => void;
}> = ({date, day, isSelected, onPress}) => (
  <TouchableOpacity
    style={[styles.dateCard, isSelected && styles.dateCardSelected]}
    onPress={onPress}>
    <Text style={[styles.dateDay, isSelected && styles.dateDaySelected]}>
      {day}
    </Text>
    <Text style={[styles.dateNum, isSelected && styles.dateNumSelected]}>
      {date.split('-')[2]}
    </Text>
  </TouchableOpacity>
);

// 日记摘要卡片
const DiaryCard: React.FC<{
  time: string;
  summary: string;
  mood: string;
  tags: string[];
}> = ({time, summary, mood, tags}) => (
  <View style={styles.diaryCard}>
    <View style={styles.diaryHeader}>
      <Text style={styles.diaryTime}>{time}</Text>
      <View style={styles.diaryMood}>
        <Text style={styles.diaryMoodEmoji}>
          {mood === 'good' ? '😊' : mood === 'bad' ? '😔' : '😐'}
        </Text>
      </View>
    </View>
    <Text style={styles.diarySummary}>{summary}</Text>
    <View style={styles.diaryTags}>
      {tags.map((tag, index) => (
        <View key={index} style={styles.tag}>
          <Text style={styles.tagText}>{tag}</Text>
        </View>
      ))}
    </View>
  </View>
);

// 一周概览
const WeekOverview: React.FC<{
  moodScore: number;
  eventCount: number;
  todoCount: number;
}> = ({moodScore, eventCount, todoCount}) => (
  <View style={styles.weekOverview}>
    <Text style={styles.weekTitle}>本周概览</Text>
    <View style={styles.weekStats}>
      <View style={styles.weekStat}>
        <Text style={styles.weekStatValue}>{moodScore}</Text>
        <Text style={styles.weekStatLabel}>状态评分</Text>
      </View>
      <View style={styles.weekDivider} />
      <View style={styles.weekStat}>
        <Text style={styles.weekStatValue}>{eventCount}</Text>
        <Text style={styles.weekStatLabel}>沟通事件</Text>
      </View>
      <View style={styles.weekDivider} />
      <View style={styles.weekStat}>
        <Text style={styles.weekStatValue}>{todoCount}</Text>
        <Text style={styles.weekStatLabel}>待办事项</Text>
      </View>
    </View>
  </View>
);

const DiaryScreen: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState('14');
  const [dates] = useState(['12', '13', '14', '15', '16', '17', '18']);
  const [days] = useState(['一', '二', '三', '四', '五', '六', '日']);

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* 标题 */}
      <View style={styles.header}>
        <Text style={styles.title}>记忆日记</Text>
        <Text style={styles.subtitle}>2026年5月</Text>
      </View>

      {/* 日期选择器 */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.dateSelector}
        contentContainerStyle={styles.dateSelectorContent}>
        {dates.map((date, index) => (
          <DateCard
            key={date}
            date={`2026-05-${date}`}
            day={days[index]}
            isSelected={date === selectedDate}
            onPress={() => setSelectedDate(date)}
          />
        ))}
      </ScrollView>

      {/* 一周概览 */}
      <WeekOverview moodScore={7.5} eventCount={12} todoCount={5} />

      {/* 日记列表 */}
      <ScrollView
        style={styles.diaryList}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.diaryListContent}>
        <DiaryCard
          time="14:32"
          summary="与客户张总进行了项目需求讨论，确认了主要功能模块和时间节点。他对方案表示认可，但提出需要增加用户权限管理功能。"
          mood="good"
          tags={['客户沟通', '项目需求']}
        />
        <DiaryCard
          time="11:15"
          summary="团队周会，讨论了本周开发进度。我负责的登录模块已完成 80%，明天可以提测。"
          mood="normal"
          tags={['团队会议']}
        />
        <DiaryCard
          time="09:48"
          summary="接到供应商李经理电话，确认下周的材料配送时间。有轻微延期，但不影响整体进度。"
          mood="normal"
          tags={['供应商沟通']}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.primary,
  },

  header: {
    paddingHorizontal: spacing['2xl'],
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
  },

  title: {
    fontSize: 28,
    fontWeight: '700',
    color: colors.text.primary,
    letterSpacing: -0.02,
  },

  subtitle: {
    fontSize: 14,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },

  dateSelector: {
    maxHeight: 80,
    paddingVertical: spacing.md,
  },

  dateSelectorContent: {
    paddingHorizontal: spacing.lg,
    gap: spacing.sm,
  },

  dateCard: {
    width: 50,
    height: 70,
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: spacing.sm,
    borderWidth: 2,
    borderColor: 'transparent',
  },

  dateCardSelected: {
    backgroundColor: colors.primary.dark,
    borderColor: colors.primary.main,
  },

  dateDay: {
    fontSize: 12,
    color: colors.text.tertiary,
    fontWeight: '500',
  },

  dateDaySelected: {
    color: colors.primary.light,
  },

  dateNum: {
    fontSize: 20,
    fontWeight: '700',
    color: colors.text.secondary,
    marginTop: spacing.xs,
  },

  dateNumSelected: {
    color: colors.text.primary,
  },

  weekOverview: {
    backgroundColor: colors.background.secondary,
    marginHorizontal: spacing.lg,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    ...shadows.sm,
  },

  weekTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text.primary,
    marginBottom: spacing.md,
  },

  weekStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },

  weekStat: {
    alignItems: 'center',
    flex: 1,
  },

  weekStatValue: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.primary.main,
  },

  weekStatLabel: {
    fontSize: 12,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },

  weekDivider: {
    width: 1,
    height: 30,
    backgroundColor: colors.border.subtle,
  },

  diaryList: {
    flex: 1,
    marginTop: spacing.lg,
  },

  diaryListContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing['4xl'],
  },

  diaryCard: {
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
    ...shadows.sm,
  },

  diaryHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },

  diaryTime: {
    fontSize: 14,
    color: colors.text.tertiary,
  },

  diaryMood: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: colors.background.tertiary,
    alignItems: 'center',
    justifyContent: 'center',
  },

  diaryMoodEmoji: {
    fontSize: 16,
  },

  diarySummary: {
    fontSize: 15,
    color: colors.text.primary,
    lineHeight: 22,
    marginBottom: spacing.md,
  },

  diaryTags: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
  },

  tag: {
    backgroundColor: colors.background.tertiary,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.sm,
  },

  tagText: {
    fontSize: 12,
    color: colors.secondary.main,
    fontWeight: '500',
  },
});

export default DiaryScreen;