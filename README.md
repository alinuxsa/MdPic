### 用FLASK实现的简单图床  

> 这是我的一个练手项目  
> 通过AutoHotkey调用client  
> 把剪切板里的图片上传到图床 返回图片地址  



* 启动服务  

  `python app.py`

* 修改文件路径  

  根据实际情况修改 `截图上传.ahk` 里面 client.exe的路径, 以及自定义快捷键

* 上传图片


  通过QQ截图  

  通过快捷键 `Alt + ,` 

  调用client上传, 成功后图片地址写在剪切板里，直接粘贴即可

* AutoHotkey 官网  

  [传送门](https://autohotkey.com/)