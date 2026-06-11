# Rockchip RK3288 Android 11

## Rockchip RK3288 Android 11 OTA 固件

### 文件来源

`firmware/update_smdt.zip` — Rockchip RK3288 设备的 Android 11 OTA 增量更新包。

### 设备信息

| 项目 | 内容 |
|---|---|
| 品牌 | SMDT (视美泰) |
| 平台 | Rockchip RK3288 |
| 设备名 | `rk3288_Android11` |
| Android 版本 | 11 (API 30, SDK level 30) |
| 构建类型 | userdebug |
| 构建指纹 | `rockchip/rk3288_Android11/rk3288_Android11:11/RD2A.211001.002/eng.lxw.20250305.235808:userdebug/release-keys` |
| 构建用户 | eng.lxw |
| 构建时间 | 2025-03-05 23:58:08 |
| 安全补丁级别 | 2021-10-01 |
| OTA 类型 | BLOCK 模式增量更新 |

### 分区镜像

| 分区 | 文件 | 说明 |
|---|---|---|
| `system` | `system.new.dat.br` | 系统分区 (brotli 压缩) |
| `vendor` | `vendor.new.dat.br` | 厂商分区 |
| `product` | `product.new.dat.br` | 产品分区 |
| `odm` | `odm.new.dat.br` | ODM 分区 |
| `system_ext` | `system_ext.new.dat.br` | 系统扩展分区 |
| `boot` | `boot.img` | 内核镜像 |
| `trust` | `trust.img` | TrustZone 固件 |
| `uboot` | `uboot.img` | U-Boot 引导加载程序 |
| `dtbo` | `dtbo.img` | Device Tree Blob Overlay |

> 每个 `.dat.br` 分区镜像均附带 `.transfer.list` (增量差异列表) 和 `.patch.dat` (补丁数据)，此为增量 OTA 包，需基于旧版系统才能应用更新。

---

## Rockchip RK3288 Android 11 完整固件镜像 (upgrade_tool)

### 文件来源

`firmware/smdt_3288A_userdebug_20250305_235357.img` — Rockchip RK3288 设备的 Android 11 **全量固件烧录包** (非 OTA，可用于空片烧录)。

### 文件信息

| 项目 | 内容 |
|---|---|
| 格式 | Rockchip Firmware Image (RKFW + Image Table) |
| 大小 | ~1.8 GB |
| 包含 | Bootloader + 全部分区镜像 |
| 烧录方式 | `upgrade_tool` / `rkdeveloptool` |

设备信息与上方 OTA 包一致（同一构建版本）。

### 分区布局 (基于 parameter 文件)

| 分区 | 块地址偏移 | 大小 | 说明 |
|---|---|---|---|
| `security` | 0x00002000 | 4MB | 安全分区 |
| `uboot` | 0x00004000 | 4MB | U-Boot 引导程序 |
| `trust` | 0x00006000 | 4MB | TrustZone 固件 (ATF) |
| `misc` | 0x00008000 | 4MB | 启动模式控制 |
| `oempriv` | 0x0000a000 | 8MB | OEM 私有数据 |
| `smdt` | 0x0008a000 | 4MB | SMDT 厂商数据 |
| `dtbo` | 0x0008c000 | 4MB | Device Tree Blob Overlay |
| `vbmeta` | 0x0008e000 | 1MB | Verified Boot 元数据 |
| `boot` | 0x0008e800 | 20MB | Linux Kernel + initramfs |
| `recovery` | 0x000a2800 | 48MB | Recovery 恢复系统 |
| `backup` | 0x000d2800 | 96MB | 备份分区 |
| `cache` | 0x00192800 | 96MB | 缓存 |
| `metadata` | 0x00252800 | 4MB | 元数据 |
| `baseparameter` | 0x0025a800 | 1MB | 基础参数 |
| `super` | 0x0025b000 | ~95MB | 动态分区 (system/vendor/product/odm/system_ext) |
| `userdata` | 0x0086f000 | 剩余空间 | 用户数据 (grow) |

> 块地址以 512 字节为一个扇区（sector）。此镜像包含完整 Bootloader（DDR 初始化、USB 下载模式、U-Boot），可通过 Rockchip `upgrade_tool` 或 `rkdeveloptool` 直接烧录到 eMMC 空片，**无需先有系统**。

---



# 6320SE-20260428（Android 9）增加烧录MAC地址功能



## HiSilicon GK6320V100 Android 机顶盒固件

### 文件来源

`firmware/6320SE-20260428（Android 9）增加烧录MAC地址功能/smdt_6323se_android_20260428_170559.zip` — SMDT 品牌海思 GK6320V100 芯片的 Android 机顶盒完整烧录包。

### 设备信息

| 项目 | 内容 |
|---|---|
| 品牌 | SMDT (视美泰) |
| 芯片型号 | HiSilicon GK6320V100 (6323SE) |
| 系统 | Android |
| 构建时间 | 2026-04-28 17:05:59 |
| 包类型 | 完整 eMMC 烧录包 (含分区表 XML) |

### 分区表 (基于 `GK6320V100-emmc.xml`)

| 分区 | 文件 | 大小 | 起始地址 | 文件系统 |
|---|---|---|---|---|
| `fastboot` | `fastboot.bin` | 1M | 0M | none |
| `bootargs` | `bootargs.bin` | 512K | 1M | none |
| `bootargsbak` | `bootargs.bin` | 512K | 1536K | none |
| `recovery` | `recovery.img` | 20M | 2M | none |
| `securestore` | `securestore.ext4` | 8M | 24M | ext3/4 |
| `atf` | `bl31.bin` | 2M | 32M | none |
| `baseparam` | `baseparam.img` | 8M | 34M | none |
| `pqparam` | `pq_param.bin` | 8M | 42M | none |
| `dtbo` | `dtbo.img` | 2M | 50M | none |
| `logo` | `logo.img` | 10M | 52M | none |
| `recoverybak` | `recovery.img` | 20M | 92M | none |
| `boot` | `kernel.img` | 60M | 112M | none |
| `system` | `system.ext4` | 1200M | 212M | ext3/4 |
| `cache` | `cache.ext4` | 800M | 1412M | ext3/4 |
| `vendor` | `vendor.ext4` | 400M | 2212M | ext3/4 |
| `backup` | `backup.ext4` | 800M | 2612M | ext3/4 |
| `private` | `private.ext4` | 50M | 3412M | ext3/4 |
| `userdata` | `userdata.ext4` | 剩余空间 | 3466M | ext3/4 |

> 使用 Hitool 或海思烧录工具配合 XML 分区表刷入 eMMC。

---

## HiSilicon GK6320V100 Android 9 Factory 工厂升级包

### 文件来源

`firmware/6320SE-20260428（Android 9）增加烧录MAC地址功能/update-factory_20260428_170559.zip` — 海思 GK6320V100 芯片的 Android 9 Factory OTA 工厂升级包 (产线烧录/售后恢复)。

### 设备信息

| 项目 | 内容 |
|---|---|
| 平台 | HiSilicon GK6320V100 |
| Android 版本 | 9 (API 28, SDK level 28) |
| 构建类型 | userdebug / test-keys |
| 构建指纹 | `GkSTBAndroid/GK6320V100/GK6320V100:9/PPR1.180610.011/cj04281706:userdebug/test-keys` |
| 构建用户 | cj |
| 构建时间 | 2026-04-28 17:06:18 |
| 安全补丁级别 | 2021-06-10 |
| OTA 类型 | BLOCK 模式 |
| 设备路径 | `/dev/block/platform/soc/f9830000.gkmciv200.MMC` |

### 包结构

```
├── bl31.bin                     # ARM Trusted Firmware
├── bootargs.bin                 # 启动参数
├── fastboot.bin                 # Fastboot 引导
├── recovery.img                 # Recovery 镜像
├── update.zip                   # 完整 OTA 包 (可能)
└── update/
    ├── META-INF/                # OTA 升级脚本
    ├── system.new.dat.br        # 系统分区 (brotli)
    ├── system.patch.dat         # 系统增量补丁
    ├── system.transfer.list
    ├── vendor.new.dat.br        # 厂商分区
    ├── vendor.patch.dat
    ├── vendor.transfer.list
    ├── boot.img                 # 内核
    ├── recovery.img             # Recovery
    ├── recoverybak.img          # Recovery 备份
    ├── fastboot.img             # Fastboot
    ├── bl31.img                 # ATF
    ├── logo.img / dtbo.img      # 开机画面 / DTBO
    ├── pqparam.img              # PQ 参数
    ├── baseparam.img            # 基础参数
    ├── bootargs.img / bootargsbak.img  # 启动参数
    ├── cache.img                # Cache 分区完整镜像
    ├── userdata.img             # Userdata 分区完整镜像
    └── wipedata.flag            # 清除数据标志
```

### 升级流程

脚本分两阶段执行：

1. **Stage 1/2** — 刷写 `recoverybak`、`bootargsbak`，设置 misc 分区状态为 `"b"`
2. **Stage 2/2** — 依次刷写 `recovery`、`bootargs`、`fastboot`、`atf`、`logo`、`pqparam`、`tee`、`dtbo`，然后格式化 `cache` 分区并写入 `cache.img`，再通过 block_image_update 更新 `system` 和 `vendor`，最后写入 `boot`、`userdata` (格式化+写入)、`baseparam`

> 与 `smdt_6323se` 同平台但用途不同：前者是 Hitool 完整 eMMC 烧录包，后者是通过 Recovery 刷写的工厂升级包。

---

## HiSilicon GK6320V100 Android 9 Factory OTA (不擦除数据版)

### 文件来源

`firmware/6320SE-20260428（Android 9）增加烧录MAC地址功能/update_smdt.zip` — 海思 GK6320V100 芯片的 Android 9 Factory OTA 包，**不擦除用户数据**。

### 设备信息

| 项目 | 内容 |
|---|---|
| 平台 | HiSilicon GK6320V100 |
| Android 版本 | 9 (API 28, SDK level 28) |
| 构建指纹 | `GkSTBAndroid/GK6320V100/GK6320V100:9/PPR1.180610.011/cj04281706:userdebug/test-keys` |
| 构建用户 | cj |
| 构建时间 | 2026-04-28 17:06:18 |
| 安全补丁级别 | 2021-06-10 |
| OTA 类型 | BLOCK 模式 |
| 包大小 | 448MB |

### 与 `update-factory_20260428_170559` 对比

| 项目 | `update-factory` | `update_smdt-2` |
|---|---|---|
| 格式化 cache/userdata | ✅ 是 | ❌ 否 |
| `system.patch.dat` / `vendor.patch.dat` | 有内容 (增量) | **0 字节** (全量替换) |
| 脚本判断逻辑 | 固定顺序 | `get_stage` / `get_recovery_state` 条件判断 |
| `cache.img` / `userdata.img` | 包含 | 不包含 |
| 用途 | 产线烧录/售后恢复 | 系统升级更新，**保留用户数据** |

### 包结构

```
├── META-INF/                     # OTA 升级脚本 + 证书
├── system.new.dat.br  (392MB)    # 系统完整镜像 (全量替换)
├── system.patch.dat   (0B)      # 空补丁
├── system.transfer.list
├── vendor.new.dat.br   (38MB)   # vendor 完整镜像
├── vendor.patch.dat    (0B)
├── vendor.transfer.list
├── boot.img            (11MB)   # 内核
├── recovery.img        (14MB)   # Recovery
├── recoverybak.img     (14MB)   # Recovery 备份
├── fastboot.img       (540KB)   # Fastboot
├── bl31.img            (55KB)   # ATF
├── bootargs.img / bootargsbak.img  # 启动参数
├── dtbo.img / logo.img / pqparam.img / baseparam.img
└── cache.img          (283KB)   # 缓存分区 (不格式化，直接写入)
```

> 与 `update-factory` 同一天同一构建，但此为**保留数据的固件升级包**，`system` 和 `vendor` 使用全量替换 (patch 为 0 字节)。

---

# HiSilicon Hi3751V660 Android TV BL2/SBL 固件

### 文件来源

`firmware/CSP60_AH_BASE.rar` — 海思 Hi3751V660 芯片的完整 BL2/SBL 阶段固件 (Ctv_Update_660.bin)。

### 基本信息

| 项目 | 内容 |
|---|---|
| 压缩包大小 | ~574 MB |
| 解压后大小 | ~1.42 GB (仅含 Ctv_Update_660.bin) |
| 芯片平台 | HiSilicon Hi3751V660 (华为海思) |
| 硬件代号 | `huanglong` (黄龙) |
| 系统类型 | Android TV |
| 固件版本 | `v120v2.2.8` |
| 构建日期 | 2024-08-14 15:24:08 |
| 源码路径 | `HisiV660/vendor/open_source/u-boot/u-boot-2022.07` |
| 打包格式 | 海思 `LOAD` 格式 |

### 作用

这是 Hi3751V660 芯片的**完整启动链固件**，包含从 SBL (Second Boot Loader) 到 Android bootargs 的所有启动阶段镜像。适用于视美泰(SMDT)等厂商基于该芯片的智能显示/电视设备。通过海思 `LOAD` 格式打包，包含多个独立的启动阶段镜像。

### 固件分区布局

| 分区 | 大小 | A/B | 说明 |
|---|---|---|---|
| `fastboot` | 1MB | - | Fastboot 引导 |
| `bootargs` / `bootargsbak` | 1MB×2 | A/B | 启动参数 |
| `sbl` / `sblbak` | 4MB×2 | A/B | 第二启动加载器 (DDR 训练) |
| `batt_nv` | 1MB | - | 电池参数 |
| `ddrparam` | 1MB | - | DDR 参数 |
| `dtbo` / `dtbobak` | 10MB×2 | A/B | 设备树叠加层 |
| `hrf` | 1MB | - | HRF 分区 |
| `sensorhub` | 1MB | - | Sensor Hub |
| `dmcu` | 4MB | - | 显示 MCU |
| `slaveboot` / `slavebootbak` | 4MB×2 | A/B | 从启动 |
| `reserved1` | 3MB | - | 保留 |
| `atf` / `atfbak` | 2MB×2 | A/B | ARM Trusted Firmware |
| `hhee` / `hheebak` | 3MB×2 | A/B | 华为可信执行环境 |
| `trustedcore` / `trustedcorebak` | 10MB×2 | A/B | 可信核心 |
| `boot` | 60MB | - | 内核 + ramdisk |
| `ramdisk` | 3MB | - | RAM Disk |
| `recovery` / `recoverybak` | 60MB×2 | A/B | Recovery 恢复系统 |
| `reserved2` | 49MB | - | 保留 |
| `deviceinfo` | 2MB | - | 设备信息 |
| `misc` | 1MB | - | 启动模式控制 |
| `versioninfo` | 1MB | - | 版本信息 |
| `logo` | 40MB | - | 开机 Logo |
| `bootmusic` / `bootmusicsec` | 10MB×2 | - | 开机音乐 |
| `panel` / `panelbak` | 48MB×2 | A/B | 屏幕面板固件 |
| `demura` | 4MB | - | Demura 校正 |
| `baseparam` | 8MB | - | 基础参数 |
| `reserved3` | 40MB | - | 保留 |
| `vbmeta_system` / `vbmeta_vendor` | 1MB×2 | - | Verified Boot 元数据 |
| `super` | 3640MB | - | Android 动态分区 |
| `product` | 400MB | - | 产品分区 |
| `odm` | 54MB | - | ODM 分区 |
| `cache` | 800MB | - | 缓存 |
| `securestore` | 8MB | - | 安全存储 |
| `dfx` | 16MB | - | DFX 诊断 |
| `eng` | 50MB | - | 工程模式 |
| `reserved4` | 53MB | - | 保留 |
| `metadata` | 16MB | - | 元数据 |
| `userdata` | 剩余空间 | - | 用户数据 |

### DDR 配置支持

| 配置 | 规格 | 用途 |
|---|---|---|
| hi3751v660dma | DDR4-3200 4GB (16bit×2, 2层板) | 主配置 |
| hi3751v660dmb | LPDDR4-2933 4GB (32bit×1, 2层板) | 备选 |
| hi3751v660dmb | LPDDR4X-2933 4GB (32bit×1, 2层板) | 备选 |

### 启动参数

```
androidboot.hardware=huanglong
androidboot.selinux=permissive
androidboot.boot_devices=soc/ff060000.emmc
androidboot.serialno=0123456789
console=ttyAMA0,115200
earlycon=pl011,0xf8b00000
pq=noacmuhd
```

### A/B 分区策略

支持 A/B 双分区升级的分区：`sbl`, `dtbo`, `slaveboot`, `recovery`, `atf`, `trustedcore`

### 构建环境信息

- 源码路径: `/home/estwork/zhangwenbin/work/HisiV660/vendor/open_source/u-boot/u-boot-2022.07/`
- 硬件平台: `huanglong` (黄龙)
- 网络驱动: `hlsfv300` (MDIO/NET)
- 安全特性: 支持加密、Hash、RSA 等安全启动链
