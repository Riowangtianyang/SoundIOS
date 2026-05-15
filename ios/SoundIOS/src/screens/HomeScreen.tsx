import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Dimensions,
  ScrollView,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import {colors, spacing, borderRadius, shadows} from '../theme';

const {width, height} = Dimensions.get('window');

// 脉冲动画组件
const PulseRing: React.FC<{active: boolean}> = ({active}) => {
  const [pulseAnim] = useState(new Animated.Value(0));

  useEffect(() => {
    if (active) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 1500,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 0,
            duration: 0,
            useNativeDriver: true,
          }),
        ]),
      ).start();
    } else {
      pulseAnim.setValue(0);
    }
  }, [active, pulseAnim]);

  if (!active) return null;

  return (
    <Animated.View
      style={[
        styles.pulseRing,
        {
          transform: [
            {scale: pulseAnim.interpolate({inputRange: [0, 1], outputRange: [1, 1.5]})},
          ],
          opacity: pulseAnim.interpolate({inputRange: [0, 1], outputRange: [0.5, 0]}),
        },
      ]}
    />
  );
};

// 录音按钮组件
const RecordButton: React.FC<{recording: boolean; onPress: () => void}> = ({
  recording,
  onPress,
}) => {
  const [scaleAnim] = useState(new Animated.Value(1));

  const handlePressIn = () => {
    Animated.spring(scaleAnim, {
      toValue: 0.95,
      useNativeDriver: true,
    }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      friction: 3,
      useNativeDriver: true,
    }).start();
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      activeOpacity={1}>
      <Animated.View
        style={[
          styles.recordButton,
          recording && styles.recordButtonActive,
          {transform: [{scale: scaleAnim}]},
        ]}>
        <PulseRing active={recording} />
        <View
          style={[
            styles.recordButtonInner,
            recording && styles.recordButtonInnerActive,
          ]}
        />
      </Animated.View>
    </TouchableOpacity>
  );
};

// 统计卡片
const StatCard: React.FC<{label: string; value: string | number; icon: string}> = ({
  label,
  value,
  icon,
}) => (
  <View style={styles.statCard}>
    <Text style={styles.statIcon}>{icon}</Text>
    <Text style={styles.statValue}>{value}</Text>
    <Text style={styles.statLabel}>{label}</Text>
  </View>
);

// 最近录音项
const RecentRecording: React.FC<{
  time: string;
  duration: string;
  onPress: () => void;
}> = ({time, duration, onPress}) => (
  <TouchableOpacity style={styles.recentItem} onPress={onPress}>
    <View style={styles.recentIcon}>
      <Text style={styles.recentIconText}>🎙</Text>
    </View>
    <View style={styles.recentContent}>
      <Text style={styles.recentTime}>{time}</Text>
      <Text style={styles.recentDuration}>{duration}</Text>
    </View>
    <View style={styles.recentArrow}>
      <Text style={styles.recentArrowText}>›</Text>
    </View>
  </TouchableOpacity>
);

const HomeScreen: React.FC = () => {
  const [recording, setRecording] = useState(false);
  const [stats, setStats] = useState({
    segments: 0,
    duration: '00:00',
    interruptions: 0,
  });

  const handleRecordToggle = () => {
    setRecording(!recording);
    // TODO: 调用 API 启动/停止录音
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* 顶部标题 */}
      <View style={styles.header}>
        <Text style={styles.greeting}>下午好</Text>
        <Text style={styles.subtitle}>今天发生了什么？</Text>
      </View>

      {/* 主录音区域 */}
      <View style={styles.recordSection}>
        <RecordButton recording={recording} onPress={handleRecordToggle} />
        <Text style={styles.recordStatus}>
          {recording ? '正在聆听...' : '点击开始录音'}
        </Text>
        <Text style={styles.recordHint}>
          {recording
            ? '我会自动记录对话内容'
            : '开启后我将持续监听周围声音'}
        </Text>
      </View>

      {/* 统计数据 */}
      <View style={styles.statsSection}>
        <StatCard label="录音段数" value={stats.segments} icon="📼" />
        <StatCard label="累计时长" value={stats.duration} icon="⏱" />
        <StatCard label="中断次数" value={stats.interruptions} icon="⚡" />
      </View>

      {/* 最近录音 */}
      <View style={styles.recentSection}>
        <Text style={styles.sectionTitle}>最近录音</Text>
        <ScrollView
          style={styles.recentList}
          showsVerticalScrollIndicator={false}>
          <RecentRecording time="14:32" duration="1:23" onPress={() => {}} />
          <RecentRecording time="11:15" duration="3:45" onPress={() => {}} />
          <RecentRecording time="09:48" duration="2:12" onPress={() => {}} />
          <RecentRecording time="昨天 18:20" duration="5:01" onPress={() => {}} />
        </ScrollView>
      </View>

      {/* 底部导航已通过 App.tsx 的 Tab.Navigator 配置 */}
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

  greeting: {
    fontSize: 32,
    fontWeight: '700',
    color: colors.text.primary,
    letterSpacing: -0.02,
  },

  subtitle: {
    fontSize: 16,
    color: colors.text.secondary,
    marginTop: spacing.xs,
  },

  recordSection: {
    alignItems: 'center',
    paddingVertical: spacing['3xl'],
  },

  recordButton: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: colors.background.elevated,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 3,
    borderColor: colors.primary.main,
    position: 'relative',
  },

  recordButtonActive: {
    borderColor: colors.accent.main,
    backgroundColor: 'rgba(255, 107, 107, 0.1)',
  },

  recordButtonInner: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.primary.main,
  },

  recordButtonInnerActive: {
    width: 30,
    height: 30,
    borderRadius: 8,
    backgroundColor: colors.accent.main,
  },

  pulseRing: {
    position: 'absolute',
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 2,
    borderColor: colors.accent.main,
    backgroundColor: 'transparent',
  },

  recordStatus: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text.primary,
    marginTop: spacing.xl,
  },

  recordHint: {
    fontSize: 14,
    color: colors.text.tertiary,
    marginTop: spacing.sm,
  },

  statsSection: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.xl,
  },

  statCard: {
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.lg,
    padding: spacing.lg,
    alignItems: 'center',
    minWidth: 90,
    ...shadows.sm,
  },

  statIcon: {
    fontSize: 24,
    marginBottom: spacing.xs,
  },

  statValue: {
    fontSize: 20,
    fontWeight: '700',
    color: colors.text.primary,
  },

  statLabel: {
    fontSize: 12,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },

  recentSection: {
    flex: 1,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
  },

  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text.secondary,
    marginBottom: spacing.md,
  },

  recentList: {
    flex: 1,
  },

  recentItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },

  recentIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.background.tertiary,
    alignItems: 'center',
    justifyContent: 'center',
  },

  recentIconText: {
    fontSize: 18,
  },

  recentContent: {
    flex: 1,
    marginLeft: spacing.md,
  },

  recentTime: {
    fontSize: 15,
    fontWeight: '500',
    color: colors.text.primary,
  },

  recentDuration: {
    fontSize: 13,
    color: colors.text.tertiary,
    marginTop: 2,
  },

  recentArrow: {
    paddingLeft: spacing.md,
  },

  recentArrowText: {
    fontSize: 24,
    color: colors.text.muted,
  },
});

export default HomeScreen;