# 华大新闻爬取与展示系统

## 项目概述

本项目旨在通过Python爬虫获取华大新闻网站的新闻信息，使用Flask框架构建Web应用展示新闻内容，并通过Nginx实现反向代理和静态资源服务。所有服务均采用Docker容器化部署，确保环境一致性和部署便捷性。

## 功能特点

- 定时爬取华大新闻首页的新闻标题与链接
- 使用MySQL数据库存储新闻数据，确保数据持久化
- 通过Flask应用展示爬取的新闻内容
- Nginx反向代理Flask应用至`/hdxw`路径
- 静态首页展示，可链接至新闻数据页
- 完整的Docker容器化部署方案

## 技术栈

- **编程语言**: Python 3.13+
- **Web框架**: Flask 2.0+
- **爬虫工具**: Requests, BeautifulSoup4
- **数据库**: MySQL 8.0
- **Web服务器**: Nginx
- **容器化**: Docker, Docker Compose
- **版本控制**: Git

## 部署指南

### 前置条件

- 安装Docker (20.10+) 和 Docker Compose (v2+)
- Git环境

### 部署步骤

1. 克隆仓库到本地
> git clone git@github.com:KeMaomao112048/hdxw-project.git

2. 启动服务
> docker-compose up -d

3. 访问服务

- 静态首页: http://<IP或域名>/
- 新闻列表: http://<IP或域名>/hdxw

### 停止服务
# 停止服务但保留数据
> docker-compose down

# 停止服务并清除数据
> docker-compose down -v
## 维护说明

- 数据库数据通过Docker Volume持久化存储
- 爬虫默认每小时执行一次，可在`scraper/scraper.py`中修改定时频率
- 查看服务日志: `docker-compose logs -f`
- 查看数据库内容: `docker exec -it hdxw-project-mysql-1 -uroot -ppassword`