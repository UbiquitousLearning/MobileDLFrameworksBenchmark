# Mobile-DL-benchmark

A Comprehensive Benchmark of Deep Learning Libraries on Mobile Devices.

> This framework is  an implementation of our paper( [A Comprehensive Benchmark of Deep Learning Libraries on Mobile Devices](#TBD) ),and it is based on TFLite,ncnn,Mace,MNN,PytorchMobile,SNPE and other libs. 

##  <a name='TableofContents'></a>Table of Contents
*  [Background](#Background)
*  [Overview](#Overview)
*  [Framework Composition](#FrameworkComposition)
	* [DL Libraries Prebuilt Binaries](#DLLibrariesPrebuiltBinaries)
	* [Model Convertors](#ModelConvertors)
	* [DL Libs Benchmark](#DLLibsBenchmark)
	* [DL Libs Longitudinal Analysis](#DLLibsLongitudinalAnalysis)
* [Milestore](#Milestore)

##  1. <a name='Background'></a>Background



Deploying deep learning (DL) on mobile devices has been a notable trend in recent years. To support fast inference of on-device
DL, DL libraries play a critical role as algorithms and hardware do.


In this repo, we first build a comprehensive benchmark
that includes 6 representative DL libs and 15 diversified DL models.
##  2. <a name='Overview'></a>Overview
 We first build a comprehensive benchmark for on device DL inference, namely MDLBench. The benchmark includes
6 popular, representative DL libs on mobile devices, i.e., `TFLite`,
`PyTorchMobile`,` ncnn`,` MNN`,` Mace`, and `SNPE`. It contains 6 DL models compatible with all above DL libs and 8 models compatible with at least 3 above DL libs, spanning from image classification, object detection, to NLP. Compared to existing
AI benchmarks , our benchmark triumphs at the aspect of rich support for various DL libs and models. In addition to the completeness, we also instrument the DL libs to obtain underlying performance details such as per-operator latency, CPU usage, etc.
Those details allow us to peek into the intrinsic features of those DL libs and therefore provide more insightful implications to developers.

##  3. <a name='FrameworkComposition'></a>Framework Composition
Our Framework is composed of the following components, which located in different sub-folders.Due to the limitations of Github and project licences, we only provide some links to them. You may need to download or build them yourself.Please read README in those sub-folders for more information.

###  3.1. <a name='DLLibrariesPrebuiltBinaries'></a>DL Libraries Prebuilt Binaries
We build some binaries of [`TFLite`](./tensorflow), [`ncnn`](./ncnn),[`MNN`](./MNN),[`PytorchMobile`](./pytorchM) for your test.All binaries are built for ARM64(aarch64) only.
But you can also build your own binaries for your device,just build and replace those binaries with yours.

SNPE has strict license that disallows redistribution so we cannot provide binaries, please download and place them in [SNPE](./snpe) sub-folder.

MACE requires device-specific build settings, so it is not included in this repo.Please clone the repository to [MACE_master](./Convertors/MACE-master).Read the [README](./Convertors/README) documentation for more information.

###  3.2. <a name='ModelConvertors'></a>Model Convertors

We build some tools to convert DL models between different frameworks in [Converntors](./Convertors).Basically the conversion flow usually starts from TensorFlow GraphDef/SavedModel files(for TFLite,Mace,MNN,SNPE) or from Pytorch TorchScript files(for PyTorchMobile,ncnn,SNPE).
Conversion between TensorFlow GraphDef/SavedModel and Pytorch TorchScript is not included in this repo.A feasible way to convert is to use [pytorch2keras](https://github.com/gmalivenko/pytorch2keras) or similar tools.

> [SNPE](https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk) has strict license that disallows redistribution, so the converter for it is not included.
> 
> Some large models are not included in this repo,but we provided links for them.Please read README for more information in ./Convertors.

###  3.3. <a name='DLLibsBenchmark'></a>DL Libs Benchmark
We offer benchmarks for `TFLite`,`PyTorchMobile`,` ncnn`,` MNN`,` Mace`, and `SNPE`. You should convert models and build necessary libs before running the benchmarks.

We place some `.py` files in name of DL libs to provide a simple way to run the benchmarks separately.
If you want to run the benchmarks together,after device connected,you can use the following command:
```shell
pip3 install -r requirements.txt
python3 main.py
```
> Remember that SNPE only supports Linux x86_64 architecture, and Ubuntu 18.04 is suggested. Please do not run `snpe.py` on unsupported platforms. \
> Note that we only support benchmarks on One device now since the SNPE  and Mace may not optimize for multi-device.

We also provide the benchmarks on every operator in the model for comparison.See files in [opTest](./opTest) for more information.
There are also several code to track the CPU usage of DL libs benchmarks in [CPUtest](./CPUtest).
###  3.4. <a name='DLLibsLongitudinalAnalysis'></a>DL Libs Longitudinal Analysis
We then perform a longitudinal analysis to understand how the performance of DL libs evolve across time.
We select `TFLite` and `ncnn` for their long open source history.

See [GetFrameworkHistory](./GetFrameworkHistory) for more instructions.

##  4. <a name='Milestore'></a>Milestore
1. Support more DL libs, like TNN.
2. Support more DL models(NLP/Transformer etc.) running on different libs.
