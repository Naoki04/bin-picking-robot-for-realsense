Not all code is uploaded yet.
# Fast Graspbaility Evaluation for RealSense
Fast Graspability Evaluation(FGE) is an algorithm for estimating the grasp pose from depth maps and gripper parameters. Based on an implementation by [Xinyi](https://github.com/xinyiz0931/bin-picking-robot), this repository shows how to use FGE with a RealSense camera for a food manipulation task. For RoboSoft Competition (Manipulation) 2023 @Singapore, we added features such as image pre-processing.

# Overview
1. RealSenseから深度マップを取得
2. クリッピング
3. 正規化：本来は深度マップをキャリブレーションして物理的な値に基づいてFGEを適応するべきですが、実装を簡単にするために深度画像をReLu型関数によって正規化します。
4. FGE
5. フィルタリング

# Demonstration
## Test Environment
RoboSoft Competition (Manipulation) 2023 @Singapore の課題設定の基づいて、画像のようなbin内の食品に対してFGEを適応します。
```
$ pip install -e .
$ python 
```

# Changes from Xinyi's repository


# Reference
  - Original Repository: [xinyiz0931/bin-picking-robot](https://github.com/xinyiz0931/bin-picking-robot)
  - Original Paper: [Yukiyasu Domae, et al., Fast graspability evaluation on single depth maps for bin picking with general grippers, ICRA2014](https://ieeexplore.ieee.org/document/6907124)