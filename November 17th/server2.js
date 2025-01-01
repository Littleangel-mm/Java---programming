const express = require('express');
const mysql = require('mysql2');
const bcrypt = require('bcryptjs');
const multer = require('multer');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();

// 设置端口号
const PORT = 5500;

// 解析请求体数据（用于接收表单数据）
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// 设置静态文件目录
app.use(express.static(path.join(__dirname, 'public')));

// 数据库连接配置
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'fl3692458121',
  database: 'xtsdb',
  port: 3306,
});

db.connect((err) => {
  if (err) {
    console.error('数据库连接失败: ' + err.stack);
    return;
  }
  console.log('已连接到数据库');
});

// 1. 托管静态文件（HTML、CSS、JS）
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'youtobe.html'));
});

//****************************************************************************************************************************** */
// 2. 配置视频上传文件夹
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'public\viode'); // 文件上传到 viode 文件夹
  },
  filename: (req, file, cb) => {
    const uniqueName = Date.now() + '-' + file.originalname; // 使用时间戳防止重名
    cb(null, uniqueName);
  },
});

const upload = multer({ storage: storage });

// 3. 上传视频接口
app.post('/upload', upload.single('public\viode'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ success: false, message: '未选择文件！' });
  }
  res.json({
    success: true,
    message: '视频上传成功！',
    filename: req.file.filename,
    path: `/viode/${req.file.filename}`,
  });
});
//*************************************************************************************************************** */

// 4. 注册接口（密码加密存储）
app.post('/register', (req, res) => {
  const { username, password } = req.body;

  // 检查用户名是否已存在
  db.query('SELECT * FROM xts_test WHERE username = ?', [username], (error, results) => {
    if (error) {
      console.error('查询失败: ' + error.stack);
      return res.status(500).json({ success: false, message: '查询失败' });
    }

    if (results.length > 0) {
      return res.json({ success: false, message: '用户名已存在' });
    }

    // 对密码进行加密
    bcrypt.hash(password, 10, (err, hashedPassword) => {
      if (err) {
        console.error('密码加密失败: ' + err.stack);
        return res.status(500).json({ success: false, message: '密码加密失败' });
      }

      // 插入新用户
      db.query('INSERT INTO xts_test (username, password) VALUES (?, ?)', [username, hashedPassword], (error, results) => {
        if (error) {
          console.error('注册失败: ' + error.stack);
          return res.status(500).json({ success: false, message: '注册失败' });
        }

        res.json({ success: true, message: '注册成功' });
      });
    });
  });
});

// 5. 登录接口（密码比较）
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  // 查询数据库中的用户
  db.query('SELECT * FROM xts_test WHERE username = ?', [username], (error, results) => {
    if (error) {
      console.error('查询失败: ' + error.stack);
      return res.status(500).json({ success: false, message: '数据库查询失败' });
    }

    if (results.length === 0) {
      return res.json({ success: false, message: '用户名不存在' });
    }

    // 获取查询到的用户信息
    const user = results[0];

    // 使用 bcrypt 比较密码
    bcrypt.compare(password, user.password, (err, isMatch) => {
      if (err) {
        console.error('密码验证失败: ' + err.stack);
        return res.status(500).json({ success: false, message: '密码验证失败' });
      }

      if (isMatch) {
        // 登录成功
        res.json({
          success: true,
          message: '登录成功！',
          user: user, // 返回用户信息
        });
      } else {
        // 密码不匹配
        res.json({ success: false, message: '密码错误' });
      }
    });
  });
});

// 6. 错误处理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('服务器错误！');
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器已启动：http://localhost:${PORT}`);
});

