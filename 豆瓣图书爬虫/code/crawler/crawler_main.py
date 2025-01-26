import random
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import requests
import csv
import atexit
from webdriver_manager.chrome import ChromeDriverManager

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 代理配置
PROXY_HOST = "117.68.38.184"
PROXY_PORT = "26147"
PROXY_USERNAME = "B636809458235"
PROXY_PASSWORD = "zKHvxnaqNw6Rl3Eh"

# User-Agent列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

all_books = []

def setup_driver():
    logger.info("开始设置 Chrome 驱动...")
    chrome_options = Options()
    chrome_options.add_argument(f'--user-agent={random.choice(USER_AGENTS)}')
    chrome_options.add_argument(f'--proxy-server={PROXY_HOST}:{PROXY_PORT}')
    # chrome_options.add_argument("--headless")  # 注释掉这行以显示浏览器窗口
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        logger.info("正在安装或更新 ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        
        logger.info("正在启动 Chrome 浏览器...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logger.info("Chrome 浏览器已成功启动")
        return driver
    except Exception as e:
        logger.error(f"启动 Chrome 浏览器时出错: {e}")
        return None

def check_ip(driver):
    try:
        driver.get("http://api.91http.com/v1/get-ip")
        ip = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre"))).text
        logger.info(f"当前使用的IP地址: {ip}")
        return ip
    except Exception as e:
        logger.error(f"检查IP时出错: {e}")
        return None

def login_with_qr(driver):
    try:
        driver.get("https://accounts.douban.com/passport/login")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "account-body")))
        
        logger.info("请手动完成登录过程。登录成功后，程序将自动继续。")
        
        # 等待用户手动登录
        start_time = time.time()
        while True:
            try:
                # 检查是否已登录成功
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "nav-user-account")))
                logger.info("检测到登录成功")
                return True
            except TimeoutException:
                # 如果还没有登录成功，继续等待
                if time.time() - start_time > 300:  # 等待5分钟
                    logger.warning("登录等待超时，请重新运行程序并尝试登录")
                    return False
                time.sleep(5)
    
    except Exception as e:
        logger.error(f"登录过程中出现错误: {e}")
        return False

def crawl_keyword(driver, keyword):
    books = []
    page = 1
    max_retries = 5
    
    while True:
        url = f"https://search.douban.com/book/subject_search?search_text={keyword}&cat=1001&start={(page-1)*15}"
        
        for attempt in range(max_retries):
            try:
                driver.get(url)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "item-root")))
                break
            except (TimeoutException, WebDriverException) as e:
                logger.warning(f"第{attempt+1}次尝试失败：{e}")
                if attempt == max_retries - 1:
                    logger.error("达到最大重试次数，跳过此页")
                    return books
                time.sleep(random.uniform(5, 10))
        
        items = driver.find_elements(By.CLASS_NAME, "item-root")
        if not items:
            logger.info(f"没有找到更多书籍，结束爬取")
            break
        
        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "a.title-text").text.strip()
                info = item.find_element(By.CLASS_NAME, "meta").text.strip().split('/')
                author = info[0].strip()
                publisher = info[-3].strip() if len(info) >= 3 else "未知"
                publish_date = info[-2].strip() if len(info) >= 2 else "未知"
                price = info[-1].strip() if len(info) >= 1 else "未知"
                rating = item.find_element(By.CLASS_NAME, "rating_nums").text.strip() if item.find_elements(By.CLASS_NAME, "rating_nums") else "暂无评分"
                
                book = {
                    '标题': title,
                    '作者': author,
                    '出版社': publisher,
                    '出版时间': publish_date,
                    '评分': rating,
                    '纸质版定价': price
                }
                books.append(book)
                logger.info(f"已爬取: {book}")
            except NoSuchElementException:
                logger.warning("解析书籍信息时出错，跳过")
        
        next_page = driver.find_elements(By.XPATH, "//a[contains(@class, 'next') and contains(text(), '后页')]")
        if not next_page:
            logger.info("没有下一页了，结束爬取")
            break
        
        page += 1
        time.sleep(random.uniform(3, 7))
    
    return books

def save_to_csv():
    global all_books
    unique_books = []
    unique_titles = set()
    for book in all_books:
        if book['标题'] not in unique_titles:
            unique_titles.add(book['标题'])
            unique_books.append(book)
    
    with open('douban_books.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['标题', '作者', '出版社', '出版时间', '评分', '纸质版定价'])
        writer.writeheader()
        writer.writerows(unique_books)
    
    logger.info(f"\n爬取完成，共爬取{len(unique_books)}本不重复的书，数据已保存到douban_books.csv文件中")

def main():
    global all_books
    driver = setup_driver()
    if driver is None:
        logger.error("无法启动 Chrome 浏览器，程序退出。")
        return

    try:
        ip = check_ip(driver)
        if not ip:
            logger.error("无法获取IP地址，请检查代理设置")
            return

        if not login_with_qr(driver):
            logger.error("登录失败，程序退出")
            return

        keywords = input("请输入要搜索的关键词，每个关键词占一行。输入完成后请按两次回车：").split('\n')
        keywords = [k.strip() for k in keywords if k.strip()]
        
        logger.info(f"您输入的关键词是：{', '.join(keywords)}")
        logger.info("开始爬取数据...")
        
        for keyword in keywords:
            logger.info(f"\n正在爬取关键词 '{keyword}'")
            keyword_books = crawl_keyword(driver, keyword)
            all_books.extend(keyword_books)
            time.sleep(random.uniform(10, 20))
        
    except KeyboardInterrupt:
        logger.info("\n程序被用户中断")
    except Exception as e:
        logger.error(f"发生错误: {e}")
    finally:
        if driver:
            driver.quit()
        save_to_csv()

if __name__ == '__main__':
    atexit.register(save_to_csv)  # 注册退出时保存函数
    main()