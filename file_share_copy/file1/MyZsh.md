# 终端美化-----oh-my-zsh的个性化配置

## 安装zsh

```shell
sudo apt install zsh
```

## 改变登陆shell

```shell
chsh -s /bin/zsh
```

## 安装oh-my-zsh

```shell
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
```

## oh-my-zsh个性化设置

### 主题

```shell
ZSH_THEME="fino-time"
```

### 插件

```shell
plugins=(git zsh-syntax-highlighting zsh-autosuggestions sublime)
```

#### git

```shell
# 配置目录
cat ~/.oh-my-zsh/plugins/git/git.plugin.zsh
```

#### zsh-syntax-highlighting

[官网](https://github.com/zsh-users/zsh-syntax-highlighting)

**安装**

克隆项目

```shell
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

在 `~/.zshrc` 中配置

```
plugins=(其他的插件 zsh-syntax-highlighting)
```

使配置生效

```
source ~/.zshrc
```

#### zsh-autosuggestions

[官网](https://github.com/zsh-users/zsh-autosuggestions)

**作用**

如图输入命令时，会给出建议的命令（灰色部分）按键盘 → 补全

如果感觉 → 补全不方便，还可以自定义补全的快捷键，比如我设置的逗号补全

```
bindkey ',' autosuggest-accept
```

在 `.zshrc` 文件添加这句话即可。

**安装**

克隆项目

```shell
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

在 `~/.zshrc` 中配置

```
plugins=(其他的插件 zsh-autosuggestions)
```

使配置生效

```
source ~/.zshrc
```