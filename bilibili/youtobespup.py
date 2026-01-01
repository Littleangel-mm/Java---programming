# 自动上传 B 站视频脚本
import os
import time
import json
import re
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# === 基本配置 ===
VIDEO_FOLDER = "output"  # 视频目录
COOKIE_FILE = "bilibili_cookies.json"  # 登录cookie文件
LOG_FILE = "upload_log.txt"  # 上传日志
VIDEO_DESC = "视频来自网络，仅供学习交流使用，若有侵权请联系删除。"
UPLOAD_URL = "https://member.bilibili.com/platform/upload/video/frame"
DEFAULT_SOURCE = "https://www.youtube.com/"  # 默认视频来源
DEFAULT_COVER_PATH = "Cover image\\default_cover.png"  # 默认封面图片路径
MAX_UPLOAD_WAIT = 600  # 最大上传等待时间（秒）
SUBMIT_WAIT = 90  # 投稿等待时间（秒）
WAIT_TIMEOUT = 10  # 元素等待超时（秒）

# === ChromeDriver 路径 ===
CHROMEDRIVER_PATH = r"chromedriver-win64\chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--ignore-certificate-errors")  # 忽略 SSL 证书错误
options.add_argument("--disable-gpu")  # 禁用 GPU 加速
options.add_argument("--no-sandbox")  # 禁用沙盒模式
options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题
driver = webdriver.Chrome(service=service, options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """
})

def save_cookies():
    """保存登录 Cookies"""
    cookies = driver.get_cookies()
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print("登录成功，Cookies 已保存")

def load_cookies():
    """加载已保存的 Cookies"""
    if not os.path.exists(COOKIE_FILE):
        return False
    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    driver.get("https://www.bilibili.com/")
    for cookie in cookies:
        cookie.pop("expiry", None)
        driver.add_cookie(cookie)
    driver.refresh()
    print("已加载登录 Cookies")
    return True

def login_bilibili():
    """自动登录"""
    print("正在登录 B 站...")
    driver.get("https://www.bilibili.com/")
    time.sleep(3)
    if load_cookies():
        print("自动登录成功")
        return
    print("请扫码登录 B 站账户...")
    driver.get("https://passport.bilibili.com/login")
    input("登录成功后按 Enter 继续：")
    save_cookies()
    print("登录信息已保存，下次将自动登录")

def find_upload_input():
    """递归查找视频上传框（适配 Shadow DOM）"""
    for attempt in range(5):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            for elem in elements:
                try:
                    if elem.is_displayed() or elem.is_enabled():
                        return elem
                except:
                    pass
            if elements:
                try:
                    driver.execute_script("arguments[0].style.display='block';", elements[0])
                    driver.execute_script("arguments[0].style.visibility='visible';", elements[0])
                    driver.execute_script("arguments[0].style.opacity='1';", elements[0])
                    return elements[0]
                except:
                    pass
        except:
            pass
        time.sleep(1)

    js_code = """
    function deepQuery(selector) {
        const all = [];
        function find(node) {
            if (!node) return;
            if (node.querySelectorAll) {
                node.querySelectorAll(selector).forEach(el => {
                    all.push({
                        element: el,
                        tagName: el.tagName,
                        id: el.id,
                        className: el.className,
                        name: el.name,
                        accept: el.accept
                    });
                });
            }
            if (node.shadowRoot) find(node.shadowRoot);
            node.childNodes.forEach(find);
        }
        find(document);
        return all;
    }
    var results = deepQuery('input[type="file"][accept*="video"], input[type="file"]');
    if (results.length > 0) {
        var first = results[0].element;
        first.style.display = 'block';
        first.style.visibility = 'visible';
        first.style.opacity = '1';
        return first;
    }
    return null;
    """

    for attempt in range(10):
        try:
            element = driver.execute_script(js_code)
            if element:
                return element
        except Exception:
            pass
        time.sleep(2)

    return None

def find_cover_input():
    """查找封面上传输入框"""
    selectors = [
        ("input[type='file'][accept*='image']", By.CSS_SELECTOR),
        ("input[accept*='jpg'], input[accept*='png'], input[accept*='jpeg']", By.CSS_SELECTOR),
        ("//input[contains(@accept, 'image')]", By.XPATH),
        ("//input[@type='file' and (contains(@accept, 'jpg') or contains(@accept, 'png') or contains(@accept, 'jpeg'))]", By.XPATH)
    ]
    for selector, by in selectors:
        try:
            cover_input = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((by, selector))
            )
            driver.execute_script("arguments[0].style.display='block';", cover_input)
            driver.execute_script("arguments[0].style.visibility='visible';", cover_input)
            driver.execute_script("arguments[0].style.opacity='1';", cover_input)
            return cover_input
        except:
            continue
    print("未找到封面上传输入框，跳过封面上传")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write("[警告] 未找到封面上传输入框\n")
    return None

def wait_for_text(text, timeout=60):
    """等待特定文字出现"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{text}')]"))
        )
        return True
    except:
        return False

def upload_video(video_path):
    """上传单个视频"""
    title = os.path.splitext(os.path.basename(video_path))[0]
    print(f"\n正在上传：《{title}》")

    abs_path = os.path.abspath(video_path)
    if not os.path.exists(abs_path):
        print(f"视频文件不存在：{abs_path}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[失败] {video_path} - 视频文件不存在\n")
        return False

    # 动态调整等待时间
    file_size_mb = os.path.getsize(abs_path) / (1024 * 1024)
    max_wait_time = max(MAX_UPLOAD_WAIT, int(file_size_mb * 2))
    print(f"文件大小：{file_size_mb:.2f}MB，上传超时时间：{max_wait_time}秒")

    driver.get(UPLOAD_URL)
    time.sleep(5)

    upload_input = find_upload_input()
    if not upload_input:
        print("未找到上传控件")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[失败] {video_path} - 未找到上传控件\n")
        return False

    try:
        driver.execute_script("arguments[0].style.display='block';", upload_input)
        driver.execute_script("arguments[0].style.visibility='visible';", upload_input)
        driver.execute_script("arguments[0].style.opacity='1';", upload_input)
        driver.execute_script("arguments[0].style.position='static';", upload_input)
        driver.execute_script("arguments[0].style.height='auto';", upload_input)
        driver.execute_script("arguments[0].style.width='auto';", upload_input)
    except Exception as e:
        print(f"设置元素样式时出错：{e}")

    try:
        upload_input.send_keys(abs_path)
        print("视频上传已触发...")
    except Exception as e:
        print(f"直接 send_keys 失败，尝试 JavaScript 方式：{e}")
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", upload_input)
            time.sleep(1)
            upload_input.send_keys(abs_path)
            print("视频上传已触发（第二次尝试）...")
        except Exception as e2:
            print(f"无法上传文件，错误：{e2}")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[失败] {video_path} - 无法上传文件：{e2}\n")
            return False

    # 短暂等待以确保上传开始
    print("等待上传初始化...")
    time.sleep(3)

    # 上传封面
    print("处理封面...")
    abs_cover_path = os.path.abspath(DEFAULT_COVER_PATH)
    if os.path.exists(abs_cover_path):
        cover_input = find_cover_input()
        if cover_input:
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", cover_input)
                cover_input.send_keys(abs_cover_path)
                print(f"封面已上传：{abs_cover_path}")
                time.sleep(2)
                if wait_for_text("封面上传成功", timeout=10) or wait_for_text("封面已设置", timeout=10):
                    print("封面上传确认成功")
                else:
                    print("未检测到封面上传成功提示，可能已成功")
            except Exception as e:
                print(f"上传封面时出错：{e}")
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"[警告] {video_path} - 上传封面失败：{e}\n")
        else:
            print("未找到封面上传控件，跳过封面上传")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[警告] {video_path} - 未找到封面上传控件\n")
    else:
        print(f"封面文件不存在：{abs_cover_path}，跳过封面上传")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[警告] {video_path} - 封面文件不存在：{abs_cover_path}\n")

    print("填写视频信息...")
    try:
        title_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'标题') or contains(@placeholder,'title')]"))
        )
        title_input.clear()
        time.sleep(0.5)
        title_input.send_keys(title)
        print(f"标题已填写：{title}")
    except Exception as e:
        print(f"未找到标题输入框：{e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[警告] {video_path} - 未找到标题输入框：{e}\n")

    try:
        desc_box = None
        selectors = [
            "//div[contains(@class,'ql-editor')]",
            "//div[contains(@class,'desc')]//div[contenteditable='true']",
            "//textarea[contains(@placeholder,'简介')]",
            "//div[@contenteditable='true']"
        ]
        for selector in selectors:
            try:
                desc_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue

        if desc_box:
            desc_box.click()
            time.sleep(0.5)
            desc_box.clear()
            time.sleep(0.5)
            desc_box.send_keys(VIDEO_DESC)
            print("简介已填写")
        else:
            print("未找到简介输入框")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[警告] {video_path} - 未找到简介输入框\n")
    except Exception as e:
        print(f"填写简介时出错：{e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[错误] {video_path} - 填写简介失败：{e}\n")

    print("添加标签...")
    tags = ["游戏", "搞笑", "甜美", "视觉震撼"]
    added_tags = 0
    for tag in tags:
        try:
            tag_input = None
            tag_selectors = [
                '//input[@placeholder="按回车键Enter创建标签"]',
                '//input[contains(@placeholder,"Enter")]',
                '//input[contains(@placeholder,"标签")]'
            ]
            for selector in tag_selectors:
                try:
                    tag_input = driver.find_element(By.XPATH, selector)
                    if tag_input:
                        break
                except:
                    continue

            if tag_input:
                tag_input.click()
                time.sleep(0.3)
                tag_input.send_keys(tag)
                time.sleep(0.3)
                tag_input.send_keys(Keys.ENTER)
                time.sleep(0.5)
                added_tags += 1
                print(f"  ✓ 已添加标签：{tag}")
            else:
                break
        except Exception as e:
            print(f"  添加标签 {tag} 失败：{e}")
            break

    if added_tags > 0:
        print(f"已添加 {added_tags} 个标签")

    print("选择视频类型：转载")
    video_type_selected = False
    try:
        type_selectors = [
            "//span[contains(text(),'转载')]",
            "//label[contains(text(),'转载')]",
            "//div[contains(text(),'转载')]",
            "//input[@value='转载' or @value='转载投稿']",
            "//radio[contains(text(),'转载')]",
            "//button[contains(text(),'转载')]"
        ]

        for selector in type_selectors:
            try:
                type_element = driver.find_element(By.XPATH, selector)
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", type_element)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", type_element)
                print("已选择视频类型：转载")
                video_type_selected = True
                time.sleep(1)
                break
            except:
                continue

        if not video_type_selected:
            print("未找到视频类型选择器，可能页面结构已变化")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[警告] {video_path} - 未找到视频类型选择器\n")
    except Exception as e:
        print(f"选择视频类型时出错：{e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[错误] {video_path} - 选择视频类型失败：{e}\n")

    print("填写转载来源...")
    try:
        source_input = None
        source_selectors = [
            "//input[contains(@placeholder,'转载来源') or contains(@placeholder,'来源') or contains(@placeholder,'source')]",
            "//input[@name='source' or @id='source']",
            "//textarea[contains(@placeholder,'转载来源') or contains(@placeholder,'来源')]"
        ]
        for selector in source_selectors:
            try:
                source_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                continue

        if source_input:
            source_input.click()
            time.sleep(0.3)
            source_input.clear()
            time.sleep(0.3)
            source_input.send_keys(DEFAULT_SOURCE)
            print(f"转载来源已填写：{DEFAULT_SOURCE}")
        else:
            print("未找到转载来源输入框")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[警告] {video_path} - 未找到转载来源输入框\n")
    except Exception as e:
        print(f"填写转载来源时出错：{e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[错误] {video_path} - 填写转载来源失败：{e}\n")

    print("正在提交投稿...")
    submit_selectors = [
        ("span.submit-add", By.CSS_SELECTOR),
        ("//span[contains(text(),'立即投稿')]", By.XPATH),
        ("//span[contains(text(),'投稿')]", By.XPATH),
        ("//span[contains(text(),'立即投稿')]/ancestor::button", By.XPATH),
        ("button[class*='submit'], button[class*='publish']", By.CSS_SELECTOR),
        ("button.btn-submit, button.submit-btn", By.CSS_SELECTOR)
    ]

    submit_btn = None
    for selector, by in submit_selectors:
        try:
            submit_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((by, selector))
            )
            print(f"找到投稿元素，使用选择器：{selector}")
            break
        except TimeoutException:
            print(f"选择器失败：{selector}")
            continue

    if not submit_btn:
        print("找不到投稿元素")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[失败] {video_path} - 找不到投稿元素\n")
        return False

    try:
        current_url = driver.current_url
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", submit_btn)
        time.sleep(0.5)
        try:
            submit_btn.click()
            print("Selenium 点击投稿元素")
        except:
            print("Selenium 点击失败，尝试 JavaScript 点击")
            driver.execute_script("arguments[0].click();", submit_btn)
            print("JavaScript 点击投稿元素")

        try:
            parent_button = driver.execute_script(
                "return arguments[0].closest('button');", submit_btn
            )
            if parent_button:
                driver.execute_script("arguments[0].click();", parent_button)
                print("已点击父级 button 元素")
        except:
            print("未找到父级 button 元素")

        # 等待视频上传完成
        print("等待视频上传和处理完成...")
        start_time = time.time()
        upload_completed = False
        last_status = ""

        while time.time() - start_time < max_wait_time:
            elapsed = int(time.time() - start_time)
            page_source = driver.page_source

            if any(keyword in page_source for keyword in ["上传完成", "上传成功", "视频上传完成", "处理完成", "100%"]):
                print("视频上传和处理完成")
                upload_completed = True
                break
            elif any(keyword in page_source for keyword in ["上传失败", "上传出错", "上传异常", "文件过大", "格式不支持"]):
                print("视频上传失败")
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"[失败] {video_path} - 视频上传失败\n")
                return False
            elif any(keyword in page_source for keyword in ["上传中", "处理中", "上传进度", "正在上传", "转码中"]):
                status = f"上传中... ({elapsed}秒)"
                if status != last_status:
                    print(status)
                    last_status = status
            elif "%" in page_source and ("上传" in page_source or "进度" in page_source):
                progress_match = re.search(r'(\d+)%', page_source)
                if progress_match:
                    progress = progress_match.group(1)
                    status = f"上传进度: {progress}% ({elapsed}秒)"
                    if status != last_status:
                        print(status)
                        last_status = status

            time.sleep(3)

        if not upload_completed:
            print("视频上传超时，可能投稿被取消")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[失败] {video_path} - 视频上传超时\n")
            return False

        # 检查投稿结果
        print("检查投稿结果...")
        start_time = time.time()
        confirm_clicked = False
        success_keywords = [
            "投稿成功", "提交成功", "发布成功", "审核中", "已提交",
            "等待审核", "投稿已提交", "视频已上传", "已提交至审核",
            "视频已发布", "投稿完成", "已进入审核", "视频管理", "草稿"
        ]
        failure_keywords = [
            "投稿失败", "提交失败", "发布失败", "错误", "失败",
            "审核不通过", "权限不足", "格式不合法", "请先",
            "无法提交", "无效链接"
        ]

        while time.time() - start_time < SUBMIT_WAIT:
            elapsed = int(time.time() - start_time)
            page_source = driver.page_source
            current_url_after = driver.current_url

            for keyword in success_keywords:
                if keyword in page_source:
                    print(f"投稿成功：《{title}》（检测到：{keyword}）")
                    with open(LOG_FILE, "a", encoding="utf-8") as log:
                        log.write(f"[成功] {video_path} - 检测到：{keyword}\n")
                    return True

            for keyword in failure_keywords:
                if keyword in page_source:
                    print(f"投稿失败（检测到：{keyword}）")
                    with open(LOG_FILE, "a", encoding="utf-8") as log:
                        log.write(f"[失败] {video_path} - {keyword}\n")
                    return False

            if current_url != current_url_after and any(x in current_url_after.lower() for x in ["success", "manage", "list", "review", "archive", "video", "upload"]):
                print(f"投稿成功：《{title}》（URL变化：{current_url_after}）")
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"[成功] {video_path} - URL变化\n")
                return True

            if not confirm_clicked:
                confirm_selectors = [
                    ("//button[contains(text(),'确认') or contains(text(),'确定') or contains(text(),'是')]", By.XPATH),
                    ("button[class*='confirm'], button[class*='ok'], button[class*='submit']", By.CSS_SELECTOR),
                    ("//div[contains(@class,'dialog') or contains(@class,'modal')]//button[contains(text(),'确认') or contains(text(),'确定')]", By.XPATH),
                    ("//span[contains(text(),'确认') or contains(text(),'确定')]/ancestor::button", By.XPATH)
                ]
                for selector, by in confirm_selectors:
                    try:
                        confirm_btn = WebDriverWait(driver, 2).until(
                            EC.element_to_be_clickable((by, selector))
                        )
                        driver.execute_script("arguments[0].click();", confirm_btn)
                        print("已点击确认按钮")
                        confirm_clicked = True
                        time.sleep(1)
                        break
                    except TimeoutException:
                        continue

            try:
                submit_btn_check = driver.find_element(By.CSS_SELECTOR, "span.submit-add")
                if not submit_btn_check.is_displayed() or not submit_btn_check.is_enabled():
                    print(f"投稿元素已禁用或不可见，视为成功")
                    with open(LOG_FILE, "a", encoding="utf-8") as log:
                        log.write(f"[成功] {video_path} - 投稿元素已禁用或不可见\n")
                    return True
            except NoSuchElementException:
                print(f"投稿元素已消失，视为成功")
                with open(LOG_FILE, "a", encoding="utf-8") as log:
                    log.write(f"[成功] {video_path} - 投稿元素已消失\n")
                return True

            time.sleep(1)

        print("投稿超时，状态不明确")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[失败] {video_path} - 投稿超时\n")
        return False

    except Exception as e:
        print(f"投稿出错，错误：{e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[错误] {video_path} -> {e}\n")
        return False

def batch_upload():
    """批量上传 output 文件夹下所有视频"""
    videos = [str(p) for p in pathlib.Path(VIDEO_FOLDER).glob("*.mp4")]
    if not videos:
        print("没有找到视频文件")
        return

    print(f"共检测到 {len(videos)} 个视频")
    success = 0

    for video in videos:
        try:
            if upload_video(video):
                success += 1
            time.sleep(5)
        except Exception as e:
            print(f"视频处理异常：{e}")
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"[错误] {video} -> {e}\n")

    print(f"\n上传完成：成功 {success}/{len(videos)} 个")
    print(f"日志文件：{LOG_FILE}")

if __name__ == "__main__":
    try:
        login_bilibili()
        batch_upload()
    except Exception as e:
        print(f"程序运行异常：{e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"[错误] 程序运行异常：{e}\n")
    finally:
        input("\n按 Enter 退出...")
        driver.quit()