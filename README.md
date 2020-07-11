## 介绍
本项目游戏环境飞翔之桨（Flappy Paddle），是在Flappybird的基础上修改而来，该游戏中玩家必须操控飞舟划桨躲避海洋中袭来的鲨鱼。

### 有效动作

- 向上飞：向上会使鸟儿/小舟向上加速。
- 无动作： 小鸟/小舟会向下坠落

### Reward

穿过的每条管道/鲨鱼都会获得+1 的正回报。每次游戏结束时，它都会收到-1 的负奖励。

## 使用环境包

- PyGame Learning Environment (PLE)
  是一种 learning 环境，，可以快速开始使用 Python 进行强化学习。
  github: https://github.com/ntasfi/PyGame-Learning-Environment

文档：https://pygame-learning-environment.readthedocs.io/en/latest/

- PARL
  PARL 是百度开发的一个高性能、灵活的强化学习框架。其提供了高质量的主流强化学习算法实现，最高可支持上万个 CPU 的同时并发计算，并且支持多 GPU 强化学习模型的训练，可复用性强，具有良好扩展性。

github：https://gitee.com/PaddlePaddle/PARL
文档：https://parl.readthedocs.io/en/latest/

### 安装
```
pip install requirements.txt
ps：安装ple
需要先clone https://github.com/ntasfi/PyGame-Learning-Environment 
然后在PyGame-Learning-Environment目录执行 pip install -e .
```

## 算法使用
- DQN
使用这个算法后，发现效果很好，flappy_paddle下的`new_f_bird_dqn.py`

---

## PLE 的 FlappyBird 环境的使用

官方给出的使用方法是

```python
from ple.games.flappybird import FlappyBird
from ple import PLE


game = FlappyBird()
p = PLE(game, fps=30, display_screen=True)
agent = myAgentHere(allowed_actions=p.getActionSet())

p.init()
reward = 0.0

for i in range(nb_frames):
   if p.game_over():
           p.reset_game()

   observation = p.getScreenRGB()
   action = agent.pickAction(reward, observation)
   reward = p.act(action)
```

具体流程： 1.实例化游戏环境 2.实例化 agent 3.游戏初始化 4.训练学习

由于我们使用 parl 来完成 DQN 训练，我们需要对环境做适应性匹配。
而 PARL 的 DQN 构成`Model`、`Agent`、`ReplayMemory`,并不需要特意进行修改，只需要根据环境调整 model 和各参数即可。

这里列出我们做适应性匹配需要知道的主要函数：

```python
ple_env.getGameState()  # 获取当前的状态字典
ple_env.getActionSet()  # 获取动作列表
ple_env.act(action)     # 行动
ple_env.game_over()     # 返回游戏是否结束
ple_env.reset_game()    # 重置游戏
ple_env.getScreenRGB()  # 渲染当前画面
```

---
## 关于修改游戏
本人重写了FlappyBird类，在其_load_images的函数中替换成我自己二次制作的素材（在flappy_paddle的assets下）
关于制作素材所用的方法有：
- 增加图片透明通道
- 把不需要的图片区域设置成无色透明
- 图片尺寸缩小
- 图片融合
以上所有均写好相应函数，感兴趣的童鞋可以直接参考，文件在flappy_paddle的assets下

## 给画面添加分数
  这里重写env的step方法，在里面draw的时候把分数画上去，项目提供2个网上下载的分数，可自由修改颜色和大小，
  同时，在得分的时候会变换分数字体的大小。
```python
# 绘制分数 step
font_path = "assets/3D Isometric Bold.otf"
# font_path = "assets/00pneumatix.woff.ttf"
change_sizes = [40,55]
if self.last_score != self.score:
    self.counter += 1
    self.last_score = self.score
if self.counter > 1:
    self.counter = 0
sz = change_sizes[self.counter]

score_font = pygame.font.Font(font_path, sz)  # 创建一个font对象
color = (255, 87, 0)  # 定义字体的颜色
score_surface = score_font.render(str(int(self.score)), True, color)
self.screen.blit(score_surface,(10,10))

```

