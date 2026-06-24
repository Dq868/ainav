// ========== 分类 ==========
const CATEGORIES = [
  { id: 'all', label: '🏠 全部' },
  { id: 'chat', label: '💬 聊天对话' },
  { id: 'image', label: '🎨 图像生成' },
  { id: 'code', label: '💻 代码开发' },
  { id: 'video', label: '🎬 视频创作' },
  { id: 'audio', label: '🎵 音频处理' },
  { id: 'office', label: '📋 办公效率' },
  { id: 'search', label: '🔍 搜索知识' },
  { id: 'other', label: '🧩 其他工具' },
];

// ========== 工具数据 ==========
const TOOLS = [
  {
    id: 'auferet', name: 'Auferet', url: 'https://auferet.com',
    desc: '免费 AI 角色扮演游戏，AI 游戏主持人能记住你的世界与上传的设定。',
    cat: 'other', icon: '🎲', tags: ['freemium'],
    useCases: ['单人角色扮演冒险', '无需真人主持的桌游战役', '与好友协作讲故事'],
    features: ['持久记忆（事件库与角色库）', '上传自定义设定', '支持 5e 与 Pathfinder 2e', '骰子与数值追踪', '单人或多人游玩']
  },
  // -- 聊天对话 --
  {
    id: 'chatgpt', name: 'ChatGPT', url: 'https://chat.openai.com',
    desc: 'OpenAI 旗下 AI 对话助手，支持多模态推理与内容生成。',
    cat: 'chat', icon: '🤖', tags: ['freemium', '热门'],
    useCases: ['日常问答与写作', '代码编写与调试', '数据分析与图表', '多语言翻译', '创意头脑风暴'],
    features: ['多模态识别（文字/图像/语音）', 'GPTs 自定义智能体', '联网搜索', '文件上传分析', '4o/4o-mini 模型可选'],
    related: ['claude', 'gemini', 'deepseek']
  },
  {
    id: 'claude', name: 'Claude', url: 'https://claude.ai',
    desc: 'Anthropic 的 AI 助手，擅长长文本理解和安全对话。',
    cat: 'chat', icon: '🧠', tags: ['freemium', '热门'],
    useCases: ['长文档分析', '学术论文阅读', '代码审查', '复杂推理任务'],
    features: ['200K 超长上下文', 'Artifacts 内容生成', '安全对齐', 'Project 项目管理'],
    related: ['chatgpt', 'gemini', 'deepseek']
  },
  {
    id: 'gemini', name: 'Gemini', url: 'https://gemini.google.com',
    desc: 'Google 的多模态 AI，支持文字、图像、代码、音频。',
    cat: 'chat', icon: '✨', tags: ['free', '热门'],
    useCases: ['多模态内容分析', 'Google 生态集成', '写作辅助', '编程帮助'],
    features: ['多模态原生支持', 'Google 应用集成', '免费使用', 'Gemini Advanced 进阶版'],
    related: ['chatgpt', 'claude', 'perplexity']
  },
  {
    id: 'deepseek', name: 'DeepSeek', url: 'https://chat.deepseek.com',
    desc: '深度求索的大语言模型，中文能力强，支持联网搜索。',
    cat: 'chat', icon: '🌊', tags: ['free', '热门'],
    useCases: ['中文对话', '编程辅助', '联网搜索问答', '文件分析'],
    features: ['深度思考模式', '中文优化', '联网搜索', '免费使用', '文件上传'],
    related: ['chatgpt', 'kimi', 'tongyi']
  },
  {
    id: 'doubao', name: '豆包', url: 'https://www.doubao.com',
    desc: '字节跳动旗下 AI 对话助手，集成在抖音、飞书等生态。',
    cat: 'chat', icon: '🫘', tags: ['free'],
    useCases: ['日常对话', '文案写作', '学习辅助', '娱乐互动'],
    features: ['多端覆盖', '抖音生态集成', '语音交互', '免费使用'],
    related: ['kimi', 'deepseek', 'tongyi']
  },
  {
    id: 'kimi', name: 'Kimi', url: 'https://kimi.moonshot.cn',
    desc: '月之暗面出品，擅长超长上下文处理，中文友好。',
    cat: 'chat', icon: '🌙', tags: ['free'],
    useCases: ['超长文档阅读', '论文分析', '联网搜索', '内容总结'],
    features: ['超长上下文窗口', '联网搜索', '文件解析', '中文场景优化'],
    related: ['deepseek', 'doubao', 'chatgpt']
  },
  {
    id: 'tongyi', name: '通义千问', url: 'https://tongyi.aliyun.com',
    desc: '阿里云自研大模型，支持文档、代码、图像理解。',
    cat: 'chat', icon: '🧘', tags: ['free'],
    useCases: ['办公文档处理', '编程帮助', '图像理解', '数据分析'],
    features: ['阿里云生态', '多模态', '文档处理', '免费使用'],
    related: ['deepseek', 'kimi', 'wenxin']
  },
  {
    id: 'wenxin', name: '文心一言', url: 'https://yiyan.baidu.com',
    desc: '百度知识增强大语言模型，融合文心大模型能力。',
    cat: 'chat', icon: '📖', tags: ['free'],
    useCases: ['知识问答', '文案创作', '百度生态集成', '办公辅助'],
    features: ['百度搜索增强', '文心大模型', '多模态理解', '插件生态'],
    related: ['tongyi', 'deepseek', 'chatgpt']
  },
  {
    id: 'zhipu', name: '智谱清言', url: 'https://chatglm.cn',
    desc: '智谱 AI 基于 GLM 模型的对话助手，支持多轮对话。',
    cat: 'chat', icon: '💡', tags: ['free'],
    useCases: ['学术研究', '编程辅助', '内容生成', '数据分析'],
    features: ['GLM 模型', '多轮对话', '代码能力', '学术场景优化'],
    related: ['deepseek', 'kimi', 'chatgpt']
  },
  {
    id: 'perplexity', name: 'Perplexity', url: 'https://www.perplexity.ai',
    desc: 'AI 搜索引擎，直接给出带引用的回答。',
    cat: 'chat', icon: '🔎', tags: ['freemium'],
    useCases: ['深度搜索', '学术调研', '事实核查', '研究报告'],
    features: ['实时引用来源', 'Pro 搜索', '文件上传分析', 'Collections 收藏'],
    related: ['chatgpt', 'gemini', 'consensus']
  },
  // -- 图像生成 --
  {
    id: 'midjourney', name: 'Midjourney', url: 'https://www.midjourney.com',
    desc: '顶尖 AI 图像生成工具，艺术风格出众。',
    cat: 'image', icon: '🎨', tags: ['paid'],
    useCases: ['艺术创作', '概念设计', '游戏原画', '品牌视觉'],
    features: ['超高质量输出', '风格多样化', 'Discord 工作流', 'V6 模型'],
    related: ['dalle', 'stable-diffusion', 'leonardo']
  },
  {
    id: 'dalle', name: 'DALL·E 3', url: 'https://openai.com/dall-e-3',
    desc: 'OpenAI 文字生成图像模型，集成于 ChatGPT。',
    cat: 'image', icon: '🖼️', tags: ['paid'],
    useCases: ['创意插图', '产品设计', '社交媒体配图', '视觉概念'],
    features: ['ChatGPT 集成', '文字渲染', '高精度提示词跟随', '安全过滤'],
    related: ['midjourney', 'stable-diffusion', 'ideogram']
  },
  {
    id: 'stable-diffusion', name: 'Stable Diffusion', url: 'https://stability.ai',
    desc: '开源图像生成模型，可本地部署，社区生态丰富。',
    cat: 'image', icon: '🌈', tags: ['free', '开源'],
    useCases: ['本地图像生成', '模型微调', 'AI 研究', '批量生成'],
    features: ['完全开源', '本地部署', 'LoRA 微调', 'ControlNet', '社区模型'],
    related: ['comfyui', 'fooocus', 'flux']
  },
  {
    id: 'comfyui', name: 'ComfyUI', url: 'https://www.comfy.org',
    desc: '基于节点工作流的 Stable Diffusion 图形界面。',
    cat: 'image', icon: '🔗', tags: ['free', '开源'],
    useCases: ['复杂图像工作流', '视频生成', '批处理', '模型测试'],
    features: ['节点式工作流', '模块化设计', 'GPU 加速', '插件生态'],
    related: ['stable-diffusion', 'fooocus', 'flux']
  },
  {
    id: 'leonardo', name: 'Leonardo AI', url: 'https://leonardo.ai',
    desc: '游戏资产与创意图像生成平台。',
    cat: 'image', icon: '🎮', tags: ['freemium'],
    useCases: ['游戏资产设计', '角色概念', '场景原画', '纹理生成'],
    features: ['游戏资产优化', '实时生成', '模型训练', 'API 接口'],
    related: ['midjourney', 'ideogram', 'dalle']
  },
  {
    id: 'fooocus', name: 'Fooocus', url: 'https://github.com/lllyasviel/Fooocus',
    desc: '极简 Stable Diffusion 前端，一键出图。',
    cat: 'image', icon: '🖌️', tags: ['free', '开源'],
    useCases: ['快速图像生成', '新手入门', '风格探索', '本地创作'],
    features: ['一键安装', '自动优化参数', '内置风格库', '低硬件要求'],
    related: ['stable-diffusion', 'comfyui', 'flux']
  },
  {
    id: 'ideogram', name: 'Ideogram', url: 'https://ideogram.ai',
    desc: '文字渲染优秀，擅长 Logo 和排版图像。',
    cat: 'image', icon: '🔤', tags: ['freemium'],
    useCases: ['Logo 设计', '排版海报', '文字艺术', '品牌设计'],
    features: ['精准文字渲染', 'Logo 生成', '风格一致性', '高分辨率'],
    related: ['midjourney', 'dalle', 'leonardo']
  },
  {
    id: 'flux', name: 'Flux', url: 'https://blackforestlabs.ai',
    desc: 'BlackForest Labs 出品的高质量图像生成模型。',
    cat: 'image', icon: '⚡', tags: ['free', '开源'],
    useCases: ['高质量图像生成', '设计原型', '创意视觉', '商业应用'],
    features: ['开源模型', '高速生成', '高美学质量', '提示词准确'],
    related: ['stable-diffusion', 'midjourney', 'dalle']
  },
  // -- 代码开发 --
  {
    id: 'copilot', name: 'GitHub Copilot', url: 'https://github.com/features/copilot',
    desc: 'AI 代码补全助手，深度集成 VS Code 等 IDE。',
    cat: 'code', icon: '🧑‍💻', tags: ['paid', '热门'],
    useCases: ['代码自动补全', '单元测试生成', '代码审查', '文档编写'],
    features: ['实时代码补全', '多 IDE 支持', 'Copilot Chat', 'PR 描述生成'],
    related: ['cursor', 'tabnine', 'windsurf']
  },
  {
    id: 'cursor', name: 'Cursor', url: 'https://cursor.sh',
    desc: 'AI 优先的代码编辑器，内置多模型对话能力。',
    cat: 'code', icon: '📟', tags: ['freemium', '热门'],
    useCases: ['全栈开发', '代码重构', 'Bug 调试', '项目脚手架'],
    features: ['多模型切换', '整库代码库理解', 'Agent 模式', 'Composer 多文件编辑'],
    related: ['copilot', 'windsurf', 'codex']
  },
  {
    id: 'windsurf', name: 'Windsurf', url: 'https://codeium.com/windsurf',
    desc: 'Codeium 出品的 AI 驱动 IDE，支持 Flow 模式。',
    cat: 'code', icon: '🏄', tags: ['freemium'],
    useCases: ['智能代码补全', '多文件重构', '终端集成', '代码审查'],
    features: ['Flow 代理模式', '深度代码索引', '多语言支持', '免费套餐'],
    related: ['cursor', 'copilot', 'continue']
  },
  {
    id: 'codex', name: 'Codex', url: 'https://codex.so',
    desc: '基于 GPT-5 的 AI 编程助手。',
    cat: 'code', icon: '📝', tags: ['freemium'],
    useCases: ['全栈开发', '项目规划', '代码审查', '技术研究'],
    features: ['GPT-5 驱动', '深度上下文', '工具集成', '多文件编辑'],
    related: ['cursor', 'copilot', 'claude']
  },
  {
    id: 'v0', name: 'v0', url: 'https://v0.dev',
    desc: 'Vercel 的 AI 前端生成工具，文字描述生成 UI。',
    cat: 'code', icon: '🎯', tags: ['freemium'],
    useCases: ['前端组件生成', '页面原型', 'React 开发', 'Tailwind 设计'],
    features: ['文字转 UI', 'React/Next.js 输出', '可视化编辑', '迭代优化'],
    related: ['cursor', 'bolt', 'replit']
  },
  {
    id: 'replit', name: 'Replit Agent', url: 'https://replit.com',
    desc: 'AI 驱动的在线开发环境，可自动生成完整应用。',
    cat: 'code', icon: '🔄', tags: ['freemium'],
    useCases: ['快速原型开发', '学习编程', '全栈应用', '部署上线'],
    features: ['在线 IDE', 'AI Agent 自动编程', '一键部署', '协作编辑'],
    related: ['bolt', 'v0', 'cursor']
  },
  {
    id: 'bolt', name: 'Bolt.new', url: 'https://bolt.new',
    desc: '浏览器内 AI 全栈开发工具，即时预览与部署。',
    cat: 'code', icon: '⚡', tags: ['freemium'],
    useCases: ['全栈开发', '快速原型', '技术学习', 'MVP 搭建'],
    features: ['浏览器内开发', '即时预览', '全栈支持', '一键部署'],
    related: ['replit', 'v0', 'cursor']
  },
  {
    id: 'devin', name: 'Devin', url: 'https://cognition.ai',
    desc: 'Cognition 出品的 AI 软件工程师，自主完成任务。',
    cat: 'code', icon: '🤖', tags: ['paid'],
    useCases: ['自主编程', 'Bug 修复', '代码迁移', '自动化开发'],
    features: ['自主完成任务', '终端操作', '浏览器操作', '多工具集成'],
    related: ['cursor', 'copilot', 'codex']
  },
  {
    id: 'tabnine', name: 'Tabnine', url: 'https://www.tabnine.com',
    desc: 'AI 代码补全，支持本地模型，注重隐私。',
    cat: 'code', icon: '📌', tags: ['freemium'],
    useCases: ['隐私优先代码补全', '本地模型推理', '企业开发'],
    features: ['本地模型', '隐私保护', '多 IDE 支持', '自定义模型'],
    related: ['copilot', 'continue', 'cursor']
  },
  {
    id: 'continue', name: 'Continue', url: 'https://continue.dev',
    desc: '开源 AI 代码助手，可接入任意 LLM。',
    cat: 'code', icon: '▶️', tags: ['free', '开源'],
    useCases: ['自建 AI 编码助手', '多模型切换', '代码审查'],
    features: ['完全开源', '任意 LLM 接入', 'VS Code/JetBrains', '自定义规则'],
    related: ['copilot', 'tabnine', 'codex']
  },
  // -- 视频创作 --
  {
    id: 'sora', name: 'Sora', url: 'https://sora.com',
    desc: 'OpenAI 视频生成模型，文字/图像生成高质量视频。',
    cat: 'video', icon: '🎥', tags: ['paid'],
    useCases: ['短视频创作', '广告制作', '概念演示', '视觉叙事'],
    features: ['文字转视频', '图像转视频', '真实物理模拟', '多风格输出'],
    related: ['runway', 'pika', 'kling']
  },
  {
    id: 'runway', name: 'Runway Gen-3', url: 'https://runwayml.com',
    desc: '专业级 AI 视频生成与编辑平台。',
    cat: 'video', icon: '🎬', tags: ['paid'],
    useCases: ['专业视频编辑', '特效生成', '动态视频创作'],
    features: ['Gen-3 Alpha', '视频到视频', '绿幕抠像', '运动笔刷'],
    related: ['sora', 'pika', 'heygen']
  },
  {
    id: 'heygen', name: 'HeyGen', url: 'https://www.heygen.com',
    desc: 'AI 数字人视频生成，支持多语言口型同步。',
    cat: 'video', icon: '👤', tags: ['paid'],
    useCases: ['数字人演讲', '多语言视频', '营销视频', '教育培训'],
    features: ['数字人定制', '多语言口型同步', '语音克隆', '模板库'],
    related: ['runway', 'pika', 'capcut']
  },
  {
    id: 'pika', name: 'Pika', url: 'https://pika.art',
    desc: '轻松生成和编辑视频，支持多种风格。',
    cat: 'video', icon: '🦊', tags: ['freemium'],
    useCases: ['快速视频生成', '视频风格化', '社交媒体剪辑'],
    features: ['多风格生成', '视频编辑器', '文字提示驱动', '免费套餐'],
    related: ['runway', 'sora', 'kling']
  },
  {
    id: 'jianying', name: '剪映', url: 'https://jyy.capcut.cn',
    desc: '字节跳动视频编辑工具，内置丰富 AI 功能。',
    cat: 'video', icon: '✂️', tags: ['free', '热门'],
    useCases: ['短视频编辑', 'AI 数字人', '自动字幕', '特效制作'],
    features: ['AI 数字人', '智能字幕', '曲线变速', '海量模板', '免费使用'],
    related: ['capcut', 'pika', 'runway']
  },
  {
    id: 'capcut', name: 'CapCut', url: 'https://www.capcut.com',
    desc: '剪映国际版，AI 视频剪辑与特效平台。',
    cat: 'video', icon: '✂️', tags: ['free'],
    useCases: ['视频剪辑', 'AI 特效', '字幕生成', '多平台导出'],
    features: ['AI 驱动编辑', '多平台同步', '云端协作', '模板市场'],
    related: ['jianying', 'runway', 'pika']
  },
  {
    id: 'kling', name: 'Kling', url: 'https://kling.kuaishou.com',
    desc: '快手 AI 视频生成模型，支持图生视频。',
    cat: 'video', icon: '🦜', tags: ['free'],
    useCases: ['图生视频', '文字生视频', '短视频创作'],
    features: ['高质量视频生成', '图生视频', '物理模拟', '免费使用'],
    related: ['sora', 'pika', 'vidu']
  },
  {
    id: 'vidu', name: 'Vidu', url: 'https://www.vidu.cn',
    desc: '生数科技自研视频生成大模型。',
    cat: 'video', icon: '🎞️', tags: ['freemium'],
    useCases: ['视频生成', '动态设计', '创意短片'],
    features: ['自研架构', '高一致性', '多风格', '快速生成'],
    related: ['kling', 'sora', 'pika']
  },
  // -- 音频处理 --
  {
    id: 'elevenlabs', name: 'ElevenLabs', url: 'https://elevenlabs.io',
    desc: 'AI 语音合成，声音逼真，支持多语言多情感。',
    cat: 'audio', icon: '🗣️', tags: ['freemium'],
    useCases: ['有声书制作', '配音旁白', '语音助手', '多语言播报'],
    features: ['语音克隆', '情感控制', '多语言支持', '语音转语音'],
    related: ['whisper', 'iflyrec', 'suno']
  },
  {
    id: 'suno', name: 'Suno', url: 'https://suno.com',
    desc: 'AI 音乐生成，文字描述即可生成完整歌曲。',
    cat: 'audio', icon: '🎵', tags: ['freemium', '热门'],
    useCases: ['音乐创作', '配乐制作', '歌曲 Demo', '背景音乐'],
    features: ['文字生歌', '多种音乐风格', '人声生成', '歌词控制'],
    related: ['udio', 'elevenlabs', 'jianying']
  },
  {
    id: 'udio', name: 'Udio', url: 'https://www.udio.com',
    desc: 'AI 音乐创作平台，高质量音频生成。',
    cat: 'audio', icon: '🎶', tags: ['freemium'],
    useCases: ['音乐创作', '编曲辅助', 'Demo 制作'],
    features: ['高质量音频', '风格多样', '歌词生成', '延展创作'],
    related: ['suno', 'elevenlabs', 'jianying']
  },
  {
    id: 'whisper', name: 'Whisper', url: 'https://openai.com/whisper',
    desc: 'OpenAI 开源语音识别模型，支持多语种。',
    cat: 'audio', icon: '🎤', tags: ['free', '开源'],
    useCases: ['语音转文字', '会议记录', '字幕生成', '多语言翻译'],
    features: ['开源免费', '多语种识别', '高准确率', '本地部署'],
    related: ['elevenlabs', 'iflyrec', 'otter']
  },
  {
    id: 'iflyrec', name: '讯飞听见', url: 'https://www.iflyrec.com',
    desc: '科大讯飞语音转文字，会议记录与字幕生成。',
    cat: 'audio', icon: '📄', tags: ['freemium'],
    useCases: ['会议转写', '字幕制作', '录音整理', '同声传译'],
    features: ['高精度识别', '多语种', '行业词库', '云端同步'],
    related: ['whisper', 'otter', 'jianying']
  },
  // -- 办公效率 --
  {
    id: 'notion-ai', name: 'Notion AI', url: 'https://www.notion.so/product/ai',
    desc: '智能写作助手，嵌入 Notion 工作空间。',
    cat: 'office', icon: '📝', tags: ['paid'],
    useCases: ['智能写作', '内容总结', '项目管理', '知识库管理'],
    features: ['Notion 原生集成', 'AI 写作辅助', '自动总结', '翻译改写'],
    related: ['wps-ai', 'feishu', 'gamma']
  },
  {
    id: 'gamma', name: 'Gamma', url: 'https://gamma.app',
    desc: 'AI 自动生成演示文稿、文档和网页。',
    cat: 'office', icon: '📊', tags: ['freemium'],
    useCases: ['演示文稿制作', '文档编写', '网页生成', '商业提案'],
    features: ['AI 自动生成', '精美模板', '一键换主题', '协作编辑'],
    related: ['beautiful-ai', 'notion-ai', 'wps-ai']
  },
  {
    id: 'feishu', name: '飞书智能伙伴', url: 'https://www.feishu.cn',
    desc: '飞书内置 AI 助手，辅助写作、总结、问答。',
    cat: 'office', icon: '📎', tags: ['freemium'],
    useCases: ['会议纪要', '文档写作', '信息总结', '日程管理'],
    features: ['飞书原生集成', '会议总结', '文档问答', '多维表格 AI'],
    related: ['notion-ai', 'wps-ai', 'iflyrec']
  },
  {
    id: 'grammarly', name: 'Grammarly', url: 'https://www.grammarly.com',
    desc: 'AI 英文写作助手，语法检查与风格优化。',
    cat: 'office', icon: '✍️', tags: ['freemium'],
    useCases: ['英文写作校对', '语法纠错', '风格优化', '学术写作'],
    features: ['实时语法检查', '风格建议', '查重检测', '全平台集成'],
    related: ['chatgpt', 'claude', 'notion-ai']
  },
  {
    id: 'beautiful-ai', name: 'Beautiful.ai', url: 'https://www.beautiful.ai',
    desc: 'AI 设计幻灯片，自动排版与美化。',
    cat: 'office', icon: '📐', tags: ['paid'],
    useCases: ['幻灯片设计', '商业演示', '品牌模板'],
    features: ['智能排版', '品牌一致性', '协作分享', '模板库'],
    related: ['gamma', 'notion-ai', 'wps-ai']
  },
  {
    id: 'wps-ai', name: 'WPS AI', url: 'https://ai.wps.cn',
    desc: '金山办公 AI 助手，支持文档、表格、演示。',
    cat: 'office', icon: '📄', tags: ['freemium'],
    useCases: ['文档写作', 'PPT 生成', '表格处理', 'PDF 分析'],
    features: ['WPS 原生集成', '多组件支持', '文档生成', 'AI 校对'],
    related: ['feishu', 'notion-ai', 'gamma']
  },
  {
    id: 'otter', name: 'Otter.ai', url: 'https://otter.ai',
    desc: 'AI 会议记录与实时转写工具。',
    cat: 'office', icon: '🦦', tags: ['freemium'],
    useCases: ['会议记录', '实时转写', '会议摘要', '录音整理'],
    features: ['实时转写', '自动摘要', '关键词提取', '多平台'],
    related: ['iflyrec', 'whisper', 'feishu']
  },
  {
    id: 'xinghuo', name: '讯飞星火', url: 'https://xinghuo.xfyun.cn',
    desc: '科大讯飞大模型，办公、学习、编程多场景。',
    cat: 'office', icon: '🔥', tags: ['free'],
    useCases: ['智能问答', '编程辅助', '办公写作', '学习辅导'],
    features: ['文本生成', '多模态', '语音交互', '免费使用'],
    related: ['deepseek', 'tongyi', 'chatgpt']
  },
  // -- 搜索知识 --
  {
    id: 'mieta', name: '秘塔 AI', url: 'https://metaso.cn',
    desc: '中国 AI 搜索引擎，无广告，结构化的搜索结果。',
    cat: 'search', icon: '🗼', tags: ['free'],
    useCases: ['学术搜索', '知识问答', '信息调研', '文档查找'],
    features: ['无广告搜索', '结构化结果', '深度研究模式', '免费使用'],
    related: ['perplexity', 'tiangong', 'consensus']
  },
  {
    id: 'tiangong', name: '天工 AI', url: 'https://www.tiangong.cn',
    desc: '昆仑万维 AI 搜索助手，支持联网。',
    cat: 'search', icon: '⚙️', tags: ['free'],
    useCases: ['联网搜索', '资讯获取', '知识问答', '信息整合'],
    features: ['联网搜索', '多模态', '长文本生成', '免费'],
    related: ['mieta', 'perplexity', 'deepseek']
  },
  {
    id: 'consensus', name: 'Consensus', url: 'https://consensus.app',
    desc: 'AI 学术搜索引擎，从论文中提炼答案。',
    cat: 'search', icon: '📚', tags: ['freemium'],
    useCases: ['学术文献搜索', '论文问答', '研究助理', '文献综述'],
    features: ['论文引用提取', 'Study Snapshots', '引用导出', '研究追踪'],
    related: ['elicit', 'scispace', 'perplexity']
  },
  {
    id: 'elicit', name: 'Elicit', url: 'https://elicit.com',
    desc: 'AI 研究助手，自动提取论文关键信息。',
    cat: 'search', icon: '🔬', tags: ['freemium'],
    useCases: ['论文筛选', '文献综述', '研究问题解答', '数据提取'],
    features: ['智能论文筛选', '数据自动提取', '文献总结', '研究问答'],
    related: ['consensus', 'scispace', 'perplexity']
  },
  {
    id: 'scispace', name: 'SciSpace', url: 'https://scispace.com',
    desc: 'AI 论文阅读与解释工具，辅助科研。',
    cat: 'search', icon: '📖', tags: ['freemium'],
    useCases: ['论文解读', '公式解释', '文献分析', '研究辅助'],
    features: ['论文解析', 'AI 问答', '参考文献管理', '协作批注'],
    related: ['elicit', 'consensus', 'perplexity']
  },
  // -- 其他 --
  {
    id: 'huggingface', name: 'Hugging Face', url: 'https://huggingface.co',
    desc: 'AI 模型与数据集社区，托管大量开源模型。',
    cat: 'other', icon: '🤗', tags: ['free', '开源', '热门'],
    useCases: ['模型托管与发现', '数据集浏览', 'AI 研究', 'Demo 展示'],
    features: ['模型社区', 'Spaces 演示', '数据集托管', 'Inference API'],
    related: ['replicate', 'dify', 'coze']
  },
  {
    id: 'replicate', name: 'Replicate', url: 'https://replicate.com',
    desc: '云端 AI 模型运行平台，API 调用各类模型。',
    cat: 'other', icon: '🔄', tags: ['freemium'],
    useCases: ['模型 API 调用', 'AI 应用开发', '模型测试', '批量推理'],
    features: ['云端 GPU', '按量计费', 'Python SDK', '模型浏览'],
    related: ['huggingface', 'dify', 'coze']
  },
  {
    id: 'poe', name: 'Poe', url: 'https://poe.com',
    desc: '集成多款 AI 聊天机器人的平台。',
    cat: 'other', icon: '📱', tags: ['freemium'],
    useCases: ['多模型体验', 'Bot 订阅', '聊天对比', '移动端使用'],
    features: ['多模型集成', 'Bot 创建', '付费订阅', '移动 App'],
    related: ['chatgpt', 'claude', 'gemini']
  },
  {
    id: 'coze', name: 'Coze', url: 'https://www.coze.com',
    desc: '字节跳动 AI Bot 开发平台，可自定义智能体。',
    cat: 'other', icon: '🧩', tags: ['free'],
    useCases: ['AI Bot 开发', '工作流自动化', '知识库构建', '插件制作'],
    features: ['可视化编排', '插件系统', '知识库', '多渠道发布', '免费'],
    related: ['dify', 'huggingface', 'poe']
  },
  {
    id: 'dify', name: 'Dify', url: 'https://dify.ai',
    desc: '开源 LLM 应用开发平台，可视化编排。',
    cat: 'other', icon: '⚗️', tags: ['free', '开源'],
    useCases: ['LLM 应用开发', 'RAG 构建', 'Agent 开发', '工作流编排'],
    features: ['开源可自部署', '可视化编排', 'RAG 引擎', '多模型接入'],
    related: ['coze', 'huggingface', 'replicate']
  },
  {
    id: 'figma-ai', name: 'Figma AI', url: 'https://www.figma.com/ai',
    desc: 'Figma 设计工具内置 AI 功能，生成 UI 组件。',
    cat: 'other', icon: '🖍️', tags: ['freemium'],
    useCases: ['UI 组件生成', '设计原型', '图标创作', '设计稿转代码'],
    features: ['Figma 原生集成', 'AI 生成 UI', '智能图层命名', '自动切图'],
    related: ['v0', 'midjourney', 'ideogram']
  },
  // -- 2026 新增工具 --
  {
    id: 'manus', name: 'Manus', url: 'https://manus.im',
    desc: '通用 AI Agent，可自主完成复杂的多步骤任务。',
    cat: 'other', icon: '🤖', tags: ['new', '热门'],
    useCases: ['自动化任务', '数据分析', '报告生成', '多步骤工作流'],
    features: ['自主 Agent', '多工具调用', '任务规划', '结果交付'],
    related: ['dify', 'coze', 'autoai']
  },
  {
    id: 'autoai', name: 'AutoAI', url: 'https://autoai.com',
    desc: 'AI 自动化平台，让重复工作自动完成。',
    cat: 'other', icon: '⚡', tags: ['new'],
    useCases: ['工作流自动化', '数据抓取', '报告生成', '定时任务'],
    features: ['可视化工作流', 'AI 驱动', '多平台集成', '定时执行'],
    related: ['manus', 'dify', 'coze']
  },
  {
    id: 'grok', name: 'Grok', url: 'https://grok.com',
    desc: 'xAI 出品的 AI 助手，实时连接 X 平台数据。',
    cat: 'chat', icon: '🚀', tags: ['new', '热门'],
    useCases: ['实时新闻分析', 'X 平台数据', '幽默对话', '深度研究'],
    features: ['X 平台实时数据', '深度研究模式', '图像理解', '语音交互'],
    related: ['chatgpt', 'claude', 'perplexity']
  },
  {
    id: 'ideogram', name: 'Ideogram', url: 'https://ideogram.ai',
    desc: 'AI 图像生成，文字渲染能力出色。',
    cat: 'image', icon: '🖼️', tags: ['new', '热门'],
    useCases: ['Logo 设计', '海报制作', '文字排版图像', '品牌视觉'],
    features: ['文字渲染', '风格控制', '高分辨率', 'Remix 功能'],
    related: ['midjourney', 'dalle', 'flux']
  },
  {
    id: 'recraft', name: 'Recraft', url: 'https://recraft.ai',
    desc: 'AI 设计工具，可生成矢量图、图标、品牌素材。',
    cat: 'image', icon: '🎯', tags: ['new'],
    useCases: ['矢量图生成', '图标设计', '品牌素材', 'UI 设计'],
    features: ['矢量图输出', '风格一致性', '品牌色管理', 'SVG 导出'],
    related: ['ideogram', 'midjourney', 'figma-ai']
  },
  {
    id: 'kling', name: '可灵 AI', url: 'https://kling.kuaishou.com',
    desc: '快手出品的视频生成模型，支持文本/图像转视频。',
    cat: 'video', icon: '🎞️', tags: ['new', '热门'],
    useCases: ['文生视频', '图生视频', '短视频创作', '广告素材'],
    features: ['高清视频生成', '运动控制', '风格化', '中文场景优化'],
    related: ['sora', 'runway', 'pika']
  },
  {
    id: 'vidu', name: 'Vidu', url: 'https://www.vidu.cn',
    desc: '生数科技的视频生成工具，支持多种创作模式。',
    cat: 'video', icon: '🎥', tags: ['new'],
    useCases: ['视频创作', '动画制作', '广告制作', '内容营销'],
    features: ['文生视频', '图生视频', '风格迁移', '快速生成'],
    related: ['kling', 'runway', 'pika']
  },
  {
    id: 'minimax', name: 'MiniMax', url: 'https://www.minimaxi.com',
    desc: 'AI 视频与音频生成平台，海螺 AI 视频能力突出。',
    cat: 'video', icon: '🐚', tags: ['new'],
    useCases: ['视频生成', '语音合成', '对话 AI', '音乐创作'],
    features: ['视频生成', 'TTS 语音', '大语言模型', '音乐生成'],
    related: ['kling', 'suno', 'vidu']
  },
  {
    id: 'elevenlabs', name: 'ElevenLabs', url: 'https://elevenlabs.io',
    desc: 'AI 语音合成，支持多语言、情感化的语音生成。',
    cat: 'audio', icon: '🎙️', tags: ['new', '热门'],
    useCases: ['语音合成', '有声书制作', '配音', '语音克隆'],
    features: ['情感语音', '多语言', '语音克隆', '声音库'],
    related: ['fish-audio', 'suno', 'voicebox']
  },
  {
    id: 'fish-audio', name: 'Fish Audio', url: 'https://fish.audio',
    desc: '开源 AI 语音合成工具，支持语音克隆与 TTS。',
    cat: 'audio', icon: '🐟', tags: ['new', '开源'],
    useCases: ['语音合成', '语音克隆', '配音制作', '有声内容'],
    features: ['开源', '语音克隆', '多语言', 'API 接入', '免费额度'],
    related: ['elevenlabs', 'suno', 'voicebox']
  },
  {
    id: 'udio', name: 'Udio', url: 'https://www.udio.com',
    desc: 'AI 音乐生成，支持歌词、风格、乐器控制。',
    cat: 'audio', icon: '🎶', tags: ['new', '热门'],
    useCases: ['音乐创作', '配乐制作', '歌曲生成', 'Demo 制作'],
    features: ['高质量音乐', '歌词控制', '风格选择', '音频编辑'],
    related: ['suno', 'elevenlabs', 'riffusion']
  },
  {
    id: 'bolt', name: 'Bolt.new', url: 'https://bolt.new',
    desc: 'AI 全栈 Web 应用生成器，从描述到部署。',
    cat: 'code', icon: '⚡', tags: ['new', '热门'],
    useCases: ['快速原型', '全栈开发', 'MVP 构建', 'Web 应用生成'],
    features: ['全栈生成', '实时预览', '代码可导出', '一键部署'],
    related: ['v0', 'lovable', 'cursor']
  },
  {
    id: 'lovable', name: 'Lovable', url: 'https://lovable.dev',
    desc: 'AI 应用构建器，自然语言描述生成完整应用。',
    cat: 'code', icon: '💕', tags: ['new'],
    useCases: ['Web 应用生成', '数据库集成', '用户认证', '全栈应用'],
    features: ['自然语言构建', 'Supabase 集成', '用户系统', '代码导出'],
    related: ['bolt', 'v0', 'replit-agent']
  },
  {
    id: 'replit-agent', name: 'Replit Agent', url: 'https://replit.com',
    desc: 'Replit 的 AI 编程代理，浏览器内全栈开发。',
    cat: 'code', icon: '🔮', tags: ['new'],
    useCases: ['云端开发', '快速原型', '协作编程', '部署上线'],
    features: ['浏览器 IDE', 'AI Agent', '一键部署', '协作编辑'],
    related: ['bolt', 'lovable', 'cursor']
  },
  {
    id: 'granica', name: 'Granica', url: 'https://granica.ai',
    desc: 'AI 数据处理平台，优化数据管道与成本。',
    cat: 'office', icon: '📊', tags: ['new'],
    useCases: ['数据管道', '成本优化', '数据治理', 'AI 数据准备'],
    features: ['数据压缩', '成本分析', '存储优化', 'AI 集成'],
    related: ['notion-ai', 'gamma', 'beautiful']
  },
  {
    id: 'gamma', name: 'Gamma', url: 'https://gamma.app',
    desc: 'AI 演示文稿生成，从大纲到精美幻灯片。',
    cat: 'office', icon: '📑', tags: ['new', '热门'],
    useCases: ['PPT 生成', '演示文稿', '报告制作', '提案设计'],
    features: ['AI 生成', '美观模板', '在线协作', '多格式导出'],
    related: ['beautiful', 'notion-ai', 'canva']
  },
  {
    id: 'beautiful', name: 'Beautiful.ai', url: 'https://www.beautiful.ai',
    desc: 'AI 智能排版 PPT，内容决定设计。',
    cat: 'office', icon: '✨', tags: ['new'],
    useCases: ['PPT 设计', '品牌模板', '团队协作', '演示制作'],
    features: ['智能排版', '品牌一致性', '团队协作', '在线编辑'],
    related: ['gamma', 'canva', 'notion-ai']
  },
  {
    id: 'notion-ai', name: 'Notion AI', url: 'https://www.notion.so/product/ai',
    desc: 'Notion 内置 AI，写作、总结、知识管理。',
    cat: 'office', icon: '📝', tags: ['new', '热门'],
    useCases: ['智能写作', '文档总结', '知识库管理', '项目协作'],
    features: ['AI 写作助手', '自动总结', '知识问答', 'Notion 集成'],
    related: ['gamma', 'beautiful', 'granica']
  },
  {
    id: 'microsoft-copilot', name: 'Microsoft Copilot', url: 'https://copilot.microsoft.com',
    desc: '微软 AI 助手，集成 Office 365 与 Windows。',
    cat: 'office', icon: '🪟', tags: ['new', '热门'],
    useCases: ['Office 自动化', 'Windows 辅助', '会议总结', '文档处理'],
    features: ['Office 集成', 'Windows 集成', '会议摘要', 'DALL·E 绘图'],
    related: ['notion-ai', 'chatgpt', 'gemini']
  },
  {
    id: 'heygen', name: 'HeyGen', url: 'https://www.heygen.com',
    desc: 'AI 数字人视频生成，支持多语言口型同步。',
    cat: 'video', icon: '👤', tags: ['new', '热门'],
    useCases: ['数字人视频', '多语言配音', '营销视频', '培训视频'],
    features: ['数字人生成', '口型同步', '多语言翻译', '视频模板'],
    related: ['kling', 'runway', 'vidu']
  },
  {
    id: 'veed', name: 'VEED.io', url: 'https://www.veed.io',
    desc: '在线视频编辑平台，AI 字幕、翻译、剪辑。',
    cat: 'video', icon: '✂️', tags: ['new'],
    useCases: ['视频编辑', '字幕生成', '多语言翻译', '视频压缩'],
    features: ['在线剪辑', 'AI 字幕', '自动翻译', '录屏编辑'],
    related: ['heygen', 'jieshi', 'canva']
  },
  {
    id: 'jieshi', name: '即事 AI', url: 'https://jishi.ai',
    desc: 'AI 视频剪辑工具，智能识别片段自动剪辑。',
    cat: 'video', icon: '🎬', tags: ['new'],
    useCases: ['自动剪辑', '精彩片段提取', '短视频制作', '直播切片'],
    features: ['智能识别', '自动剪辑', '模板生成', '批量处理'],
    related: ['veed', 'jianying', 'runway']
  },
  {
    id: 'check-ai', name: 'Check AI', url: 'https://check-ai.com',
    desc: 'AI 内容检测与事实核查工具。',
    cat: 'search', icon: '✅', tags: ['new'],
    useCases: ['事实核查', 'AI 内容识别', '信息验证', '来源追踪'],
    features: ['AI 检测', '事实核实', '来源分析', '偏见识别'],
    related: ['perplexity', 'consensus', 'elicit']
  },
];

// ========== 导出 ==========

// ========== 用户提交工具 ==========
const SUBMISSIONS_KEY = 'ainav_user_submissions';

function getUserSubmissions() {
  try { return JSON.parse(localStorage.getItem(SUBMISSIONS_KEY)) || []; }
  catch { return []; }
}

function saveUserSubmission(tool) {
  const subs = getUserSubmissions();
  tool.id = 'user-' + Date.now();
  tool.addedAt = new Date().toISOString();
  subs.push(tool);
  localStorage.setItem(SUBMISSIONS_KEY, JSON.stringify(subs));
  return tool;
}

function getAllTools() {
  return [...TOOLS, ...getUserSubmissions()];
}

function getToolById(id) {
  return getAllTools().find(t => t.id === id);
}

function getToolsByCategory(catId) {
  if (catId === 'all') return getAllTools();
  return getAllTools().filter(t => t.cat === catId);
}

function getRelatedTools(tool, limit = 4) {
  if (!tool.related || tool.related.length === 0) {
    return getToolsByCategory(tool.cat).filter(t => t.id !== tool.id).slice(0, limit);
  }
  return tool.related.map(id => getToolById(id)).filter(Boolean).slice(0, limit);
}

// ========== URL 工具 ==========
function getDetailUrl(toolId) {
  return '/tool/' + toolId;
}

function getLocalDetailUrl(toolId) {
  return 'detail.html?tool=' + toolId;
}
