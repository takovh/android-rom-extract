# 编码习惯
- 使用python时，用uv管理包
- extract_yaffs_final.py 可以用来解包 `YAFFS filesystem root entry (little endian), type root or directory, v1 root directory`
- 文件解压后放到项目根目录的 output 下


# 目录结构

```
android-firmware/
├── firmware/                          # 固件原始文件
├── output/                            # 解包输出目录
├── yaffshiv                            # YAFFS 文件系统解析/提取工具 (单文件脚本)
├── extract_yaffs_final.py              # YAFFS 解包脚本
├── main.py                             # 项目入口
├── pyproject.toml                      # Python 项目配置 (依赖: unblob)
├── AGENTS.md                           # 当前文件 - 项目说明与使用指南
├── README.md                           # 项目介绍
└── .gitignore
```



# 缩写

- SMDT: [视美泰|ShiMeta](https://www.shimeta.com.cn/)