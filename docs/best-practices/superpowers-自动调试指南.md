# Superpowers 自动调试完整指南

> systematic-debugging 技能详解
> 更新日期：2025-12-27

---

## 目录

- [核心概念](#核心概念)
- [4 阶段调试流程](#4-阶段调试流程)
- [如何触发](#如何触发)
- [实际使用示例](#实际使用示例)
- [相关技能](#相关技能)
- [最佳实践](#最佳实践)

---

## 核心概念

### 什么是 systematic-debugging？

**systematic-debugging** 是 Superpowers 中的一个核心技能，实施**系统化的 4 阶段根因分析**过程。

**与传统调试的区别**：

| 方面 | 传统调试 | Systematic Debugging |
|------|----------|---------------------|
| 方法 | 试错、猜测 | 系统化、科学方法 |
| 流程 | 随意性 | 强制性 4 阶段 |
| 目标 | 快速修复 | 找到并修复根因 |
| 验证 | "看起来可以了" | 完整验证流程 |
| 防止回归 | 无 | 自动添加测试 |

**核心理念**：
> "不要修复症状，要找到并修复根因"

---

## 4 阶段调试流程

### 阶段 1：问题识别（Problem Identification）

**目标**：明确定义错误并收集证据

**Claude 会做什么**：

```bash
# 1. 重现错误
Claude: "让我重现错误..."
> 运行失败的代码
> 触发错误条件
> 观察错误行为

# 2. 收集证据
Claude: "收集证据..."
✓ 错误消息
✓ 堆栈跟踪
✓ 日志文件
✓ 系统状态
✓ 相关代码

# 3. 确定失败点
Claude: "分析堆栈跟踪..."
> 定位确切失败位置
> 理解调用链
> 识别相关组件

# 4. 一致性验证
Claude: "验证可重现性..."
> 100% 可重现
> 或特定条件下重现
```

**关键输出**：

```markdown
## 问题描述

**错误消息**: `TypeError: Cannot read property 'user' of undefined`

**发生位置**: `src/controllers/auth.js:42`

**堆栈跟踪**:
```
TypeError: Cannot read property 'user' of undefined
    at authenticate (src/controllers/auth.js:42:15)
    at processTicksAndRejections (internal/process/task_queues.js:95:5)
```

**触发条件**:
- 用户登录后访问受保护路由
- Token 有效期内的请求
- 100% 可重现

**相关代码**:
- src/controllers/auth.js (第 35-50 行)
- src/middleware/auth.js (第 10-20 行)
```

---

### 阶段 2：假设形成（Hypothesis Formation）

**目标**：基于可用数据生成潜在原因

**Claude 会做什么**：

```bash
# 1. 列出可能原因
Claude: "基于证据，可能的原因："

假设 A: 数据库查询返回 undefined
假设 B: Token 解析失败但没有抛出错误
假设 C: 中间件执行顺序错误
假设 D: 异步处理导致时序问题

# 2. 评估每个假设
Claude: "评估假设..."
假设 A: 可能性 40% - 常见问题
假设 B: 可能性 30% - 有错误处理
假设 C: 可能性 20% - 最近改动过
假设 D: 可能性 10% - 代码是同步的

# 3. 按概率排序
Claude: "测试顺序：A → B → C → D"
```

**关键输出**：

```markdown
## 潜在原因假设

### 假设 A: 数据库查询返回 undefined [40%]
**原因**: User.find() 返回 null/undefined
**证据**: auth.js:42 直接访问 .user 而没有检查
**验证方法**: 添加日志检查查询结果

### 假设 B: Token 解析失败 [30%]
**原因**: JWT verify 失败但返回 undefined
**证据**: 错误处理可能吞掉错误
**验证方法**: 添加 try-catch 和日志

### 假设 C: 中间件执行顺序错误 [20%]
**原因**: auth 中间件可能在其他中间件之前
**证据**: 最近改动过中间件顺序
**验证方法**: 检查 app.use() 顺序

### 假设 D: 异步时序问题 [10%]
**原因**: await/await 使用不当
**证据**: 代码看起来是正确的
**验证方法**: 检查所有 async/await
```

---

### 阶段 3：假设测试（Hypothesis Testing）

**目标**：通过受控实验系统化测试每个假设

**Claude 会做什么**：

```bash
# 测试假设 A: 数据库查询返回 undefined

Claude: "设计实验 1："

实验：添加日志检查数据库查询结果
位置：src/controllers/auth.js:40
代码：
```javascript
console.log('DB Result:', user);
if (!user) {
  console.log('User is undefined!');
}
```

执行：运行失败场景
预期：
- 如果看到 "User is undefined!" → 假设 A 正确
- 如果看到正常用户对象 → 假设 A 错误

结果：✗ 未触发
结论：假设 A 不成立

# 测试假设 B: Token 解析失败

Claude: "设计实验 2："

实验：添加 try-catch 捕获验证错误
位置：src/middleware/auth.js
代码：
```javascript
try {
  const decoded = jwt.verify(token, secret);
  console.log('Token decoded:', decoded);
} catch (error) {
  console.log('Token verify error:', error);
}
```

执行：运行失败场景
预期：
- 如果看到 "Token verify error" → 假设 B 正确
- 如果看到正常解码 → 假设 B 错误

结果：✓ 确认！
结论：假设 B 正确，找到根因
```

**关键输出**：

```markdown
## 假设测试结果

### 实验 1: 数据库查询检查
**方法**: 添加日志输出
**结果**: ✗ 未发现问题
**结论**: 假设 A 不成立

### 实验 2: Token 解析验证
**方法**: 添加 try-catch 和日志
**结果**: ✓ 确认问题！
```
Token verify error: JsonWebTokenError: invalid token
```
**结论**: ✓ 找到根因！
**根因**: JWT verify 失败但错误被吞掉

### 实验 3: （不需要）
实验 2 已确认根因，停止测试
```

---

### 阶段 4：解决方案实施（Solution Implementation）

**目标**：应用验证的解决方案并确认解决

**Claude 会做什么**：

```bash
# 1. 修复根因
Claude: "实施修复..."

修改：src/middleware/auth.js
```javascript
// 修复前
try {
  const decoded = jwt.verify(token, secret);
  req.user = decoded;
} catch (error) {
  // 错误被吞掉
  next();
}

// 修复后
try {
  const decoded = jwt.verify(token, secret);
  req.user = decoded;
  next();
} catch (error) {
  console.error('Token verification failed:', error);
  return res.status(401).json({
    error: 'Authentication failed',
    message: 'Invalid token'
  });
}
```

# 2. 添加自动化测试
Claude: "添加测试防止回归..."

测试：src/middleware/auth.test.js
```javascript
describe('Auth Middleware', () => {
  it('should reject invalid token', async () => {
    const invalidToken = 'invalid.token.here';
    const res = await request(app)
      .get('/protected')
      .set('Authorization', `Bearer ${invalidToken}`);

    expect(res.status).toBe(401);
    expect(res.body.error).toBe('Authentication failed');
  });
});
```

# 3. 验证修复
Claude: "验证修复..."
> $ npm test
> ✓ all tests pass

# 4. 运行失败场景
Claude: "重现原始问题..."
> $ 运行失败场景
> ✓ 问题已解决！

# 5. 文档化解决方案
Claude: "更新文档..."
> 添加注释说明修复原因
> 更新 CHANGELOG
> 记录问题解决过程
```

**关键输出**：

```markdown
## 解决方案

### 修复代码
**文件**: src/middleware/auth.js
**变更**: 添加正确的错误处理
**行数**: +5 -2

### 添加测试
**文件**: src/middleware/auth.test.js
**测试**: Invalid token rejection
**覆盖**: 防止回归

### 验证结果
✓ 所有测试通过（42/42）
✓ 原始问题已解决
✓ 不会影响其他功能
✓ 性能无影响

### 文档更新
✓ 代码注释
✓ CHANGELOG.md
✓ 问题解决记录
```

---

## 如何触发

### 方式 1：自动触发（推荐）

```bash
# 自然描述问题
You: "生产环境的登录功能出问题了"

# Superpowers 自动触发
Claude: "检测到调试需求...
启动 systematic-debugging 技能..."
```

### 方式 2：明确触发

```bash
# 描述具体问题
You: "API 端点返回 500 错误"

Claude: "开始系统化调试..."

# 或者明确要求
You: "请使用 systematic-debugging 调试这个问题"

Claude: "启动 systematic-debugging 流程..."
```

### 方式 3：命令触发

```bash
# 如果技能有独立命令
/superpowers:systematic-debugging "问题描述"
```

---

## 实际使用示例

### 示例 1：API 500 错误

```bash
# 开始
You: "我的 API 返回 500 错误"

# 自动触发 systematic-debugging

Claude: "开始系统化调试...

## 阶段 1：问题识别

收集证据：
- 错误：`Internal Server Error`
- 端点：`POST /api/users`
- 发生时间：每次请求
- 可重现：100%

分析代码：src/routes/users.js
- 定位失败点：第 45 行
- 错误类型：未捕获的异常

## 阶段 2：假设形成

可能原因：
A. 数据库连接失败 [30%]
B. 请求验证失败 [40%]
C. 数据模型约束冲突 [20%]
D. 外部 API 调用失败 [10%]

测试顺序：B → A → C → D

## 阶段 3：假设测试

测试假设 B：请求验证失败

实验：添加验证日志
```javascript
console.log('Request body:', req.body);
console.log('Validation result:', validationResult);
```

执行：发送测试请求
结果：✓ 确认！
```
Validation error: 'email' is required
```

结论：找到根因！

## 阶段 4：解决方案实施

修复：添加更好的错误处理
```javascript
if (validationResult.error) {
  return res.status(400).json({
    error: 'Validation failed',
    details: validationResult.error.details
  });
}
```

测试：添加验证测试
验证：✓ 所有测试通过

完成！根因已修复并防止回归。"
```

### 示例 2：前端渲染错误

```bash
You: "用户列表页面有时显示不出来"

Claude: "开始系统化调试...

## 阶段 1：问题识别

问题描述：
- 症状：页面空白，无错误显示
- 场景：用户列表页面
- 频率：间歇性，约 30% 时间
- 浏览器：Chrome 和 Firefox 都有

收集证据：
- Console: 无错误
- Network: API 返回 200
- DOM: 元素存在但内容为空

## 阶段 2：假设形成

可能原因：
A. React 状态未更新 [40%]
B. 异步数据加载竞争 [35%]
C. CSS 隐藏内容 [15%]
D. 浏览器兼容性 [10%]

## 阶段 3：假设测试

测试假设 A：React 状态
- 添加 React DevTools 检查
- 结果：✗ 状态正常

测试假设 B：异步竞争
- 添加日志追踪数据流
- 结果：✓ 确认！
```
Data undefined at render time
```

## 阶段 4：解决方案实施

修复：添加加载状态
```javascript
const [loading, setLoading] = useState(true);
const [users, setUsers] = useState([]);

useEffect(() => {
  fetchUsers().then(data => {
    setUsers(data);
    setLoading(false);
  });
}, []);

if (loading) return <Spinner />;
return <UserList users={users} />;
```

验证：✓ 问题解决
测试：添加集成测试

完成！"
```

### 示例 3：内存泄漏

```bash
You: "服务器运行一段时间后内存持续增长"

Claude: "开始系统化调试...

## 阶段 1：问题识别

问题特征：
- 内存增长：每小时 ~100MB
- 触发条件：高负载后
- 影响：最终 OOM

收集证据：
- Node.js heap snapshot
- 内存 profiler
- 事件监听器检查

## 阶段 2：假设形成

可能原因：
A. 未清理的事件监听器 [50%]
B. 闭包持有大对象 [30%]
C. 缓存无限增长 [15%]
D. 数据库连接未关闭 [5%]

## 阶段 3：假设测试

测试假设 A：事件监听器
- 使用 Chrome DevTools 检测
- 结果：✓ 确认！
发现：socket.io 连接未清理

## 阶段 4：解决方案实施

修复：添加清理逻辑
```javascript
socket.on('disconnect', () => {
  // 清理所有事件监听器
  socket.removeAllListeners();
  // 清理用户数据
  userCache.delete(userId);
});
```

验证：
- 内存 profiler 确认无泄漏
- 负载测试 24 小时
- 结果：✓ 内存稳定

完成！"
```

---

## 相关技能

### 1. verification-before-completion

**何时使用**：调试完成后

```bash
# 系统化调试后自动触发
Claude: "调试完成，启动验证流程..."

# 会验证：
✓ 修复已彻底测试
✓ 添加了回归测试
✓ 边缘情况已考虑
✓ 性能影响已评估
✓ 文档已更新
```

### 2. defense-in-depth

**何时使用**：需要额外防护

```bash
Claude: "添加纵深防御..."

# 会添加：
✓ 主要解决方案验证
✓ 次要预防措施
✓ 监控和警报
✓ 日志记录增强
```

### 3. root-cause-tracing

**何时使用**：复杂问题需要深入分析

```bash
Claude: "启动根因追溯..."

# 会分析：
✓ 调用栈分析
✓ 错误模式识别
✓ 系统状态重构
✓ 因果链映射
```

---

## 最佳实践

### 1. 提供足够的上下文

```bash
❌ 不好：
"有个 bug"

✅ 好：
"用户登录后访问 /dashboard 时返回 500 错误
错误消息：'Cannot read property id of undefined'
堆栈跟踪：[完整堆栈]
可重现：100%
最近改动：昨天添加了新的中间件"
```

### 2. 让 Claude 完成整个流程

```bash
❌ 不要：
在阶段 1 就开始自己修复
跳过假设测试直接改代码

✅ 应该：
让 Claude 完成 4 个阶段
基于证据做出决策
验证假设后再修复
```

### 3. 信任流程，即使看起来慢

```bash
# 流程可能需要 10-20 分钟
# 但能找到真正的根因
# 而不是表面症状

阶段 1: 2-3 分钟 - 收集证据
阶段 2: 3-5 分钟 - 形成假设
阶段 3: 5-10 分钟 - 测试假设
阶段 4: 2-5 分钟 - 实施修复

总计：12-23 分钟
# 但一次解决，不会复发
```

### 4. 利用测试防止回归

```bash
# systematic-debugging 会自动添加测试
# 确保问题不会再次出现

✓ 单元测试
✓ 集成测试
✓ 边缘情况测试
```

### 5. 记录学习过程

```bash
# 每次调试后创建文档

Claude: "创建调试报告..."

## 调试报告

### 问题描述
- 症状
- 触发条件
- 影响范围

### 调试过程
- 测试的假设
- 发现的证据
- 根因分析

### 解决方案
- 实施的修复
- 添加的测试
- 性能影响

### 经验教训
- 如何避免类似问题
- 改进建议
```

---

## 调试技巧

### 技巧 1：使用日志驱动调试

```bash
# 让 Claude 添加详细日志
Claude: "添加调试日志..."

# 日志位置：
- 关键变量
- 函数入口/出口
- 错误处理
- 异步操作

# 日志级别：
debug: 详细信息
info: 重要事件
warn: 警告
error: 错误
```

### 技巧 2：二分法快速定位

```bash
# 对于代码库中的问题

Claude: "使用二分法定位..."

1. 检查代码库的一半
2. 问题是否在这部分？
   - 是：继续二分这部分
   - 否：检查另一半
3. 重复直到定位到具体文件/函数
```

### 技巧 3：最小可复现案例

```bash
# Claude 会创建最小案例

Claude: "创建最小复现..."

1. 提取核心问题代码
2. 移除无关依赖
3. 创建独立测试
4. 验证可以复现
5. 在隔离环境中修复
```

### 技巧 4：对比分析法

```bash
# 对于间歇性问题

Claude: "对比分析..."

工作的情况 vs 失败的情况
├─ 输入差异
├─ 状态差异
├─ 环境差异
└─ 时间差异

找出关键差异点
```

---

## 常见问题

### Q1: 调试需要多长时间？

**A**: 取决于问题复杂度

- 简单问题：5-10 分钟
- 中等问题：15-30 分钟
- 复杂问题：30-60 分钟
- 但通常比试错快得多

### Q2: 必须完成所有 4 个阶段吗？

**A**: 是的，这是强制流程

```
✓ 阶段 1: 必须明确定义问题
✓ 阶段 2: 必须列出假设
✓ 阶段 3: 必须测试假设
✓ 阶段 4: 必须验证修复

跳过任何阶段都不符合 systematic-debugging
```

### Q3: 如果找不到根因怎么办？

**A**: 扩大搜索范围

```bash
Claude: "扩大搜索范围..."

1. 检查更多代码路径
2. 考虑外部依赖
3. 检查环境配置
4. 查看系统日志
5. 分析并发问题
6. 考虑版本差异
```

### Q4: 可以跳过测试直接修复吗？

**A**: 不推荐

```bash
❌ 跳过假设测试
→ 可能修复错误的假设
→ 问题没有解决
→ 浪费时间

✓ 完成假设测试
→ 确认真正的根因
→ 一次修复成功
→ 添加测试防止回归
```

### Q5: systematic-debugging 适合所有问题吗？

**A**: 适合大多数问题

```
✓ 适合：
- Bug 修复
- 错误诊断
- 性能问题
- 内存泄漏

✗ 不适合：
- 新功能开发（用 brainstorming）
- 代码重构（用 TDD）
- 架构设计（用 planning）
```

---

## 总结

### 核心价值

```
系统化调试 = 科学方法 + 强制流程 + 验证机制

✓ 找到真正的根因，不是症状
✓ 基于证据的决策
✓ 防止回归的测试
✓ 文档化的解决方案
```

### 与传统调试对比

```
传统调试：
试错 → 修复 → "看起来可以了" → 下次又出问题

systematic-debugging：
识别 → 假设 → 测试 → 验证 → 永久解决
```

### 使用建议

```
1. 信任流程
2. 提供充分上下文
3. 让 Claude 完成 4 个阶段
4. 利用测试防止回归
5. 记录学习过程
```

---

## 快速参考

```
触发方式：
- 自然描述问题
- "请使用 systematic-debugging"
- /superpowers:systematic-debugging

4 个阶段：
1. 问题识别（2-3分钟）
2. 假设形成（3-5分钟）
3. 假设测试（5-10分钟）
4. 解决方案（2-5分钟）

关键输出：
✓ 根因分析
✓ 修复代码
✓ 回归测试
✓ 文档更新

相关技能：
- verification-before-completion
- defense-in-depth
- root-cause-tracing
```

---

**维护者**: Claude Code Research Team
**最后更新**: 2025-12-27
**相关文档**:
- `docs/best-practices/superpowers-使用流程指南.md`
- `docs/best-practices/superpowers-最佳实践指南.md`
