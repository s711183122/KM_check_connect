# KM_check_connect
## 本程式用於自動檢查某一伺服器連線狀況，並架設於 fly.io 雲託管平台。

自架網頁伺服器在學校、公司、家庭時，有時候會遇到未知連線問題，
因此這時候就需要一個架設在雲端，會自動檢查是否可連線的程式，
有任何狀況會發送 Email 通知！


## 功能

- 自動檢查指定伺服器是否可正常連線
- 遇到連線問題時會寄電子郵件通知
- 重新連線時也會寄電子郵件通知

## 安裝方式

### 複製本程式至你的電腦
```sh
git clone https://github.com/s711183122/KM_check_connect.git
cd KM_check_connect
```
### 修改 config.py
> Note: 請按照[此篇](https://wiki.eztrust.com.tw/webdesign/D/1360) 獲得自己的 Gmail SMTP 密碼

![](img\md_pc1.png)

### 修改 receivers.txt
> Note: 請在此輸入所有接收者的電子郵件信箱

![](img\md_pc2.png)

### 建立 [Fly.io](https://fly.io/) 帳號

![](img\md_pc_fly.png)

### 安裝 fly-cli 至電腦
[請參照此網址進行安裝](https://fly.io/docs/hands-on/install-flyctl/)

![](img\md_pc_fly2.png)

### 推上 fly.io 伺服器
請修改 fly.toml 中的 APP 名稱

![](img\md_pc_flytoml.png)

執行以下指令建立新的 APP
```sh
fly launch
```
![](img\md_pc_fly_deploy.png)
```sh
flyctl deploy
```
![](img\md_pc_fly_deploy2.png)

由於預設會建立兩個虛擬機 請使用以下指令設定為一個
```sh
fly scale count 1
```
![](img\md_pc_fly_deploy3.png)

可使用上方的網址進行手動檢測
## License

MIT

**Free Software, Hell Yeah!**