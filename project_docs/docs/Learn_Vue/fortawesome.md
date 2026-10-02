##### 📚 Install & Setup Vue Libraries

### 5️⃣ Font Awesome

### 1️⃣ Install 📚

```cmd
npm i --save @fortawesome/fontawesome-svg-core @fortawesome/vue-fontawesome@latest @fortawesome/vue-fontawesome@prerelease @fortawesome/free-solid-svg-icons @fortawesome/free-brands-svg-icons @fortawesome/free-regular-svg-icons
```

### 2️⃣ Setup 🛠️

#### Import Inside main.js

```js
// Font Awesome
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
// Add Free Icons Styles To SVG Core
library.add(fas, far, fab);
```

```js
// eslint-disable-next-line vue/multi-word-component-names
app.component("fa", FontAwesomeIcon);
```
