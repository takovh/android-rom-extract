# 编码习惯
- 使用python时，用uv管理包
- 文件解压后放到项目根目录的 output 下
- unblob 
- `extract_yaffs_final.py` 可以用来解包 `YAFFS filesystem root entry (little endian), type root or directory, v1 root directory`
- `rkunpack.py` - Rockchip 固件解包工具。
  - 支持 RKAF/RKFW/RKFP 三种固件格式。
  - 用法: `python rkunpack.py [-o OUTPUT] [-r] update.img`
  - 选项: `-o` 指定输出目录, `-r` 递归解包内嵌镜像
- `simg2img.py` - Android sparse image 转换为 raw image 工具
  - 用法: `python simg2img.py input.img output.img`
  - unblob 也支持sparse解包
- `lpunpack.py` - 安卓动态分区 super.img 固件解包工具。
  - 对于sparse格式，会先解为原始文件系统镜像 super.unsparse.img， 再解出各个分区
  - 用法: `python lpunpack.py [-h] [-p NAME] [-S NUM] SUPER_IMAGE OUTPUT_DIR`
  - unblob 也可以解包 super.img 动态分区，但是会丢失各个分区的名称

# unblob

```
Usage: unblob [OPTIONS] FILE

  A tool for getting information out of any kind of binary blob.

  You also need these extractor commands to be able to extract the supported
  file types: 7z, debugfs, fsck.erofs, jefferson, lz4, lziprecover, lzop,
  partclone.restore, sasquatch, sasquatch-v4be, simg2img,
  ubireader_extract_files, ubireader_extract_images, unar, zstd

  NOTE: Some older extractors might not be compatible.

Options:
  -e, --extract-dir DIRECTORY     Extract the files to this directory. Will be
                                  created if doesn't exist.
  -f, --force                     Force extraction even if outputs already
                                  exist (they are removed).
  -d, --depth INTEGER RANGE       Recursion depth. How deep should we extract
                                  containers.  [default: 10; x>=1]
  -n, --randomness-depth INTEGER RANGE
                                  Entropy calculation depth. How deep should
                                  we calculate randomness for unknown files? 1
                                  means input files only, 0 turns it off.
                                  [default: 1; x>=0]
  -P, --plugins-path PATH         Load plugins from the provided path.
  -S, --skip-magic TEXT           Skip processing files with given magic
                                  prefix. The provided values are appended to
                                  unblob's own skip magic list unless --clear-
                                  skip-magic is provided. [default: BFLT,
                                  Erlang BEAM file, GIF, GNU message catalog,
                                  HP Printer Job Language, JPEG, Java module
                                  image, MPEG, MS Windows icon resource,
                                  Macromedia Flash data, Microsoft Excel,
                                  Microsoft PowerPoint, Microsoft Word,
                                  OpenDocument, PDF document, PNG, SQLite,
                                  TrueType Font data, Web Open Font Format,
                                  Windows Embedded CE binary image, Xilinx BIT
                                  data, compiled Java class, magic binary
                                  file, python]
  --skip-extension TEXT           Skip processing files with given extension
                                  [default: .rlib]
  --clear-skip-magics             Clear unblob's own skip magic list.
  -p, --process-num INTEGER RANGE
                                  Number of worker processes to process files
                                  parallelly.  [default: 16; x>=1]
  --report PATH                   File to store metadata generated during the
                                  extraction process (in JSON format).
  --log PATH                      File to save logs (in text format). Defaults
                                  to unblob.log.
  -s, --skip-extraction           Only carve chunks and skip further
                                  extraction
  --no-sandbox                    Disable Landlock sandboxing (useful for
                                  breakpoint-based debugging).
  -k, --keep-extracted-chunks     Keep extracted chunks
  --delete-extracted-files TEXT   Delete fully extracted intermediate files
                                  (whole-file chunks only). Use
                                  'selected:<handler1,handler2>' (comma-
                                  separated) to restrict deletions to specific
                                  handlers.  [default: none]
  --carve-suffix TEXT             Carve directory name is source file + this
                                  suffix. NOTE: carving is skipped when the
                                  whole file is of a known type  [default:
                                  _extract]
  --extract-suffix TEXT           Extraction directory name is source file +
                                  this suffix  [default: _extract]
  -v, --verbose                   Verbosity level, counting, maximum level: 3
                                  (use: -v, -vv, -vvv)
  --show-external-dependencies    Shows commands needs to be available for
                                  unblob to work properly
  --build-handlers-doc TEXT       Build handlers markdown documentation
  --version                       Shows unblob version
  -h, --help                      Show this message and exit.
```

# 目录结构

```
android-firmware/
├── firmware/                           # 固件原始文件
├── output/                             # 解包输出目录
├── yaffshiv                            # YAFFS 文件系统解析/提取工具 (单文件脚本)
├── extract_yaffs_final.py              # YAFFS 解包脚本
├── simg2img.py                         # Android sparse image → raw image 转换工具
├── lpunpack.py                         # 安卓动态分区 super.img 固件解包工具
├── rkunpack.py                         # Rockchip 瑞芯微固件解包工具
├── main.py                             # 项目入口
├── pyproject.toml                      # Python 项目配置 (依赖: unblob)
├── AGENTS.md                           # 当前文件 - 项目说明与使用指南
├── README.md                           # 项目介绍
└── .gitignore
```



# 缩写

- SMDT: [视美泰|ShiMeta](https://www.shimeta.com.cn/)