# 原始项目
https://huggingface.co/spaces/ResembleAI/Chatterbox

# 安装
```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
cat /data/work/frp/frpc.ini 
vim /data/work/frp/frpc.ini

# 后台
[ssh-chatterbox]
type = tcp
local_ip = 127.0.0.1
local_port = 6796
remote_port = 6796
use_encryption = false
use_compression = false
```
# 重启frp
sudo systemctl restart  supervisor
sudo supervisorctl reload
sudo supervisord