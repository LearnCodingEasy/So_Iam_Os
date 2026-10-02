##### 📚 Install & Setup Vue Libraries

#### 4️⃣ Axios

### 1️⃣ Install 📚

```cmd
npm install axios
```

### 2️⃣ Setup 🛠️

#### Import Inside main.js

```js
import axios from "axios";
axios.defaults.baseURL = "http://127.0.0.1:8000";
```

#### During development أثناء التطوير

```
ipconfig
```

```js
import axios from "axios";
axios.defaults.baseURL = "http://192.168.1.3:8000";
```

```js
// Axios تفعيل التوجيه و
app.use(router, axios);
```
