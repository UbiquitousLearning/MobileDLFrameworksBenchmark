
## 项目说明
本项目用于生成`yaml配置`以配合集群部署服务服务以`Matrix Build` 形式对不同 Commit 进行批量编译.


## 运行环境
Python 3.9 on macOS 11.2

> 部分特性依赖于Python 3.6+
## 文件说明

[commits.py](commits.py) 用于调用`Github RestFul API`获取指定仓库的 Weekly Commit. 根据脚本开头定义的仓库OWNER与仓库名称(REPO)获取,生成"{FILENAME}_commits.json"文件供后续读取.

[tf_compile_template.yaml](tf_compile_template.yaml)/[ncnn_compile_template.yaml](ncnn_compile_template.yaml) `Github Actions`编译模板,包含编译所需流程.

[json_to_yaml.py](json_to_yaml.py) 用于生成yaml配置文件.以 `ncnn_compile_template.yaml`或 `tf_compile_template.yaml`为模板,读取"{FILENAME}_commits.json"文件中的`commit sha`与`日期`,生成编译配置文件.生成的配置文件将以20个commit为一个job,5个job为一次执行的形式并行进行编译.
并生成 "{Date}.zip"的编译产物.

[download_artifacts.py](download_artifacts.py) 用于下载编译生成的产物(artifacts).根据脚本开头定义的仓库OWNER与仓库名称(REPO),与`run_id`数组中信息获取,`run_id`即RUN运行结果 URL中的id数字部分.脚本将自动下载编译产物到"{REPO}/{item['name']}.zip",并进行解压生成`{item['name']}`子目录.

[adbTest.py](adbTest.py) 调用`adb 命令行`进行操作.流程包括 `遍历指定目录` `push所需文件` `赋权执行` `保存日志`.不同框架命令不同,参见注释.产物为 "adbLogs"文件夹下执行输出.

prase_log_*.py 分析命令输出日志,生成csv文件.目前只提取`Model_Name`指定网络 Benchmark.


[prepare_bazel.py](prepare_bazel.py) 用于在编译前对Bazel进行必需的配置,包括生成NDK路径,生成供`bazelisk`配置使用的.bazelversion,生成编译指令等.无法在本地执行,用途是在`Github Actions Runner` 中执行进行编译前置配置.请结合 `tf_compile_template.yaml`.


.bazel*文件,configure.py,WORKSPACE,actions_build.sh等  均为 `TensorFlow Lite`环境配置脚本`prepare_bazel.py`的依赖与产物.prepare_bazel.py 利用这些文件检测 当前版本与控制编译流程.测试时使用.

> _PS_
> 
> 对于早期NCNN Benchmark,一些动态依赖未编译打包,需自行将依赖放入 /data/local/tmp/ 并指定 export LD_LIBRARY_PATH=/data/local/tmp.
> 这里准备了ARMv8(aarch64)版本的libomp.so放置于项目根目录(来自Clang 11.05 Darwin Prebuilt),可以尝试使用.
