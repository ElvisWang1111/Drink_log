# Drink Log（两步提交版，无后端）

[![English](https://img.shields.io/badge/Language-English-orange)](./README.md)
[![简体中文](https://img.shields.io/badge/语言-简体中文-blue)](./README.zh-CN.md)

这是一个纯前端页面，不需要后端。

## 使用方式

1. 打开你的 GitHub Pages 网页。
2. 填写邮箱，点击 `Open Step 2`。
3. 在 GitHub 页面点击一次 `Submit new issue`。
4. GitHub Action 会自动把数据写入 `data/drink-log.csv`。

## 为什么是两步

因为没有后端授权，网页不能直接代替你提交 issue。  
所以需要你在 GitHub 页面手动点一次提交。

## 安全限制

workflow 只处理仓库 owner 自己创建的 `drink-log` issue。  
其他人提交不会写入你的 CSV。

## 仓库需要的文件

- `.github/workflows/process-drink-log.yml`
- `scripts/process_issue.py`
- `data/drink-log.csv`

如果你使用这个模板创建仓库，默认都已包含。
