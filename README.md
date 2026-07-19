<h1 align="center"><samp>Tan Jian Ron</samp></h1>

<p align="center">
  <img src="assets/profile-cube.png" width="200" alt="spinning cube made of my profile picture">
</p>

<p align="center"><samp>Computer Science @ NUS · SRE intern @ CPF Board · Singapore</samp></p>

<p align="center">
  <a href="mailto:jianrontan101@gmail.com"><img src="https://img.shields.io/badge/Email-jianrontan101%40gmail.com-EA4335?style=flat&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://allin.jianrontan.com"><img src="https://img.shields.io/badge/AllIn-allin.jianrontan.com-232F3E?style=flat&logo=cloudflare&logoColor=F38020" alt="AllIn live site"></a>
  <a href="https://chess.jianrontan.com"><img src="https://img.shields.io/badge/Chess-chess.jianrontan.com-4169E1?style=flat&logo=lichess&logoColor=white" alt="Chess live site"></a>
  <img src="https://img.shields.io/badge/Based%20in-Singapore-ED2939?style=flat" alt="Singapore">
</p>

## <samp>About</samp>

<samp>I'm Ron, a Computer Science undergraduate at NUS. Currently an SRE intern at the Central Provident Fund Board, working on Terraform, AKS, and Azure DevOps pipelines for systems serving 4M+ CPF members. Also Vice-Chair of NUS Sheares Web, where I lead 16 developers shipping a hall intranet and React Native app used by 400+ residents.</samp>

## <samp>Projects</samp>

### <samp>♠️ AllIn: heads-up poker AI</samp>

<a href="https://github.com/jianrontan/AllIn">
  <img src="https://opengraph.githubassets.com/1/jianrontan/AllIn" alt="AllIn repo card" width="20%">
</a>

<samp>A poker bot you can actually play, live at **[allin.jianrontan.com](https://allin.jianrontan.com)**.</samp>

- <samp>Trained a **200K info-set CFR blueprint over 50M self-play iterations** for heads-up play.</samp>
- <samp>On high-stakes river decisions it doesn't just read the blueprint: a **safe, blueprint-anchored solver runs CFR live** to approximate game-theory-optimal play in real time.</samp>
- <samp>Productionised end to end: Flask/gunicorn API on **AWS Lightsail** behind **Cloudflare**, with DynamoDB, ECR, and SQLite.</samp>
- <samp>CI/CD via **GitHub Actions with OIDC** (no long-lived AWS keys) and multi-stage Docker builds tested against a prod-equivalent image.</samp>

### <samp>♟️ Chess explanation engine</samp>

<a href="https://github.com/jianrontan/Chess">
  <img src="https://opengraph.githubassets.com/1/jianrontan/Chess" alt="Chess repo card" width="20%">
</a>

<samp>Engines tell you the best move; they can't tell you *why*. This is a **RAG pipeline that grounds LLM chess explanations in Stockfish analysis and retrieved human commentaries**, so the explanation matches what the engine actually sees. Live at **[chess.jianrontan.com](https://chess.jianrontan.com)**.</samp>

## <samp>Stack</samp>

**<samp>Languages</samp>**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Java-007396?style=flat" alt="Java">
  <img src="https://img.shields.io/badge/SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL">
</p>

**<samp>Infrastructure</samp>**

<p>
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white" alt="AWS">
  <img src="https://img.shields.io/badge/Azure-0078D4?style=flat" alt="Azure">
  <img src="https://img.shields.io/badge/Terraform-844FBA?style=flat&logo=terraform&logoColor=white" alt="Terraform">
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/GitLab%20CI-FC6D26?style=flat&logo=gitlab&logoColor=white" alt="GitLab CI">
  <img src="https://img.shields.io/badge/Cloudflare-F38020?style=flat&logo=cloudflare&logoColor=white" alt="Cloudflare">
</p>

**<samp>Web & data</samp>**

<p>
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/React%20Native-61DAFB?style=flat&logo=react&logoColor=black" alt="React Native">
  <img src="https://img.shields.io/badge/Node.js-339933?style=flat&logo=nodedotjs&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Supabase-3FCF8E?style=flat&logo=supabase&logoColor=white" alt="Supabase">
  <img src="https://img.shields.io/badge/DynamoDB-4053D6?style=flat&logo=amazondynamodb&logoColor=white" alt="DynamoDB">
</p>

<details>
<summary><samp>Where I've used all this</samp></summary>
<br>

- <samp>**CPF Board**: Azure GCC infra and CI/CD: Terraform provisioning, AKS, Azure DevOps pipeline templates across non-prod and prod.</samp>
- <samp>**NUS Sheares Web**: GitHub Actions CI/CD with Liquibase schema migrations and a plan/apply data pipeline on Postgres; AWS infra with SST (CloudFront, Lambda SSR, S3), isolated preprod/prod on Supabase.</samp>
- <samp>**Screening Eagle | Proceq**: Cross-platform E2E test framework (Playwright + TypeScript, 10+ device/browser configs on BrowserStack, GitLab CI); 100+ regression cases automated with Python and AltTester.</samp>
- <samp>**TES Capital**: AI document automation (ChatGPT API, n8n, React, Flask): OCR + prompt workflows turning unstructured insurance data into standardised policy documents at 95% accuracy.</samp>
- <samp>**Hysses**: Full-stack ops platform (React, Node.js, Express, MySQL, Docker) with a custom NetSuite↔MySQL integration API.</samp>

</details>

<!-- Stats hidden until the public github-readme-stats instance is reliable (or self-hosted)

## <samp>Stats</samp>

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=jianrontan&show_icons=true&theme=tokyonight&hide_border=true">
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api?username=jianrontan&show_icons=true&theme=default&hide_border=true">
    <img alt="Jian Ron's GitHub stats" src="https://github-readme-stats.vercel.app/api?username=jianrontan&show_icons=true&hide_border=true">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=jianrontan&layout=compact&theme=tokyonight&hide_border=true&hide=html,css,jupyter%20notebook">
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=jianrontan&layout=compact&theme=default&hide_border=true&hide=html,css,jupyter%20notebook">
    <img alt="Top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=jianrontan&layout=compact&hide_border=true&hide=html,css,jupyter%20notebook">
  </picture>
</p>

-->

---

<p align="center"><samp> Computer Science @ NUS ·  <a href="mailto:jianrontan101@gmail.com">jianrontan101@gmail.com</a></samp></p>
