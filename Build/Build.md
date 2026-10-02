# File Create Project Build.md

## Step 1

- 🖥️ Create Virtual Environment 🐍

```
python -m venv venv
```

- 🖥️ Activate Virtual Environment 🐍

```
venv\Scripts\activate
```

- 🖥️ Install Django 🔧

```
pip install django
```

- 💡 Start Project

```
django-admin startproject backend_django
```

```
cd backend_django
```

## Vue

### 🖥️ Create Vue Project

###### 📁 Create Vue Project

```
npm create vue@latest
```

###### 🚀 Choose Vite [ Project name & Select a framework] 🛠️

```

(venv) D:\So_Iam_Os>npm create vue@latest

> npx
> create-vue

┌  Vue.js - The Progressive JavaScript Framework
│
◆  Project name (target directory):
│  frontend_vue

```

```

(venv) D:\So_Iam_Os>npm create vue@latest

> npx
> create-vue

┌  Vue.js - The Progressive JavaScript Framework
│
◇  Project name (target directory):
│  frontend_vue
│
◆  Use TypeScript?
│  ○ Yes / ● No
└

```

```

(venv) D:\So_Iam_Os>npm create vue@latest

> npx
> create-vue

┌  Vue.js - The Progressive JavaScript Framework
│
◇  Project name (target directory):
│  frontend_vue
│
◇  Use TypeScript?
│  No
│
◆  Select features to include in your project: (↑/↓ to
│  navigate, space to select, a to toggle all, enter to
│  confirm)
│  ◻ JSX Support
│  ◼ Router (SPA development)
│  ◼ Pinia (state management)
│  ◼ Vitest (unit testing)
│  ◻ End-to-End Testing
│  ◼ Linter (error prevention)
│  ◼ Prettier (code formatting)
│  ↑/↓ to navigate • Space: select • Enter: confirm
└
```

```cmd
(venv) D:\So_Iam_Os>npm create vue@latest

> npx
> create-vue

┌  Vue.js - The Progressive JavaScript Framework
│
│
◇  Select features to include in your project: (↑/↓ to
│  navigate, space to select, a to toggle all, enter to
│  confirm)
│  Router (SPA development), Pinia (state management),
│  Vitest (unit testing), Linter (error prevention),
│  Prettier (code formatting)
│
◇  Select experimental features to include in your
│  project: (↑/↓ to navigate, space to select, a to
│  toggle all, enter to confirm)
│  none
│
◆  Skip all example code and start with a blank Vue
│  project?
│  ○ Yes / ● No
└

```

```
(venv) D:\So_Iam_Os>npm create vue@latest

> npx
> create-vue

┌  Vue.js - The Progressive JavaScript Framework
│
│
◇  Select features to include in your project: (↑/↓ to
│  navigate, space to select, a to toggle all, enter to
│  confirm)
│  Router (SPA development), Pinia (state management),
│  Vitest (unit testing), Linter (error prevention),
│  Prettier (code formatting)
│
◇  Select experimental features to include in your
│  project: (↑/↓ to navigate, space to select, a to
│  Router (SPA development), Pinia (state management),
│  Vitest (unit testing), Linter (error prevention),
│  Prettier (code formatting)
│
◇  Select experimental features to include in your
│  project: (↑/↓ to navigate, space to select, a to
│  toggle all, enter to confirm)
│  none
│
◇  Skip all example code and start with a blank Vue
│  project?
│  No

Scaffolding project in D:\So_Iam_Os\frontend_vue...
│
└  Done. Now run:

   cd frontend_vue
   npm install
   npm run format
   npm run dev

| Optional: Initialize Git in your project directory with:

   git init && git add -A && git commit -m "initial commit"


(venv) D:\So_Iam_Os>
```

### 📂 Go To Project

```cmd
cd frontend_vue
```

### 📂 Install

```cmd
npm install
```

### 📂 format

```cmd
npm run format
```

### 📦 Build Vue Project

```cmd
npm run build
```

### ✅ Run Vue Project

```cmd
npm run dev
```

```cmd
npm run dev -- --host
```

### 📦 Django Libraries

#### 👥 User Authentication and Registration

```cmd
pip install djangorestframework
```

```cmd
pip install djangorestframework-simplejwt
```

```cmd
pip install djoser
```

```cmd
pip install django-cors-headers
```

#### 📸 Images

```cmd
pip install pillow requests
```

#### 🔒 Decouple

```cmd
pip install python-decouple
```

#### 🗄️ PostgreSQL 🐘

```cmd
pip install psycopg2
```

```cmd
pip install psycopg2-binary
```

#### 🐞 Debug

```cmd
pip install django-debug-toolbar
```

#### 🖨️ Console

```cmd
pip install rich
```

#### 📋 Document APIs

```cmd
pip install drf-spectacular
```

#### 🕸️ Scraper

```cmd
pip install beautifulsoup4
```

🕸️ Automation

```cmd
pip install pyautogui
```

```cmd
pip install pywinauto
```

```cmd
pip install opencv-python
```

### 📲 Start App

###### Start App

```cmd
cd backend_django
```

```cmd
python manage.py startapp users_accounts
```

```cmd
python manage.py startapp social
```

```cmd
python manage.py startapp notification
```

```cmd
python manage.py startapp core
```

```cmd
python manage.py startapp projects
```

```cmd
python manage.py startapp challenges
```

```cmd
python manage.py startapp tasks
```

```cmd
python manage.py startapp goals
```

```cmd
python manage.py startapp learning
```

```cmd
python manage.py startapp knowledge
```

```cmd
python manage.py startapp memory
```

```cmd
python manage.py startapp ai
```

```cmd
python manage.py startapp vendor
```

```cmd
python manage.py startapp product
```

```cmd
python manage.py startapp client
```

```cmd
python manage.py startapp scraper
```

```cmd
python manage.py startapp sheets
```

```cmd
python manage.py startapp automation
```

```cmd
python manage.py startapp mcp_server
```

```cmd
python manage.py startapp jobs_opportunity
```
