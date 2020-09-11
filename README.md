# IoT助手设备模拟器

提供多种硬件设备demo及模拟脚本

.
├── README.md
├── hardware //硬件实现代码
│   └── WiFi_control_switch_base_nodemcu //基于nodemcu实现的8路wifi控制器
│       ├── README.md
│       ├── main.py
│       ├── robust.py
│       └── simple.py
└── simulator //模拟设备代码
    ├── gateway //Python脚本在pc运行模拟网关
    │   ├── README.md
    │   ├── get_username_password.py
    │   └── main.py
    └── shares_monitoring //node-red运行股票监测
        └── main.py