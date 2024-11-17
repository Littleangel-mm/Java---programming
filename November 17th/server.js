const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

// 设置端口号
const PORT = 5500;

// 1. 托管静态文件（HTML、CSS、JS）
// app.use(express.static('public'));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'youtobe.html'));
});
//静态资源加载
// app.use(express.static('public'));
app.use(express.static(path.join(__dirname, 'public')));


//****************************************************************************************************************************** */
// 2. 配置视频上传文件夹
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'viode'); // 文件上传到 viode 文件夹
  },
  filename: (req, file, cb) => {
    const uniqueName = Date.now() + '-' + file.originalname; // 使用时间戳防止重名
    cb(null, uniqueName);
  },
});

const upload = multer({ storage: storage });

// 3. 上传视频接口
app.post('/upload', upload.single('video'), (req, res) => {
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


// 4. 错误处理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('服务器错误！');
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器已启动：http://localhost:${PORT}`);
});







