# WatchmanRouteProblem
## 一、当前进度
- 完成kernel计算
- 完成visibility计算
- 完成最大凸多边形计算
- TPP问题
- HouseExpo数据集
- 多进程优化速度
## 二、后续规划
- 速度优化
- bugfix
- 接口封装

## 三、依赖安装
```bash
pip install -r requirements.txt
```

## 四、测试方法

1. 简单测试：
```bash
python3 run_test.py 
#如果出现错误，可以尝试重新运行
```
2. 测试指定种子
```bash
python3 run_test.py number [0 <= number <= 30000]
```
测试结果的可视化形式可在项目根目录下生成的 test 文件夹下查看。
## 五、文件结构

WRP问题解决步骤：

```c
求出多边形最大凸多边形子集(MACS) -> 遍历凸多边形子集(GTSP)
```

```bash
WatchmanRouteProblem
├── README.md 
├── requirements.txt #python 依赖库
├── run_test.py #测试运行脚本
└── wrpsolver #主文件夹
    ├── GTSP #遍历凸多边形子集算法
    │   ├── astar
    │   ├── gtsp.py
    │   ├── __init__.py
    │   └── samples.py
    ├── __init__.py
    ├── MACS #求出多边形最大凸多边形子集算法
    │   ├── compute_kernel.py
    │   ├── compute_visibility.py
    │   ├── __init__.py
    │   ├── polygons_coverage.py
    ├── Test #测试所用文件
    │   ├── draw_pictures.py
    │   ├── __init__.py
    │   ├── json #数据集
    │   ├── map_id_35000.txt #数据集的样本
    │   ├── vis_maps.py #从数据集生成多边形
    │   ├── test.py #测试文件
    └── WRP_solver.py #main函数
```