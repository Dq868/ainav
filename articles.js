const ARTICLES = [
  {
    id: 'chatgpt-vs-claude-vs-gemini',
    title: 'ChatGPT vs Claude vs Gemini — 2026 最热 AI 助手横评',
    summary: '三大主流 AI 助手功能、价格、场景全面对比，帮你选最适合的那一个。',
    date: '2026-06-07',
    cat: 'chat',
    icon: '🏆',
    relatedTools: ['chatgpt', 'claude', 'gemini'],
    content: `
<p>2026 年，AI 助手已经成了很多人日常工作和学习的标配。ChatGPT、Claude、Gemini 这三款是最受关注的，但它们到底有什么区别？该怎么选？</p>

<h2>基本对比</h2>
<table>
  <tr><th>维度</th><th>ChatGPT</th><th>Claude</th><th>Gemini</th></tr>
  <tr><td>开发商</td><td>OpenAI</td><td>Anthropic</td><td>Google</td></tr>
  <tr><td>免费版</td><td>✅ 有（GPT-4o mini）</td><td>✅ 有（Sonnet）</td><td>✅ 有（Gemini 2.0 Flash）</td></tr>
  <tr><td>付费价格</td><td>$20/月（Plus）</td><td>$20/月（Pro）</td><td>$20/月（Advanced）</td></tr>
  <tr><td>上下文长度</td><td>128K</td><td>200K</td><td>1M</td></tr>
  <tr><td>联网搜索</td><td>✅ 需手动开启</td><td>✅ 自动</td><td>✅ 默认开启</td></tr>
  <tr><td>文件上传</td><td>✅ 图片/文档/代码</td><td>✅ 图片/文档</td><td>✅ 图片/文档/视频</td></tr>
</table>

<h2>各平台优势</h2>

<h3>ChatGPT — 生态最完整</h3>
<p>ChatGPT 的优势在于生态。GPTs 应用商店有大量别人做好的专用助手，直接拿来用。DALL·E 绘图、高级数据分析、语音对话都原生集成。适合大多数日常场景。</p>

<h3>Claude — 长文处理最强</h3>
<p>Claude 200K 上下文在同类中非常突出，可以一次性读完整本《三体》。对话风格更温和安全，回复结构清晰，适合写作、分析、代码审查这类需要深度思考的任务。Artifacts 功能可以直接生成可运行的代码和文档。</p>

<h3>Gemini — Google 生态集成</h3>
<p>Gemini 最大特色是和 Google 全家桶的深度集成：Gmail、Google Docs、YouTube 都能直接用。1M 上下文窗口能处理超大文件。免费版功能很全，性价比高。</p>

<h2>选哪个？</h2>
<p>如果你的预算只够一个：<strong>ChatGPT Plus</strong> 依然是综合最佳选择，应用场景最广。</p>
<p>如果你主要做写作和长文分析：<strong>Claude</strong> 更合适。</p>
<p>如果你是 Google 生态用户：<strong>Gemini</strong> 集成后体验很顺滑。</p>
<p>最省钱方案：三个都白嫖，不同场景切换着用。</p>
`
  },
  {
    id: 'ai-code-tools-comparison',
    title: 'AI 代码助手怎么选？Cursor / Copilot / Windsurf 横向对比',
    summary: '2026 年最主流的三个 AI 编程工具，哪个更适合你的开发场景？',
    date: '2026-06-07',
    cat: 'code',
    icon: '💻',
    relatedTools: ['cursor', 'copilot', 'windsurf'],
    content: `
<p>AI 代码助手已经成了程序员的新标配。Cursor、GitHub Copilot、Windsurf 是目前最受欢迎的三个选择。</p>

<h2>核心对比</h2>
<table>
  <tr><th>维度</th><th>Cursor</th><th>GitHub Copilot</th><th>Windsurf</th></tr>
  <tr><td>使用方式</td><td>独立 IDE</td><td>VS Code 插件</td><td>独立 IDE</td></tr>
  <tr><td>代码补全</td><td>✅</td><td>✅</td><td>✅</td></tr>
  <tr><td>多文件编辑</td><td>✅ Composer</td><td>✅ Copilot Chat</td><td>✅ Flow</td></tr>
  <tr><td>全项目理解</td><td>✅ 优秀</td><td>✅ 良好</td><td>✅ 优秀</td></tr>
  <tr><td>AI 模型选择</td><td>多模型（GPT-4o/Claude）</td><td>OpenAI 专属</td><td>多模型</td></tr>
  <tr><td>免费版</td><td>✅ 有限</td><td>✅ 有限</td><td>✅ 有限</td></tr>
  <tr><td>付费价格</td><td>$20/月</td><td>$10/月</td><td>$15/月</td></tr>
</table>

<h2>怎么选？</h2>

<p><strong>Cursor</strong> 是目前综合体验最好的。Composer 能一次改多个文件，理解项目上下文的能力很强。如果你愿意换个编辑器，Cursor 是最推荐的选择。</p>

<p><strong>GitHub Copilot</strong> 最大的优势是轻量——安装个插件就行，不用切换 IDE。如果你习惯了 VS Code 的工作流，不想换编辑器，Copilot 是最方便的选择。而且价格最便宜，$10/月。</p>

<p><strong>Windsurf</strong> 的 Flow 模式可以实现半自治的"代理"体验，你告诉他做什么，他自己改代码、跑命令。对新项目起步很有帮助。</p>

<h2>性价比建议</h2>
<p>从便宜到贵全用一遍：先用 Copilot（$10/月），体验不满意换 Windsurf（$15/月），最后上 Cursor（$20/月）。大多数场景 Cursor 值得多花那 $10。</p>
`
  },
  {
    id: 'free-ai-tools-2026',
    title: '10 个免费的 AI 工具，让你的工作效率翻倍',
    summary: '一分钱不花，用这些免费 AI 工具提升写代码、做图、写作的效率。',
    date: '2026-06-07',
    cat: 'other',
    icon: '🎁',
    relatedTools: ['deepseek', 'gemini', 'tongyi', 'jianying', 'suno'],
    content: `
<p>不一定非要付费才能用好 AI。下面这 10 个高质量的免费 AI 工具，覆盖了聊天、写作、图像、代码、视频等常见场景。</p>

<h2>1. DeepSeek — 最强的免费中文 AI 助手</h2>
<p>DeepSeek 是目前中文能力最好的免费大模型之一。深度思考模式可以处理复杂推理，联网搜索默认开启。支持文件上传分析。</p>

<h2>2. Gemini — Google 的免费多模态助手</h2>
<p>Gemini 免费版功能很全：文字、图像、代码都能处理。结合 Google 搜索获取实时信息。1M 上下文窗口能处理超长文档。</p>

<h2>3. 通义千问 — 阿里云的 AI 全家桶</h2>
<p>完全免费，支持文档处理、图像理解、代码生成。直接对接阿里云生态，读取 PDF、Excel、PPT 都很方便。</p>

<h2>4. 剪映 — 免费的视频编辑利器</h2>
<p>字节跳动的剪映内置了大量 AI 功能：智能字幕、AI 数字人、自动特效、曲线变速。国内用户的首选视频工具。</p>

<h2>5. GitHub Copilot 免费版</h2>
<p>2026 年 GitHub 为 VS Code 用户提供了受限的 Copilot 免费版，每月有限次数但日常够用。</p>

<h2>6. Flux — 开源的图像生成模型</h2>
<p>BlackForest Labs 的 Flux 模型完全开源，本地部署就能用。图像质量接近 Midjourney，完全免费。</p>

<h2>7. ComfyUI + Stable Diffusion</h2>
<p>节点式的 Stable Diffusion 界面，可本地运行。配合社区模型能做各种风格图像，不受任何 API 限制。</p>

<h2>8. Suno 免费版</h2>
<p>Suno 每天送一定数量的免费生成额度，文字描述就能生成完整歌曲。做配乐、Demo 都很方便。</p>

<h2>9. 秘塔 AI</h2>
<p>国内的无广告 AI 搜索引擎。搜索结果结构化清晰，有深度研究模式，适合学术和工作调研。</p>

<h2>10. Coze — 免费的 AI Bot 构建平台</h2>
<p>字节跳动出品，可视化编排 AI 智能体，支持插件、知识库、工作流。完全免费，发布不需要技术背景。</p>

<p>这 10 个工具加起来覆盖了大部分常见 AI 需求场景。先用免费的，等有更深入需求了再考虑升级付费版。</p>
`
  }
];
  {
    id: 'ai-video-generation-2026',
    title: '2026 AI 视频生成哪家强？可灵 / Vidu / Sora 对比实测',
    summary: '可灵 AI、Vidu、Sora、Runway 几大视频生成工具实测对比，看看哪个最能打。',
    date: '2026-06-09',
    cat: 'video',
    icon: '🎬',
    relatedTools: ['kling', 'vidu', 'sora', 'runway'],
    content: `
<p>AI 视频生成是 2025-2026 年最火热的 AI 赛道之一。国内的可灵 AI、Vidu，国外的 Sora、Runway 几家各有千秋。今天从几个常用维度做对比实测。</p>

<h2>对比一览</h2>
<table>
  <tr><th>维度</th><th>可灵 AI</th><th>Vidu</th><th>Sora</th><th>Runway</th></tr>
  <tr><td>开发商</td><td>快手</td><td>生数科技</td><td>OpenAI</td><td>Runway</td></tr>
  <tr><td>文生视频</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
  <tr><td>图生视频</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
  <tr><td>免费额度</td><td>每日免费</td><td>注册送积分</td><td>限时免费</td><td>免费试用</td></tr>
  <tr><td>最长时长</td><td>10 秒</td><td>8 秒</td><td>20 秒</td><td>10 秒</td></tr>
  <tr><td>中文理解</td><td>优秀</td><td>良好</td><td>一般</td><td>一般</td></tr>
</table>

<h2>实测感受</h2>

<p><strong>可灵 AI</strong>：国内首选，中文 prompt 理解准确，人物动作流畅度不错。运动控制功能让用户可以指定物体运动轨迹。视频质量在国产工具里属于第一梯队。</p>

<p><strong>Vidu</strong>：风格化能力强，可以生成动漫、绘画等多种风格的视频。速度较快，4K 清晰度高。适合创意内容制作。</p>

<p><strong>Sora</strong>：OpenAI 的王牌。虽然还没大规模开放，但从已发布的 demo 看，画面真实感和物理模拟能力是最强的。适合高端广告、影视级别的制作。</p>

<p><strong>Runway</strong>：功能最全面，除了视频生成还有绿幕抠图、运动追踪、视频修复等工具。Gen-3 模型画质提升明显。$12/月起的价格居中。</p>

<h2>推荐</h2>
<p>国内使用首选 <strong>可灵 AI</strong>，免费额度够用，中文友好。做创意视频可以搭配 <strong>Vidu</strong> 的多种风格。专业制作考虑 <strong>Runway</strong> 的全套工具链。</p>
`
  },
  {
    id: 'deepseek-vs-tongyi-vs-doubao',
    title: '国产 AI 大模型横评：DeepSeek / 通义千问 / 豆包 / Kimi 谁更强？',
    summary: '国内四大 AI 助手深度对比，中文能力、功能、价格一网打尽。',
    date: '2026-06-08',
    cat: 'chat',
    icon: '🇨🇳',
    relatedTools: ['deepseek', 'tongyi', 'doubao', 'kimi'],
    content: `
<p>国产大模型在 2025-2026 年进步显著。DeepSeek、通义千问、豆包、Kimi 四家各有所长，今天做个全面的对比测评。</p>

<h2>基本对比</h2>
<table>
  <tr><th>维度</th><th>DeepSeek</th><th>通义千问</th><th>豆包</th><th>Kimi</th></tr>
  <tr><td>开发商</td><td>深度求索</td><td>阿里云</td><td>字节跳动</td><td>月之暗面</td></tr>
  <tr><td>免费</td><td>✅ 完全免费</td><td>✅ 完全免费</td><td>✅ 完全免费</td><td>✅ 完全免费</td></tr>
  <tr><td>联网搜索</td><td>✅ 默认开启</td><td>✅ 手动开启</td><td>✅ 默认开启</td><td>✅ 默认开启</td></tr>
  <tr><td>文件上传</td><td>✅</td><td>✅</td><td>✅</td><td>✅</td></tr>
  <tr><td>上下文</td><td>64K</td><td>128K</td><td>128K</td><td>200K</td></tr>
  <tr><td>多模态</td><td>图像理解</td><td>图像+文档</td><td>图像+语音</td><td>图像+文档</td></tr>
  <tr><td>深度思考</td><td>✅ R1 模式</td><td>❌</td><td>❌</td><td>❌</td></tr>
</table>

<h2>各自优势</h2>

<h3>DeepSeek — 推理能力最强</h3>
<p>DeepSeek 的 R1 深度思考模式在复杂推理任务上表现亮眼，数学、逻辑、代码撰写能力在国产模型中属于顶尖水平。唯一支持"深度思考"功能的国产免费 AI。完全免费使用。</p>

<h3>通义千问 — 阿里全家桶</h3>
<p>依托阿里云生态，通义千问的文档处理能力很强，可以直接读取 PDF、Excel、PPT。多模态能力覆盖全面，还可以通过插件扩展功能。阿里系用户最方便。</p>

<h3>豆包 — 最接地气</h3>
<p>字节跳动的豆包凭借抖音、飞书等流量入口，用户量最大。语音交互体验好，集成在剪映里还能辅助视频创作。功能更新快、界面友好。</p>

<h3>Kimi — 长文档阅读</h3>
<p>月之暗面的 Kimi 以超长上下文著称，可以一次性处理超长文档。联网搜索能力强，特别适合做研究报告、论文分析类任务。</p>

<h2>总结</h2>
<p>四个全免费，不存在"选错了浪费钱"的问题。<strong>DeepSeek</strong> 适合深度推理和编程，<strong>通义千问</strong>适合阿里生态用户，<strong>豆包</strong>最方便日常，<strong>Kimi</strong>适合长文档阅读。建议四个都试试，不同场景切换着用。</p>
`
  },
];
