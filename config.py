# 程式名稱
program_name = 'KM_check_connect'

# 接收者名稱
receivers_name = 'Receivers'

# 被檢測伺服器的網址
server_url = 'http://120.xxx.xxx.213/status'

# 檢查間隔 (秒)
check_interval_second = 1800

# 寄件者的 gmail
sender_email = 's711183122@gmail.com'

# SMTP伺服器
smtp_acc = 's711183122@gmail.com'
smtp_pass = '---'

# 檢查錯誤時所發送的文字
error_text = f'出事了阿伯！！！'

# 被檢測伺服器重新上線時發送的文字
re_connect_text = f'伺服器已重新上線\n由於伺服器曾發生過中斷，目前已重新連線。'



# 以下為本程式自動檢測的參數
check_alive_text = '每日線上檢測程式在線測試'
check_server_alive_para = {
    'day': '*/3', # */3 代表每隔三天
    # UTC+0 的 00:15:00 檢查本程式是否在線
    'hour': '00', 'minute': '15', 'second':'00'
}
close_text = f'線上檢測程式已關閉'

