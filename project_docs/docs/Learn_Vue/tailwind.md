### 📚 Install & Setup Vue Libraries [ Tailwind ]

### 1️⃣ Install 📚

```cmd
npm install -D tailwindcss@3 postcss autoprefixer
```

```cmd
npx tailwindcss init -p
```

### 2️⃣ Setup 🛠️

- 📝 File [ tailwind.config.js ]

```js
// ...
content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
// ...
```

### 3️⃣ Create Folder And File

- 📝 Create File [ tailwind.css ] Inside [ src\assets\Tailwind\tailwind.css ]

```
Tailwind\tailwind.css
```

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";
```

### 4️⃣ Import

- Import File Inside [main.js]

```js
// Tailwind
import "./assets/Tailwind/tailwind.css";
import "tailwindcss/tailwind.css";
```
