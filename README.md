# 豆瓣AI书籍爬虫与数据可视化

这个项目包含了一个豆瓣AI相关书籍的爬虫程序和一个数据可视化网页应用。

## 项目结构

- `code/crawler/`: 包含爬虫相关代码
  - `crawler_main.py`: 主爬虫程序
- `code/ai-books-visualization/`: 包含数据可视化相关代码
  - `app.js`: 前端JavaScript代码
  - `index.html`: 主HTML页面
  - `styles.css`: CSS样式文件
  - `douban_books.csv`: 爬取的书籍数据

## 功能

1. 爬虫程序:
   - 使用Selenium自动化爬取豆瓣上的AI相关书籍信息
   - 支持代理IP和随机User-Agent
   - 自动处理验证码和登录
   - 将爬取的数据保存为CSV格式

2. 数据可视化:
   - 展示Top 10评分最高的AI书籍
   - 显示价格分析数据
   - 生成出版时间轴图表
   - 展示AI书籍关键词词云图

## 如何使用

1. 运行爬虫程序:
   ```
   python code/crawler/crawler_main.py
   ```

2. 启动数据可视化网页:
   - 在`code/ai-books-visualization/`目录下启动一个本地服务器
   - 在浏览器中打开`index.html`

## 依赖

- Python 3.7+
- Selenium
- Chrome WebDriver
- D3.js
- ECharts

## 注意事项

-仅用于学术用途，严禁商业 
-请遵守豆瓣的robots.txt规则和使用条款
- 爬取速度请控制在合理范围内,避免对目标网站造成压力

## 贡献

欢迎提交问题和合并请求。对于重大更改,请先开issue讨论您想要更改的内容。
## 感谢

oeasy最后一次作业啦，虽然课上老是摸鱼，偶尔还逃了几节课，还是感谢你带我打开了一个新世界的大门。

## 许可证

[MIT](https://choosealicense.com/licenses/mit/)# -
