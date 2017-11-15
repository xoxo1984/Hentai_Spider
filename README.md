Hentai_Spider
===
## 项目说明
爬绅士站的爬虫，主要是自己用  
项目参考了https://github.com/fffonion/xeHentai，在此表示感谢  
main.exe由pyinstaller生成，供windows用户使用  
另，下文中提到的画廊的概念，指绅士站中.../**g**/xxx/xxxx/所代表的那一连串图片  
## 如何使用
### 下载
下载`main.exe`，`config.ini`和`task_list.txt`3个文件到本地，放到一个目录下  
### 配置
打开`config.ini`  
添加绅士站的用户名和密码  
添加`SAVEDIR`，其为保存图片的目录；当此参数为空时，会下载到程序所在目录
配置其他参数（当然也可以使用默认参数） 
`SAVEDIR` 保存图片的目录；当此参数为空时，会下载到程序所在目录  
`THREAD` 一个gallery任务中同时运行的线程数  
`TRYNUM`  下载某张图片，遇到错误时是否重试，及其次数  
`TIMEOUT` 下载某张图片，是否超时  
`RENAME` 下载某个gallery时，是否会重命名图片，重命名的规则是根据gallery图片数量大小，从1/01/001(以此类推)递增  
`ORIGINAL_PIC` 是否下载原始图片  
`LOG` 是否记录日志，这里包括gallery信息的info.txt和下载失败时会出现的fail_log.txt  
`CONTINUEDOWNLOAD` 是否继续下载上次未完成的gallery；注意：由于设计上的一些原因，程序不会下载所有未完成gallery  
   
 保存`config.ini`
### 加入任务
打开`task_list.txt`，填入要下载的gallery url，保存  
  
支持下载该gallery特定的页码，方法是在url后加入()，括号内填入数字，或数字-数字，例如  
.../**g**/xxx/xxxx/(1-30)  
.../**g**/xxx/xxxx/()  
支持填入多个url，url之间以换行或英文逗号分割  
### 运行主程序
运行main.exe  
运行时/运行后会有一些文件生成，分别是  
`local_cookies.json` 用于记录cookies形式的用户信息，程序会首先找这个文件，用其中信息来登录  
`last_gallery_download_task.json` 用于记录上次未完成的gallery中url  
