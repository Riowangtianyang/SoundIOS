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