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

// 节点类型
type NodeType = 'person' | 'event' | 'topic' | 'todo';

// 图谱节点
interface GraphNode {
  id: string;
  type: NodeType;
  label: string;
  x: number;
  y: number;
  connections: string[];
}

// 模拟数据
const mockNodes: GraphNode[] = [
  {id: '1', type: 'person', label: '张总', x: 0.3, y: 0.25, connections: ['3']},
  {id: '2', type: 'person', label: '李经理', x: 0.7, y: 0.25, connections: ['3']},
  {id: '3', type: 'event', label: '项目会议', x: 0.5, y: 0.5, connections: ['1', '2', '4']},
  {id: '4', type: 'topic', label: '智能家居', x: 0.3, y: 0.75, connections: ['3', '5']},
  {id: '5', type: 'todo', label: '发报价单', x: 0.7, y: 0.75, connections: ['4']},
];

// 简化图谱渲染（使用圆点和线条）
const SimpleGraph: React.FC<{
  nodes: GraphNode[];
  onNodePress: (node: GraphNode) => void;
  selectedId: string | null;
}> = ({nodes, onNodePress, selectedId}) => {
  const graphWidth = width - spacing['2xl'] * 2 - spacing.md * 2;
  const graphHeight = 260;

  const getNodeColor = (type: NodeType) => {
    switch (type) {
      case 'person':
        return colors.nodes.person;
      case 'event':
        return colors.nodes.event;
      case 'topic':
        return colors.nodes.topic;
      case 'todo':
        return colors.nodes.todo;
    }
  };

  const getNodeSize = (type: NodeType) => {
    switch (type) {
      case 'person':
        return 44;
      case 'event':
        return 36;
      case 'topic':
        return 32;
      case 'todo':
        return 28;
    }
  };

  // 绘制连接线
  const renderConnections = () => {
    const lines: JSX.Element[] = [];
    nodes.forEach(node => {
      node.connections.forEach(targetId => {
        const target = nodes.find(n => n.id === targetId);
        if (target) {
          const x1 = node.x * graphWidth;
          const y1 = node.y * graphHeight;
          const x2 = target.x * graphWidth;
          const y2 = target.y * graphHeight;

          lines.push(
            <View
              key={`${node.id}-${targetId}`}
              style={[
                styles.connectionLine,
                {
                  left: x1,
                  top: y1,
                  width: Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2)),
                  transform: [
                    {
                      rotate: `${Math.atan2(y2 - y1, x2 - x1)}rad`,
                    },
                  ],
                  transformOrigin: 'left center',
                },
              ]}
            />
          );
        }
      });
    });
    return lines;
  };

  return (
    <View style={[styles.simpleGraph, {width: graphWidth, height: graphHeight}]}>
      {/* 连接线 */}
      {renderConnections()}

      {/* 节点 */}
      {nodes.map(node => (
        <TouchableOpacity
          key={node.id}
          style={[
            styles.graphNode,
            {
              left: node.x * graphWidth - getNodeSize(node.type) / 2,
              top: node.y * graphHeight - getNodeSize(node.type) / 2,
              width: getNodeSize(node.type),
              height: getNodeSize(node.type),
              borderRadius: getNodeSize(node.type) / 2,
              backgroundColor: getNodeColor(node.type),
            },
            selectedId === node.id && styles.graphNodeSelected,
          ]}
          onPress={() => onNodePress(node)}>
          <Text style={styles.graphNodeLabel}>{node.label}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
};

// 人物卡片
const PersonCard: React.FC<{
  name: string;
  relationship: string;
  lastContact: string;
  interactionCount: number;
  tags: string[];
  onPress: () => void;
}> = ({name, relationship, lastContact, interactionCount, tags, onPress}) => (
  <TouchableOpacity style={styles.personCard} onPress={onPress}>
    <View style={styles.personAvatar}>
      <Text style={styles.personAvatarText}>{name[0]}</Text>
    </View>
    <View style={styles.personInfo}>
      <Text style={styles.personName}>{name}</Text>
      <Text style={styles.personRelationship}>{relationship}</Text>
      <View style={styles.personMeta}>
        <Text style={styles.personMetaText}>📞 {interactionCount}次沟通</Text>
        <Text style={styles.personMetaText}>🕐 {lastContact}</Text>
      </View>
    </View>
    <View style={styles.personArrow}>
      <Text style={styles.personArrowText}>›</Text>
    </View>
  </TouchableOpacity>
);

const PersonScreen: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [viewMode, setViewMode] = useState<'graph' | 'list'>('graph');

  const handleNodePress = (node: GraphNode) => {
    setSelectedNode(selectedNode?.id === node.id ? null : node);
  };

  const getNodeTypeName = (type: NodeType) => {
    switch (type) {
      case 'person':
        return '人物';
      case 'event':
        return '事件';
      case 'topic':
        return '主题';
      case 'todo':
        return '待办';
    }
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* 标题 */}
      <View style={styles.header}>
        <Text style={styles.title}>人物关系</Text>
        <Text style={styles.subtitle}>知识图谱可视化</Text>
      </View>

      {/* 视图切换 */}
      <View style={styles.viewToggle}>
        <TouchableOpacity
          style={[styles.toggleButton, viewMode === 'graph' && styles.toggleButtonActive]}
          onPress={() => setViewMode('graph')}>
          <Text style={[styles.toggleText, viewMode === 'graph' && styles.toggleTextActive]}>
            图谱
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.toggleButton, viewMode === 'list' && styles.toggleButtonActive]}
          onPress={() => setViewMode('list')}>
          <Text style={[styles.toggleText, viewMode === 'list' && styles.toggleTextActive]}>
            列表
          </Text>
        </TouchableOpacity>
      </View>

      {viewMode === 'graph' ? (
        <>
          {/* 知识图谱 */}
          <View style={styles.graphSection}>
            <Text style={styles.graphTitle}>关系网络</Text>
            <View style={styles.graphContainer}>
              <SimpleGraph
                nodes={mockNodes}
                onNodePress={handleNodePress}
                selectedId={selectedNode?.id || null}
              />
            </View>
          </View>

          {/* 图例 */}
          <View style={styles.legend}>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, {backgroundColor: colors.nodes.person}]} />
              <Text style={styles.legendText}>人物</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, {backgroundColor: colors.nodes.event}]} />
              <Text style={styles.legendText}>事件</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, {backgroundColor: colors.nodes.topic}]} />
              <Text style={styles.legendText}>主题</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, {backgroundColor: colors.nodes.todo}]} />
              <Text style={styles.legendText}>待办</Text>
            </View>
          </View>

          {/* 选中节点详情 */}
          {selectedNode && (
            <View style={styles.nodeDetail}>
              <Text style={styles.nodeDetailTitle}>{selectedNode.label}</Text>
              <Text style={styles.nodeDetailType}>类型: {getNodeTypeName(selectedNode.type)}</Text>
              <Text style={styles.nodeDetailHint}>点击节点可查看详情或编辑</Text>
            </View>
          )}
        </>
      ) : (
        /* 人物列表 */
        <ScrollView
          style={styles.personList}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.personListContent}>
          <PersonCard
            name="张总"
            relationship="客户 · 项目负责人"
            lastContact="今天 14:32"
            interactionCount={15}
            tags={['技术方案', '预算沟通']}
            onPress={() => {}}
          />
          <PersonCard
            name="李经理"
            relationship="供应商 · 采购"
            lastContact="昨天 09:48"
            interactionCount={8}
            tags={['材料采购', '报价确认']}
            onPress={() => {}}
          />
          <PersonCard
            name="王工"
            relationship="同事 · 开发"
            lastContact="昨天 11:15"
            interactionCount={23}
            tags={['技术评审']}
            onPress={() => {}}
          />
          <PersonCard
            name="陈总"
            relationship="客户 · 决策者"
            lastContact="周二 15:20"
            interactionCount={5}
            tags={['商务谈判']}
            onPress={() => {}}
          />
        </ScrollView>
      )}
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
  },

  subtitle: {
    fontSize: 14,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },

  viewToggle: {
    flexDirection: 'row',
    marginHorizontal: spacing.lg,
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.md,
    padding: spacing.xs,
  },

  toggleButton: {
    flex: 1,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.sm,
    alignItems: 'center',
  },

  toggleButtonActive: {
    backgroundColor: colors.primary.main,
  },

  toggleText: {
    fontSize: 14,
    fontWeight: '500',
    color: colors.text.secondary,
  },

  toggleTextActive: {
    color: colors.background.primary,
  },

  graphSection: {
    marginTop: spacing.lg,
    marginHorizontal: spacing.lg,
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    ...shadows.sm,
  },

  graphTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text.primary,
    marginBottom: spacing.md,
  },

  graphContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },

  simpleGraph: {
    position: 'relative',
  },

  connectionLine: {
    position: 'absolute',
    height: 1.5,
    backgroundColor: colors.border.default,
  },

  graphNode: {
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.2)',
  },

  graphNodeSelected: {
    borderColor: colors.text.primary,
    borderWidth: 3,
  },

  graphNodeLabel: {
    fontSize: 10,
    fontWeight: '600',
    color: colors.background.primary,
    textAlign: 'center',
  },

  legend: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'wrap',
    paddingVertical: spacing.md,
    gap: spacing.lg,
  },

  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },

  legendDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: spacing.xs,
  },

  legendText: {
    fontSize: 12,
    color: colors.text.tertiary,
  },

  nodeDetail: {
    backgroundColor: colors.background.secondary,
    marginHorizontal: spacing.lg,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    ...shadows.sm,
  },

  nodeDetailTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text.primary,
  },

  nodeDetailType: {
    fontSize: 14,
    color: colors.text.tertiary,
    marginTop: spacing.xs,
  },

  nodeDetailHint: {
    fontSize: 12,
    color: colors.text.muted,
    marginTop: spacing.sm,
    fontStyle: 'italic',
  },

  personList: {
    flex: 1,
    marginTop: spacing.lg,
  },

  personListContent: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing['4xl'],
  },

  personCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.background.secondary,
    borderRadius: borderRadius.md,
    padding: spacing.md,
    marginBottom: spacing.sm,
    ...shadows.sm,
  },

  personAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.primary.dark,
    alignItems: 'center',
    justifyContent: 'center',
  },

  personAvatarText: {
    fontSize: 20,
    fontWeight: '700',
    color: colors.primary.light,
  },

  personInfo: {
    flex: 1,
    marginLeft: spacing.md,
  },

  personName: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text.primary,
  },

  personRelationship: {
    fontSize: 13,
    color: colors.text.tertiary,
    marginTop: 2,
  },

  personMeta: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: spacing.xs,
  },

  personMetaText: {
    fontSize: 12,
    color: colors.text.tertiary,
  },

  personArrow: {
    paddingLeft: spacing.md,
  },

  personArrowText: {
    fontSize: 24,
    color: colors.text.muted,
  },
});

export default PersonScreen;