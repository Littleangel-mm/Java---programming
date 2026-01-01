


#检测脚本



import time



import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = r"chromedriver-win64\\chromedriver.exe"  # 改成你的路径
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

OUT_FILE = "iframe_info.txt"

def try_click_candidates():
    # 尝试点击可能会触发上传区域的按钮/链接（中文匹配）
    texts = ["上传视频", "投稿", "发布视频", "选择文件", "选择视频", "开始上传", "上传"]
    clicked = []
    for t in texts:
        try:
            els = driver.find_elements(By.XPATH, f"//*[contains(text(), '{t}')]")
            for el in els:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", el)
                    el.click()
                    clicked.append(t)
                    time.sleep(1)
                except Exception:
                    pass
        except Exception:
            pass
    return clicked

def get_elements_info():
    results = []
    # 1) 所有 iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    results.append(f"检测到 {len(iframes)} 个 iframe：\n")
    for i, f in enumerate(iframes, 1):
        name = f.get_attribute("name")
        cls = f.get_attribute("class")
        src = f.get_attribute("src")
        outer = f.get_attribute("outerHTML")
        visible = f.is_displayed()
        results.append(f"iframe #{i}:\n name: {name}\n class: {cls}\n src: {src}\n visible: {visible}\n outerHTML: {outer}\n\n")

    # 2) 所有 input[type=file]
    files = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
    results.append(f"检测到 {len(files)} 个 input[type=file]：\n")
    for i, el in enumerate(files, 1):
        cls = el.get_attribute("class")
        id_ = el.get_attribute("id")
        name = el.get_attribute("name")
        outer = el.get_attribute("outerHTML")
        visible = el.is_displayed()
        results.append(f"file input #{i}:\n id: {id_}\n name: {name}\n class: {cls}\n visible: {visible}\n outerHTML: {outer}\n\n")

    # 3) 其它可能的相关元素（class/id/name 包含关键字）
    keywords = ["upload", "video", "file", "choose", "select", "post", "投稿", "上传"]
    matched = []
    all_elems = driver.find_elements(By.XPATH, "//*")
    for el in all_elems:
        try:
            cls = el.get_attribute("class") or ""
            id_ = el.get_attribute("id") or ""
            name = el.get_attribute("name") or ""
            combined = " ".join([cls, id_, name]).lower()
            if any(k in combined for k in keywords):
                outer = el.get_attribute("outerHTML")
                visible = el.is_displayed()
                matched.append((cls, id_, name, visible, outer))
        except Exception:
            continue
    results.append(f"检测到 {len(matched)} 个 class/id/name 包含关键字的元素：\n")
    for i, (cls, id_, name, visible, outer) in enumerate(matched, 1):
        results.append(f"elem #{i}:\n id: {id_}\n name: {name}\n class: {cls}\n visible: {visible}\n outerHTML: {outer}\n\n")

    return "\n".join(results)


def main():
    try:
        print("打开登录页，请登录 B 站（扫码或账号登录）...")
        driver.get("https://passport.bilibili.com/login")
        driver.maximize_window()
        input("登录成功后按 Enter 继续：")

        print("尝试打开投稿页...")
        driver.get("https://member.bilibili.com/platform/upload/video/frame")
        time.sleep(5)

        print("尝试点击可能触发上传区域的按钮（上传/投稿 等）...")
        clicked = try_click_candidates()
        if clicked:
            print("已尝试点击的文本：", clicked)
        else:
            print("未自动点击到触发元素，继续检测页面元素...")

        time.sleep(3)
        info = get_elements_info()

        with open(OUT_FILE, "w", encoding="utf-8") as f:
            f.write(info)

        print(f"检测完成，已将结果保存到 {OUT_FILE}")
        print("请把文件内容贴给我，或直接把文件里的包含 'upload' / 'video' / 'file' 的部分复制过来。")

    finally:
        input("按 Enter 关闭浏览器并退出脚本...")
        driver.quit()

if __name__ == "__main__":
    main()





import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = r"chromedriver-win64\\chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

OUT_FILE = "iframe_info.txt"

def try_click_candidates():
    texts = ["上传视频", "投稿", "发布视频", "选择文件", "选择视频", "上传"]
    for t in texts:
        els = driver.find_elements(By.XPATH, f"//*[contains(text(), '{t}')]")
        for el in els:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", el)
                el.click()
                time.sleep(1)
                print(f"尝试点击元素: {t}")
            except Exception:
                pass


def short(s):
    """裁剪长字符串"""
    if not s:
        return ""
    return s if len(s) < 60 else s[:60] + "..."


def detect_elements():
    report = []

    # iframe 检测
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    report.append(f"检测到 {len(iframes)} 个 iframe：")
    for i, f in enumerate(iframes, 1):
        name = f.get_attribute("name")
        cls = f.get_attribute("class")
        src = f.get_attribute("src")
        visible = f.is_displayed()
        report.append(f"[iframe {i}] name={name}, class={cls}, visible={visible}, src={short(src)}")

    # input[type=file]
    files = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
    report.append(f"\n检测到 {len(files)} 个文件选择框：")
    for i, el in enumerate(files, 1):
        cls = el.get_attribute("class")
        id_ = el.get_attribute("id")
        name = el.get_attribute("name")
        visible = el.is_displayed()
        report.append(f"[file {i}] id={id_}, name={name}, class={cls}, visible={visible}")

    # class/id/name 中包含 upload 或 video
    keywords = ["upload", "video", "file", "投稿", "上传"]
    all_elems = driver.find_elements(By.XPATH, "//*")
    matched = []
    for el in all_elems:
        try:
            cls = el.get_attribute("class") or ""
            id_ = el.get_attribute("id") or ""
            name = el.get_attribute("name") or ""
            text = el.text or ""
            combo = " ".join([cls, id_, name, text]).lower()
            if any(k in combo for k in keywords):
                matched.append((cls, id_, name, text[:20], el.is_displayed()))
        except Exception:
            continue

    report.append(f"\n检测到 {len(matched)} 个可疑元素（包含关键词 upload/video/file）：")
    for i, (cls, id_, name, text, visible) in enumerate(matched, 1):
        report.append(f"[match {i}] id={id_}, name={name}, class={short(cls)}, text={short(text)}, visible={visible}")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"\n检测结果已保存到 {OUT_FILE}")


def main():
    print("🟦 打开登录页，请登录 B 站（扫码或账号登录）...")
    driver.get("https://passport.bilibili.com/login")
    input("登录完成后按 Enter 继续：")

    driver.get("https://member.bilibili.com/platform/upload/video/frame")
    print("🟦 正在加载投稿页面...")
    time.sleep(6)

    try_click_candidates()
    time.sleep(3)
    detect_elements()

    input("\n按 Enter 关闭浏览器...")
    driver.quit()


if __name__ == "__main__":
    main()





