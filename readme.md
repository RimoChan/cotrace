# 同事追踪器！

你是否有遇到过这样的问题，从同事那里接手了1份古代代码想要修改，却看得头昏脑胀，不知从哪里改起？

快使用<b>同事追踪器</b>吧！

<b>同事追踪器</b>使用数十种名贵药材，历经9年烹饪，并加入了珍稀的莉沫酱提取物，可以快速解决你的1切问题！

## 效果

假如你的同事写了这样1个工程，它用来煎几个荷包蛋然后吃掉，虽然听起来很简单但是实际上有1000行。

但是它上线以后经常崩溃，得尽快调查1下出错的原因。

```python
eggs = [*range(5)]
锅里 = []
餐桌 = []
def 打破(egg):
    try:
        import 奇怪的第三方库
    except Exception:
        ...
def 翻面(egg):
    马: None
def 铲出来():
    global 锅里
    t = 锅里
    锅里 = []
    return t
def 下锅(egg):
    锅里.append(egg)
def 煎蛋(eggs):
    for egg in eggs:
        打破(egg)
        下锅(egg)
    for _ in range(3):
        [*map(翻面, 锅里)]
    res = 铲出来()
    return res
def 做菜():
    菜 = []
    for i in range(0, len(eggs), 2):
        菜.extend(煎蛋(eggs[i:i + 2]))
    return 菜
def 上桌(t):
    餐桌.extend(t)
def 吃掉(egg):
    ...
t = 做菜()
上桌(t)
for egg in 餐桌:
    吃掉(egg)
```

接下来，只要你在入口文件的头部加上<b>同事追踪器</b>，然后重新运行代码——

```python
from cotrace import auto_call_trace
auto_call_trace([__file__])
```

就可以看到代码打印出了每个函数的实际调用关系和执行顺序啦！

```
时间 | 函数名                          位置 | 次数
==================================================
0.065|<module>                   [L1, 菜.py]|
0.065|  做菜                    [L33, 菜.py]|
0.065|    煎蛋                  [L25, 菜.py]|
0.066|      打破                [L11, 菜.py]|
0.067|      下锅                [L23, 菜.py]|
0.067|      打破                [L11, 菜.py]|
0.068|      下锅                [L23, 菜.py]|
0.068|      翻面                [L16, 菜.py]| * 6
0.068|      铲出来              [L18, 菜.py]|
0.069|    煎蛋                  [L25, 菜.py]|
0.069|      打破                [L11, 菜.py]|
0.069|      下锅                [L23, 菜.py]|
0.070|      打破                [L11, 菜.py]|
0.071|      下锅                [L23, 菜.py]|
0.071|      翻面                [L16, 菜.py]| * 6
0.071|      铲出来              [L18, 菜.py]|
0.071|    煎蛋                  [L25, 菜.py]|
0.071|      打破                [L11, 菜.py]|
0.072|      下锅                [L23, 菜.py]|
0.072|      翻面                [L16, 菜.py]| * 3
0.073|      铲出来              [L18, 菜.py]|
0.073|  上桌                    [L38, 菜.py]|
0.073|  吃掉                    [L40, 菜.py]| * 5
```

我们只需要读<b>同事追踪器</b>的结果，就可以理清这段代码的逻辑: 

蛋有5个，煎蛋被调用了3次，各煎了2/2/1个蛋，说明它是分块操作的。

每次煎蛋前要把蛋依次打破和下锅，全部下锅完了之后再1个1个翻面。最后再1口气铲出来。

最后再把5个蛋1起端上桌，然后1个1个吃掉。

然后我们就可以快速地发现代码里可以优化的地方，比如: 

- 上桌不是逐元素操作，可能蛋太多了1次端不上来？

- 煎蛋的流程太长了，可能前面的蛋最后都凉了？

之后你就可以有针对性地去优化同事的代码啦。

## 使用方法

你需要1个Python3.6以上版本，并通过pip安装cotrace。

```
pip install git+https://github.com/RimoChan/cotrace.git
```

安装好以后就可以`import cotrace`来使用啦。

接口说明: 

```python
def auto_call_trace(paths, *, width=None, indent=2): ...
```

+ `paths`: 需要追踪的文件的路径列表。当函数所在的文件(或其祖先目录)在这个列表里就会被追踪。  
   追踪当前文件可以用`[__file__]`。  
   追踪当前文件夹可以用`[__file__+'/..']`。

+ `width`: 输出的宽度，不指定的话就会以控制台宽度输出。

+ `indent`: 输出的缩进格数，调用栈每增加1层就会缩进1级。


## 使用例

比如，想要观察stable diffusion模型运行中，unet的耗时情况，可以这样用——

```python
import torch
from diffusers import StableDiffusionXLPipeline
from cotrace import auto_call_trace

pipe = StableDiffusionXLPipeline.from_single_file(
    "E:/stable-diffusion-webui/models/Stable-diffusion/ConfusionXL4.0_fp16_vae.safetensors",
    torch_dtype=torch.float16,
).to("cuda")

# 加上这1行
auto_call_trace(['E:/python311/Lib/site-packages/diffusers/models/unets'], width=152)

pipe(
    prompt=['1girl'],
    negative_prompt=['worst quality, low quality'],
    guidance_scale=7,
    generator=torch.Generator(device='cuda').manual_seed(1),
)
```

就会得到以下输出:

```
时间 | 函数名                                                                                                                                          位置 | 次数
==================================================================================================================================================================
0.308|<module>                                                                                                             [L1, c:\Users\我\Desktop\s\0t.py]|
0.308|  context_decorator.<locals>.decorate_context                                        [L113, E:\python311\Lib\site-packages\torch\utils\_contextlib.py]|
0.308|    StableDiffusionXLPipeline.__call__  [L819, E:\python311\Lib\site-packages\diffusers\pipelines\stable_diffusion_xl\pipeline_stable_diffusion_xl.py]|
0.309|      Module._wrapped_call_impl                                                     [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.309|        Module._call_impl                                                           [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.309|          UNet2DConditionModel.forward                             [L1039, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.309|            UNet2DConditionModel.get_time_embed                     [L909, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.324|            UNet2DConditionModel.get_class_embed                    [L935, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.324|            UNet2DConditionModel.get_aug_embed                      [L951, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.326|            UNet2DConditionModel.process_encoder_hidden_states     [L1003, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.399|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.399|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.400|                DownBlock2D.forward                                   [L1364, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.454|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.454|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.454|                CrossAttnDownBlock2D.forward                          [L1241, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.481|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.481|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.482|                CrossAttnDownBlock2D.forward                          [L1241, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.545|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.545|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.546|                UNetMidBlock2DCrossAttn.forward                        [L847, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.560|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.560|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.560|                CrossAttnUpBlock2D.forward                            [L2482, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.811|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.811|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.811|                CrossAttnUpBlock2D.forward                            [L2482, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.833|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.833|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.833|                UpBlock2D.forward                                     [L2617, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.933|      Module._wrapped_call_impl                                                     [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.933|        Module._call_impl                                                           [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.933|          UNet2DConditionModel.forward                             [L1039, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.933|            UNet2DConditionModel.get_time_embed                     [L909, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.934|            UNet2DConditionModel.get_class_embed                    [L935, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.934|            UNet2DConditionModel.get_aug_embed                      [L951, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.935|            UNet2DConditionModel.process_encoder_hidden_states     [L1003, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_condition.py]|
0.935|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.935|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.936|                DownBlock2D.forward                                   [L1364, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.939|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.940|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.940|                CrossAttnDownBlock2D.forward                          [L1241, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.949|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.949|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.949|                CrossAttnDownBlock2D.forward                          [L1241, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.975|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.975|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.975|                UNetMidBlock2DCrossAttn.forward                        [L847, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
0.990|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.990|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
0.990|                CrossAttnUpBlock2D.forward                            [L2482, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
1.023|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
1.023|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
1.023|                CrossAttnUpBlock2D.forward                            [L2482, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
1.031|            Module._wrapped_call_impl                                               [L1549, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
1.031|              Module._call_impl                                                     [L1555, E:\python311\Lib\site-packages\torch\nn\modules\module.py]|
1.031|                UpBlock2D.forward                                     [L2617, E:\python311\Lib\site-packages\diffusers\models\unets\unet_2d_blocks.py]|
```


## 结束

如果你觉得<b>同事追踪器</b>对你的工作或学习有所帮助，欢迎给作者送1些萝莉同事过来。

就这样，大家88，我要回去提炼莉沫酱了！
