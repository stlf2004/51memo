# 51备忘录
---

## 使用方法：
- ### 交互式操作
```
> python 51memo.py
```
- ### 命令行操作
> 1. #### 查看帮助
```
> python 51memo.py -h
Usage:
-h or --help or help 查看帮助
query -u [用户名] -y [年] -m [月] 查询备忘录信息
mail -u [用户名] -y [年] -m [月] 发送备忘录信息到用户的邮箱中
```
> 2. #### 查询用户备忘录信息
```
> python 51memo.py query -u lf -y 2018 -m 5
{'status': 0, 'message': 'success', 'data': [{'id': 2, 'date': '2018年05月21日16:40', 'thing': '明天上班'}, {'id': 3, 'date': '2018年05月
30日00:00', 'thing': '出门'}]}
```
> 3. #### 发送用户备忘录信息到他的邮箱中
```
> python 51memo.py mail -u lf -y 2018 -m 5
{'status': 0, 'message': 'success', 'data': {}}
```
