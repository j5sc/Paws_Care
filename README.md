# 🐾 萌爪管家

这是一个面向养宠人群(猫狗为主、兼顾其他常见家养宠物)的智能客服项目,基于 RAG + ReAct Agent 架构。

## 功能
- **日常饲养咨询**:基于 4 份养宠知识库(养宠 100 问、健康 200 条、用品选购 200 条、维护保养 200 条)做精准检索回答
- **真实天气**:接 wttr.in,中英文城市名,支持天气对宠物饲养的影响类问题
- **月度使用报告**:基于外部 records.csv,自动汇总指定用户的宠物使用情况
- **多会话切换**:侧栏支持新建 / 切换 / 重命名 / 删除多个会话
- **流式输出**:Agent 回复逐字流式渲染,体验更自然

## 技术栈
- LangChain + LangGraph Agent
- Chroma 向量库 + bge 嵌入模型
- Streamlit 1.61 前端
- wttr.in 天气 API(免 key)

## 目录结构
```
├── app.py                 # Streamlit 入口
├── agent/                 # ReAct Agent 定义 + 工具 + 中间件
├── rag/                   # RAG 检索服务 + Chroma 封装
├── model/                 # 模型工厂(LLM / Embedding)
├── prompts/               # 系统提示词 / 报告提示词 / RAG 提示词
├── config/                # YAML 配置
├── data/                  # 知识库 PDF/TXT + 外部数据 CSV
├── chroma_db/             # 向量库持久化目录
└── utils/                 # 配置加载 / 日志 / 路径 / 文件处理 / 天气客户端
```

## 运行
```bash
pip install pypdf
streamlit run app.py
```
