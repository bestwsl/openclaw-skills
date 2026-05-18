---
name: zero-language
description: Zero - Vercel Labs 出品的专为 AI Agent 设计的系统编程语言，具有显式效果系统、可预测内存和结构化编译器输出
category: software-development
---

# Zero 编程语言 — The Programming Language for Agents

**GitHub**: https://github.com/vercel-labs/zero  
**Stars**: ⭐ ~2000  
**License**: Apache-2.0  

## 项目简介

Zero 是 Vercel Labs 开发的一款专为 AI Agent 设计的系统编程语言。核心设计理念是为 Agent 提供一种可预测、显式表达效果、内存行为清晰的编译型语言。

### 核心设计原则

- **显式效果（Explicit Effects）**：外部操作（IO、内存分配等）在类型系统中显式标记
- **可预测内存（Predictable Memory）**：无 GC，编译期可知的内存布局和生命周期
- **结构化编译输出（Structured Compiler Output）**：编译器输出 JSON 等结构化格式
- **小型原生工具（Small Native Tools）**：编译为静态链接可执行文件，体积小、启动快

## 快速上手

### 1. 编写第一个程序

创建 `hello.0`：

```zero
pub fun main(world: World) -> Void raises {
    check world.out.write("hello from zero\n")
}
```

运行检查和执行：

```bash
zero check hello.0
zero run hello.0
```

### 2. 基本语法

**函数与变量**：

```zero
fun answer() -> i32 {
    return 40 + 2
}

pub fun main(world: World) -> Void raises {
    let value = answer()
    if value == 42 {
        check world.out.write("math works\n")
    } else {
        check world.out.write("math broke\n")
    }
}
```

**结构体（shape）**：

```zero
shape Point {
    x: i32,
    y: i32,
}

fun sum(point: Point) -> i32 {
    return point.x + point.y
}

pub fun main(world: World) -> Void raises {
    let point = Point { x: 40, y: 2 }
    let total = sum(point)
    check world.out.write("point works\n")
}
```

## 关键命令

| 命令 | 用途 |
|------|------|
| `zero check <file>` | 类型检查 |
| `zero run <file>` | 编译并运行 |
| `zero build --emit exe --target <target> <file>` | 编译为静态可执行文件 |
| `zero graph --json <package>` | 依赖图输出（JSON） |
| `zero size --json <file>` | 二进制大小分析（JSON） |
| `zero routes --json <package>` | 路由分析（JSON） |
| `zero skills get zero --full` | 获取 Zero 技能定义 |
| `zero doctor --json` | 诊断环境 |
| `zero new cli <name>` | 创建新项目 |
| `zero test .` | 运行测试 |

## 语言特性

- **shape 系统**：类似 struct 的数据类型
- **显式效果系统**：函数签名标记 `raises` 表示可抛出错误
- **World 对象**：通过参数传递的显式能力，替代全局变量
- **check 关键字**：处理可能失败的操作
- **无全局状态**：所有外部资源通过参数传递
- **编译器输出 JSON**：便于 Agent 编程

## 适用场景

1. **AI Agent 编写工具**：Agent 可用 Zero 编写小型原生工具
2. **系统编程教学**：语法简洁清晰
3. **WebAssembly / 边缘计算**：可编译为 Wasm 目标
4. **CLI 工具开发**：静态链接可执行文件，分发方便
5. **需要显式效果控制**：IO 操作在类型系统中标记

## 学习资源

- 官方文档站点：克隆仓库后运行 `npm run docs:dev`
- 示例代码：`examples/` 目录含 70+ 示例文件
- VSCode 扩展：`extensions/vscode/` 提供 `.0` 语法高亮

## 注意事项

- 项目仍处于实验阶段，语言设计可能变化
- 目前仅支持 Linux x86-64 目标
- Windows 和 macOS 支持尚在开发中
