# SUSTech-CourseTable
[![GitHub license](https://img.shields.io/github/license/HeZean/SUSTech-CourseTable)](https://github.com/HeZean/SUSTech-CourseTable) [![Python version](https://img.shields.io/badge/python-v3.x-blue)](https://github.com/HeZean/SUSTech-CourseTable)

## 快速开始

1. 检查 `user.json` 

   - `sid` 和 `pwd` 指 **学号** 和 **CAS的密码**

   - `year` 填入学年，如 `2021-2022` 
   - `semester` 填入学期，*秋季学期填 1、春季学期填 2，夏季 (暂未实验) 填 3*

2. **假设你已经装有 python3** 和 **pip**：在此目录打开 terminal，安装依赖，并运行主程序，选择导出中文 / 英文课表

   ```shell
   cd /path/to/the/repo
   pip install -r requirements.txt
   python3 main.py
   ```

3. 将生成的 `schedule.ics` [导入手机](https://miaotony.xyz/NUAA_ClassSchedule/HowToImport.html)



## 但是…

此版本较为简陋，且使用需要一定的代码基础，也不具备课程别名，合并大课等功能

⚠️ 如果你喜欢安全，有改代码能力，大可以拿走现有的代码自己修改，希望能帮到你 : )

✅ 使用 [在线版本](http://) 能获得更好的使用体验，只要你愿意相信本服务是安全的  **但是暂时可能会鸽**

> 登陆接入了学校的 CAS 系统，我的服务仅使用会话的 cookie 达到临时访问课表的功能
>
> 我无法且没必要获取你的用户名和密码 — take it easy

✨ 有任何问题或建议欢迎开 issue 和 PR
