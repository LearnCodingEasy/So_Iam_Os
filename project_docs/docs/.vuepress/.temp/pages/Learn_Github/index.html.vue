<template><div><h1 id="github" tabindex="-1"><a class="header-anchor" href="#github"><span>Github</span></a></h1>
<h2 id="_0️⃣1️-create-repository" tabindex="-1"><a class="header-anchor" href="#_0️⃣1️-create-repository"><span>0️⃣1️ Create Repository</span></a></h2>
<p><img src="@source/Images/Github/Create_Repository.gif" alt="This is an image"></p>
<h2 id="_0️⃣2️⃣-clone-repository" tabindex="-1"><a class="header-anchor" href="#_0️⃣2️⃣-clone-repository"><span>0️⃣2️⃣ Clone Repository</span></a></h2>
<h6 id="📁-git-clone-project" tabindex="-1"><a class="header-anchor" href="#📁-git-clone-project"><span>📁 Git Clone Project</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">git clone https://github.com/LearnCodingEasy/YourRepositoryName.git</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h6 id="📁-project-readmap" tabindex="-1"><a class="header-anchor" href="#📁-project-readmap"><span>📁 Project Readmap</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📦Project</span>
<span class="line">┣ 📁.git</span>
<span class="line">┣ 📜README.md</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p><img src="@source/Images/Github/Clone.gif" alt="This is an image"></p>
<h2 id="_0️⃣3️⃣-create-file-gitignore" tabindex="-1"><a class="header-anchor" href="#_0️⃣3️⃣-create-file-gitignore"><span>0️⃣3️⃣ Create File Gitignore</span></a></h2>
<h6 id="📝-create-file-gitignore" tabindex="-1"><a class="header-anchor" href="#📝-create-file-gitignore"><span>📝 Create File Gitignore</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">.gitignore</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">touch .gitignore</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h6 id="📁-project-readmap-1" tabindex="-1"><a class="header-anchor" href="#📁-project-readmap-1"><span>📁 Project Readmap</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📁Project</span>
<span class="line">┣ 📁 .git</span>
<span class="line">┣ 📜 .gitignore</span>
<span class="line">┣ 📜 README.md</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h6 id="🖊️-write-inside-file-gitignore" tabindex="-1"><a class="header-anchor" href="#🖊️-write-inside-file-gitignore"><span>🖊️ Write Inside File [gitignore]</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">node_modules/</span>
<span class="line">project_docs/</span>
<span class="line"></span>
<span class="line">venv/</span>
<span class="line"></span>
<span class="line">.env</span>
<span class="line">*.env</span>
<span class="line">.env.local</span>
<span class="line">.env.production</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="_0️⃣4️⃣-review-changes" tabindex="-1"><a class="header-anchor" href="#_0️⃣4️⃣-review-changes"><span>0️⃣4️⃣ Review Changes</span></a></h2>
<h6 id="📋-review-changes-and-formulate-change-action" tabindex="-1"><a class="header-anchor" href="#📋-review-changes-and-formulate-change-action"><span>📋 Review changes and formulate change action</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">git status</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_0️⃣5️⃣-add-changes" tabindex="-1"><a class="header-anchor" href="#_0️⃣5️⃣-add-changes"><span>0️⃣5️⃣ Add Changes</span></a></h2>
<h6 id="📂-add-all-new-and-changed-files-to-the-staging-area" tabindex="-1"><a class="header-anchor" href="#📂-add-all-new-and-changed-files-to-the-staging-area"><span>📂 Add all new and changed files to the Staging Area.</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">git add *</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_0️⃣6️⃣-commit-changes" tabindex="-1"><a class="header-anchor" href="#_0️⃣6️⃣-commit-changes"><span>0️⃣6️⃣ Commit Changes</span></a></h2>
<h6 id="💾-this-command-sends-the-file-from-the-staging-area-to-the-local-repo" tabindex="-1"><a class="header-anchor" href="#💾-this-command-sends-the-file-from-the-staging-area-to-the-local-repo"><span>💾 This command sends the file from the Staging Area to the Local Repo.</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">git commit -m &quot;Commit Explain Code&quot;</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_0️⃣7️⃣-who-you-are" tabindex="-1"><a class="header-anchor" href="#_0️⃣7️⃣-who-you-are"><span>0️⃣7️⃣ Who You Are</span></a></h2>
<h6 id="please-tell-me-who-you-are" tabindex="-1"><a class="header-anchor" href="#please-tell-me-who-you-are"><span>Please tell me who you are.</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">git config --global user.name "Hossam Rashad"</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">git config --global user.email "learncodingeasy@yahoo.com"</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_0️⃣8️⃣-push-changes" tabindex="-1"><a class="header-anchor" href="#_0️⃣8️⃣-push-changes"><span>0️⃣8️⃣ Push Changes</span></a></h2>
<h6 id="🌐-this-command-sends-files-from-local-repo-to-remote-repo" tabindex="-1"><a class="header-anchor" href="#🌐-this-command-sends-files-from-local-repo-to-remote-repo"><span>🌐 This command sends files from (Local Repo) to (Remote Repo).</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">git push origin main</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_0️⃣9️⃣-online-project" tabindex="-1"><a class="header-anchor" href="#_0️⃣9️⃣-online-project"><span>0️⃣9️⃣ Online Project</span></a></h2>
<h6 id="go-to" tabindex="-1"><a class="header-anchor" href="#go-to"><span>Go To</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">https://dash.cloudflare.com/ead902dc7582ff64dbe07564003280c3/workers-and-pages/create/pages</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_1️⃣0️⃣" tabindex="-1"><a class="header-anchor" href="#_1️⃣0️⃣"><span>1️⃣0️⃣</span></a></h2>
</div></template>


