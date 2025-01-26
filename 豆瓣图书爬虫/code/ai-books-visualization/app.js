// 价格分析数据（由后台填写）
const topBooks = [
  {
    title: '人工智能影响经济增长的多渠道效应研究',
    author: '黄志',
    publisher: '四川大学出版社',
    publishYear: '2023',
    rating: '9.8',
    price: '65.00',
    doubanLink: 'https://book.douban.com/subject/36899866/'
  },
  {
    title: '模式识别',
    author: '吴建鑫',
    publisher: '机械工业出版社',
    publishYear: '2020',
    rating: '9.8',
    price: '99.00',
    doubanLink: 'https://book.douban.com/subject/35010688/'
  },
  {
    title: '人工智能 (第4版) : 现代方法',
    author: '[美] Stuart Russell',
    publisher: '人民邮电出版社',
    publishYear: '2022',
    rating: '9.7',
    price: '358.00',
    doubanLink: 'https://book.douban.com/subject/36152133/'
  },
  {
    title: '深度学习入门2 : 自制框架',
    author: '[日]斋藤康毅',
    publisher: '人民邮电出版社',
    publishYear: '2023',
    rating: '9.7',
    price: '129.00',
    doubanLink: 'https://book.douban.com/subject/36303408/'
  },
  {
    title: 'Introduction to Linear Algebra : Fifth Edition',
    author: 'Gilbert Strang',
    publisher: 'Wellesley-Cambridge Press',
    publishYear: '2016',
    rating: '9.7',
    price: '64.99（GBD）',
    doubanLink: 'https://book.douban.com/subject/26824921/'
  },
  {
    title: 'Paradigms of Artificial Intelligence Programming : Case Studies in Common Lisp',
    author: 'Peter Norvig',
    publisher: 'Morgan Kaufmann',
    publishYear: '1991',
    rating: '9.7',
    price: '77.95（USD）',
    doubanLink: 'https://book.douban.com/subject/1754619/'
  },
  {
    title: 'OpenCV深度学习应用与性能优化实践 : Intel与阿里巴巴高级图形图像专家联合撰写！深入解析OpenCV DNN 模块',
    author: '吴至文',
    publisher: '机械工业出版社',
    publishYear: '2020',
    rating: '9.7',
    price: '77.95（USD）',
    doubanLink: 'https://book.douban.com/subject/35107912/'
  },
  {
    title: '从智慧教室到未来教学:"人工智能+"推动干部培训创新发展',
    author: '陈孟贤',
    publisher: '中译出版社',
    publishYear: '2024',
    rating: '9.6',
    price: '89.00',
    doubanLink: 'https://book.douban.com/subject/36954828/'
  },
  {
    title: '游戏人工智能',
    author: 'Steve Rabin',
    publisher: '电子工业出版社',
    publishYear: '2017',
    rating: '9.6',
    price: '129.00',
    doubanLink: 'https://book.douban.com/subject/26838921/'
  },
  {
    title: 'Reinforcement Learning (2/e) : An Introduction',
    author: 'Richard S. Sutton',
    publisher: 'A Bradford Book',
    publishYear: '2018',
    rating: '9.6',
    price: '76.00（USD）',
    doubanLink: 'https://book.douban.com/subject/30323890/'
  },  
];

// 价格分析数据（由后台填写）
const priceAnalysisData = {
  mostExpensiveBook: {
    title: 'Artificial Intelligence (4/e) : A Modern Approach , 4th Edition',
    author: 'Stuart Russell',
    price: '$199.99'
  },
  cheapestBook: {
    title: '老子止笑谭 : 从人工智能的立场重读《道德经》',
    author: '朱邦复',
    price: '4.00'
  },
  averagePrice: '129.78'
};

// 手动输入的出版时间轴数据
const publicationTimelineData = {
  '1980年以前': 8,
  '1980-1990': 12,
  '1990-2000年': 49,
  '2000-2010年': 236,
  '2010-2020年': 601,
  '2020年至今': 521,
  
};

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM 加载完成');

  // 调试：检查 topBooks 数据
  console.log('Top Books 数据:', topBooks);

  // 使用预定义的数据
  renderPriceAnalysis();
  renderTopRatedBooksTable(topBooks);
  renderPublicationTimelineChart();
  displayWordCloud();
});

function renderPriceAnalysis() {
  document.getElementById('mostExpensiveBook').innerHTML = `
    <p>${priceAnalysisData.mostExpensiveBook.title}</p>
    <p>作者：${priceAnalysisData.mostExpensiveBook.author}</p>
    <p>价格：￥${priceAnalysisData.mostExpensiveBook.price}</p>
  `;
  document.getElementById('cheapestBook').innerHTML = `
    <p>${priceAnalysisData.cheapestBook.title}</p>
    <p>作者：${priceAnalysisData.cheapestBook.author}</p>
    <p>价格：￥${priceAnalysisData.cheapestBook.price}</p>
  `;
  document.getElementById('averagePrice').textContent = `￥${priceAnalysisData.averagePrice}`;
}

function renderPublicationTimelineChart() {
  console.log('开始渲染出版时间轴');
  const chart = echarts.init(document.getElementById('publicationTimelineChart'));
  
  const option = {
    title: {
      text: '出版年份时间轴'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const year = params[0].name;
        const count = params[0].value;
        return `${year}年: ${count}本书`;
      }
    },
    xAxis: {
      type: 'category',
      data: Object.keys(publicationTimelineData)
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: Object.values(publicationTimelineData),
      type: 'line'
    }]
  };

  chart.setOption(option);
  console.log('出版时间轴渲染完成');
}

function renderTopRatedBooksTable(books) {
  console.log('开始渲染 Top 10 表格');
  const tableBody = document.getElementById('topRatedBooksBody');
  if (!tableBody) {
    console.error('未找到 topRatedBooksBody 元素');
    return;
  }
  tableBody.innerHTML = books.map(book => `
    <tr class="cursor-pointer hover:bg-gray-100" onclick="window.open('${book.doubanLink}', '_blank')">
      <td class="px-4 py-2">${book.title}</td>
      <td class="px-4 py-2">${book.author}</td>
      <td class="px-4 py-2">${book.publisher}</td>
      <td class="px-4 py-2">${book.publishYear}</td>
      <td class="px-4 py-2">${book.rating}</td>
      <td class="px-4 py-2">${book.price}</td>
    </tr>
  `).join('');
  console.log('Top 10 表格渲染完成');
}

function displayWordCloud() {
  const wordCloudContainer = document.getElementById('wordFrequencyChart');
  wordCloudContainer.innerHTML = `
    <img src="wordcloud.jpg" alt="AI书籍关键词词云" class="w-full h-full object-contain">
  `;
}