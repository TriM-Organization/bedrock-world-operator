<h1 align="center">Bedrock World Operator</h1>
<h3 align="center">一个基于 Go 实现并为 Python 提供的网易（国际版）我的世界基岩版存档操作实现</h3>
<br/>
<p align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg">
<p>



[python]: https://img.shields.io/badge/python-3.11-AB70FF?style=for-the-badge
[license]: https://img.shields.io/badge/LICENSE-MIT-228B22?style=for-the-badge



[![][python]](https://www.python.org/)<br/>
[![][license]](LICENSE)<br/>







# 目录
- [目录](#目录)
- [简述](#简述)
  - [世界观](#世界观)
  - [受支持的操作系统及架构](#受支持的操作系统及架构)
  - [基础概念](#基础概念)
  - [基础功能](#基础功能)
  - [额外实现](#额外实现)
  - [实用功能](#实用功能)
- [兼容性](#兼容性)
- [快速上手](#快速上手)
- [注意事项](#注意事项)
- [🐍 Pypi 包](#-pypi-包)
- [其他](#其他)





# 简述
## 世界观
**Bedrock World Operator** 是一个以 **Go** 语言为底层，以动态库调用的方式，皆在为 **Python** 提供一个效率足够的我的世界基岩版存档操作器。

存档操作器的主要目的在于为网易我的世界基岩版（v1.20.51）提供支持（但不包含解密其存档的实现），即，提供了相关的函数可以将子区块解码或编码为网端格式（Network Encoding），以供在网络传输区块上使用。

您可以前往 [block.go](./block/block.go) 并将 `const UseNeteaseBlockStates = true` 改为 `const UseNeteaseBlockStates = false` 以将本操作器作为国际版（v1.20.51）的使用。

需要指出的是，**Python** 的内存中几乎不会维护存档的任何部分，在大部分情况下，存档中的区块或子区块，甚至是 **Python** 创建的区块或子区块，都由 **Go** 进行管理，而 **Python** 只控制这些内存的回收。

另外，**Go** 部分的大部分代码参阅并修改自[该存储库](https://github.com/df-mc/dragonfly)，您可以通过它进行更深入的研究（如果可能）。



## 受支持的操作系统及架构
由于 **Bedrock World Operator** 是基于 **Go** 提供动态库供 **Python** 调用的实现，所以不可避免的，未被包含在下述列表内的操作系统及架构不受支持。
当然，我们随时欢迎发起 **Pull Request**。

- Windows
    * x86_64/amd64
    * x86/i686
- Darwin (MacOS)
    * x86_64/amd64
    * arm64/aarch64
- Linux
    * x86_64/amd64
    * arm64
    * aarch64 (Termux on Android)

您可以通过参阅[此文件](./python/package/internal/load_dynamic_library.py)来了解 **Bedrock World Operator** 加载相应动态库的具体逻辑。



## 基础概念
**Bedrock World Operator** 基于以区块坐标（Chunk Pos）、子区块坐标（Sub Chunk Pos）、区块高度范围（Range）、维度（Dimension）、方块及状态（Block States）的定义，实现了区块（Chunk）、子区块（Sub Chunk）的定义。



## 基础功能
在上面定义的基础上，**Bedrock World Operator** 提供一系列基本函数，允许使用者操作区块或子区块中的成分，然后将修改后的数据存入基岩版我的世界存档。

目前已经实现了区块、子区块、生物群落、区块方块实体数据的读写，还没有支持生物数据、玩家数据的读写。目前不考虑将这些未实现的部分纳入未来的更新计划，但欢迎发起 **Pull Request**。



## 额外实现
除了以上基本的标准基岩版我的世界操作实现外，我们根据我们自己的其他需求提供了其他的一些实现，例如可以保存子区块的 **Blob hash**，或保存区块的最后更新时间。



## 实用功能
当然，除了提供以上操作实现外，我们还提供了一些实用函数，如下。
1. 允许将使用者将子区块编码为网端或磁盘端，或把已经编码的二进制解码为子区块。
2. 可以把方块运行时（Block Runtime ID）转换为方块名及其状态，或者进行其逆过程。





# 兼容性
对于目前的 `0.0.x` 版本，我们暂时不考虑后向兼容性，因为本操作器仍然处于早期测试阶段。





# 快速上手
```python
from .world.chunk import Chunk, new_chunk
from .world.sub_chunk import SubChunk, SubChunkWithIndex, new_sub_chunk
from .world.world import World, new_world
from .world.level_dat import LevelDat, Abilities

from .world.constant import (
    EMPTY_COMPOUND,
    EMPTY_BLOCK_STATES,
    DIMENSION_ID_OVERWORLD,
    DIMENSION_ID_NETHER,
    DIMENSION_ID_END,
    DIMENSION_OVERWORLD,
    DIMENSION_NETHER,
    DIMENSION_END,
    RANGE_OVERWORLD,
    RANGE_NETHER,
    RANGE_END,
    RANGE_INVALID,
    AIR_BLOCK_STATES,
    AIR_BLOCK_RUNTIME_ID,
)

from .world.define import (
    ChunkPos,
    SubChunkPos,
    Range,
    Dimension,
    BlockStates,
    QuickChunkBlocks,
    QuickSubChunkBlocks,
    HashWithPosY,
)

from .world.conversion import (
    runtime_id_to_state,
    state_to_runtime_id,
    sub_chunk_network_payload,
    from_sub_chunk_network_payload,
    sub_chunk_disk_payload,
    from_sub_chunk_disk_payload,
)

from nbtlib.tag import Compound, String, Byte, Int
```
我们默认导出了以上类、常量及函数，下面将阐述几个重要的函数。
- `new_chunk` - 创建一个新的区块
- `new_sub_chunk` - 创建一个新的子区块
- `new_world` - 打开或创建一个基岩版存档

在通过上面三个函数得到区块、子区块或存档以后，您可以利用这些类下面实现的各个函数来进行更多操作。

我们在所有对外公开的函数中都提供了足够详尽的注释，因此您不必担心太多。所以，我们不会再提供额外的文档。





# 注意事项
您不应该调用任何来自 `internal` 包的函数，因为它们都只是纯粹的内部实现。

如果您希望对此项目进行贡献，那么您可能需要研究这个包，但更多的，请参阅存储库中的 `c_api` 及 `world` 所指示的 **Go** 实现。





# 🐍 Pypi 包
我们已将此存储库以 **bedrock-world-operator** 的名字上载到 **Pypi** ，您可以通过 `pip install bedrock-world-operator` 快速安装。

访问 [📦 bedrock-world-operator on Pypi](https://pypi.org/project/bedrock-world-operator) 以了解有关此库的更多信息。

我们配置了自动化 **CD/CI 工作流**，因此如果您是本项目的协作者，您可以通过更改 **version** 文件或通过手动触发的方式启动工作流，它会自动编译本项目并将将其上载到 **Pypi** 中。





# 其他
本项目依照 [MIT LICENSE](./LICENSE) 许可证进行许可和授权。
