# 模块定义
- PreComputeModule:用于爬取文献、整理词库等。该模块与检索系统运行时关系不大，只是用于存放用于预先计算的脚本
- RetrievalCore:主要负责检索系统运行时的逻辑，例如涉及到的算法实现，文档推荐排序等等


# 数据结构定义

- 用户实体类型

|字段名|字段类型|字段意义|
|:------|:------|:------|
|id|int|自增id|
|username|str|用户名|
|password|str|密码|
|D|json(list< float >)|用户当前D向量|
|P|json(list< float >)|用户当前P向量|

- session实体类型

|字段名|字段类型|字段意义|
|:------|:------|:------|
|id|int|自增id|
|user|UserModel|用户外键|
|D|json(list< float >)|该次session的D向量|
|P|json(list< float >)|该次session的P向量|
|precision|float|每次session结束后的准确率|


- 文献实体类型

|字段名|字段类型|字段意义|
|:------|:------|:------|
|id|int|自增id|
|md5|64位str|取Title+Authors+Abstract计算出来的64位MD5值|
|Title|str|文献标题|
|Authors|List< str >|文献作者列表|
|Publication|str|文献出版刊物|
|DocURL|str|文献链接(https://doi.org/10.1145/3375462.3375477)|
|Abstract|str|文献摘要|
|References|List< str >|文献引用列表|
|Classification|tinyInt|所属类别|

