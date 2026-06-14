---
name: politics
description: 政治 RAG 知识库、Coze 时政查询。维护或扩展政治能力时使用。
---

# Politics Skill

## 两个子系统
- **politics_knowledge**：Markdown → embedding → 向量检索 → Qwen RAG 回答
- **current_affairs**：Coze 子智能体（时政热点、近期政策）

## 边界
- 问知识点（矛盾、辩证法）→ RAG
- 问近期时政 → Coze
- 无法判断 → Coze（Coze 能答静态知识，RAG 不能答新时事）

## 知识库
- 源文件：`data/raw/politics/*.md`
- 向量：`data/processed/politics_vectors.jsonl`
- 切块 700 字符，text-embedding-v4 1024 维，cosine similarity
- 构建：`python scripts/build_politics_db.py`

## RAG 约束
模型严格限于参考资料，不得编造案例或年份。资料不足时明确说明。
