// 简单的搜索功能
document.querySelector('.search-bar').addEventListener('input', function(event) {
  const searchQuery = event.target.value.toLowerCase();
  const videoCards = document.querySelectorAll('.video-card');

  videoCards.forEach(card => {
    const title = card.querySelector('.video-title').textContent.toLowerCase();
    card.style.display = title.includes(searchQuery) ? 'block' : 'none';
  });
});

// 处理视频播放
const videoCards = document.querySelectorAll('.video-card');
const videoPlayerSection = document.querySelector('.video-player-section');
const videoPlayer = document.getElementById('video-player');
const videoSource = document.getElementById('video-source');
const closePlayerBtn = document.getElementById('close-player');

videoCards.forEach(card => {
  card.addEventListener('click', () => {
    const videoUrl = card.getAttribute('data-video-url');
    videoSource.src = videoUrl;
    videoPlayer.load(); // 刷新视频源
    videoPlayerSection.style.display = 'flex'; // 显示视频播放区域
  });
});

// 关闭视频播放器
closePlayerBtn.addEventListener('click', () => {
  videoPlayerSection.style.display = 'none'; // 隐藏视频播放区域
  videoPlayer.pause(); // 暂停视频
});

// 登录和注册模态框控制
const signinBtn = document.querySelector('.signin-btn');
const loginModal = document.getElementById('login-modal');
const registerModal = document.getElementById('register-modal');
const loginClose = document.getElementById('login-close');
const registerClose = document.getElementById('register-close');

// 显示登录模态框
signinBtn.addEventListener('click', () => {
  loginModal.style.display = 'flex';
});

// 关闭登录模态框
loginClose.addEventListener('click', () => {
  loginModal.style.display = 'none';
});

// 关闭注册模态框
registerClose.addEventListener('click', () => {
  registerModal.style.display = 'none';
});

// 登录表单提交
document.getElementById('login-form').addEventListener('submit', (e) => {
  e.preventDefault();
  alert('登录成功！');
  loginModal.style.display = 'none';
});

// 注册表单提交
document.getElementById('register-form').addEventListener('submit', (e) => {
  e.preventDefault();
  alert('注册成功！');
  registerModal.style.display = 'none';
});

// 上传视频模态框控制
const uploadBtn = document.querySelector('.upload-btn');
const uploadModal = document.getElementById('upload-modal');
const uploadClose = document.getElementById('upload-close');
const uploadForm = document.getElementById('upload-form');

// 打开上传视频模态框
uploadBtn.addEventListener('click', () => {
  uploadModal.style.display = 'flex';
});

// 关闭上传视频模态框
uploadClose.addEventListener('click', () => {
  uploadModal.style.display = 'none';
});

// 上传表单提交处理
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(uploadForm);

  try {
    const response = await fetch('/upload', {
      method: 'POST',
      body: formData,
    });
    const result = await response.json();

    if (result.success) {
      alert('视频上传成功！');
    } else {
      alert('视频上传失败！');
    }
  } catch (error) {
    alert('上传过程中出错，请稍后再试！');
  }

  uploadModal.style.display = 'none';
});

